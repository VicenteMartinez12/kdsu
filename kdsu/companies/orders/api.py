from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import JsonResponse
from datetime import datetime
import tempfile, os
from django.db import transaction
from kdsu.companies.utils.csv import read_csv
from kdsu.companies.utils.xlsx import read_xlsx
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product
from .models import Order, OrderDetail
from ninja import Body
from ninja import Router



orders_router = Router(tags=["Órdenes"])



def clean_text(value):
    return str(value).strip().replace("\n", "").replace("\r", "").replace("\ufeff", "")

def parse_fecha(fecha_raw):
    import datetime as dt
    if isinstance(fecha_raw, (dt.datetime, dt.date)):
        return fecha_raw.date() if isinstance(fecha_raw, dt.datetime) else fecha_raw
    try:
        return datetime.strptime(clean_text(fecha_raw), "%d/%m/%Y").date()
    except ValueError:
        try:
            return datetime.strptime(clean_text(fecha_raw), "%Y-%m-%d %H:%M:%S").date()
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: {fecha_raw}")

@orders_router.post("/file", summary="Carga de órdenes vía cvs y xlsx", description="Este endpoint permite cargar múltiples órdenes en  formato CSV Y XLSX")
@transaction.atomic
def file_orders(request, file: UploadedFile = File(...)):
    ext = file.name.split('.')[-1].lower()
    if ext not in ["csv", "xlsx"]:
        return JsonResponse({"error": "Archivo no válido. Debe ser CSV o XLSX."}, status=400)

    temp_path = os.path.join(tempfile.gettempdir(), file.name)
    with open(temp_path, 'wb+') as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)

    try:
        data = read_csv(temp_path) if ext == "csv" else read_xlsx(temp_path)
    except Exception as e:
        return JsonResponse({"error": f"Error al leer el archivo: {str(e)}"}, status=400)

    data = [{key.replace(' ', ''): value for key, value in row.items()} for row in data]

    required_columns = [
        "Compania", "Orden", "FechaPedido", "ClaveProveedor", "EsTemporada",
        "EsPagoAnticipado", "Tipo", "SucursalDestino", "ClaveProducto",
        "NumeroArticulo", "Descripcion", "CostoUnitario", "Cantidad",
        "PorcentajeImpuesto", "Unidad", "EmpaqueMaster", "EmpaqueInner", "EsMercanciaSinCargo"
    ]

    missing = [col for col in required_columns if col not in data[0]]
    if missing:
        return JsonResponse({"error": f"Faltan columnas: {', '.join(missing)}"}, status=400)

    ordenes_por_clave = {}
    detalles_por_clave = {}
    detalles_a_guardar = []

    # PRIMERA PASADA: VALIDACIÓN Y PREPARACIÓN EN MEMORIA
    for idx, row in enumerate(data):
        row = {k: clean_text(v) for k, v in row.items()}
        for col in required_columns:
            if col not in row or row[col] == "":
                raise ValueError(f"Fila {idx+1}: El campo '{col}' está vacío o nulo.")

        clave_orden = (row["Compania"], row["Orden"])
        try:
            company = Company.objects.get(short_name=row["Compania"])
        except Company.DoesNotExist:
            raise ValueError(f"La compañía '{row['Compania']}' no existe.")

        if clave_orden not in ordenes_por_clave:
            if Order.objects.filter(company=company, order_id=row["Orden"]).exists():
                raise ValueError(f"La orden '{row['Orden']}' ya existe para la compañía '{row['Compania']}'.")

            try:
                supplier = Supplier.objects.get(company=company, company_supplier_id=row["ClaveProveedor"])
            except Supplier.DoesNotExist:
                raise ValueError(f"No se encontró el proveedor '{row['ClaveProveedor']}'")

            try:
                _ = Warehouse.objects.get(company=company, company_warehouse_id=row["SucursalDestino"])
            except Warehouse.DoesNotExist:
                raise ValueError(f"No se encontró la sucursal '{row['SucursalDestino']}'")

            ordenes_por_clave[clave_orden] = Order(
                company=company,
                supplier=supplier,
                order_id=row["Orden"],
                is_season=row["EsTemporada"].upper() == "S",
                is_prepaid=row["EsPagoAnticipado"].upper() == "S",
                category=row["Tipo"],
                status="Pendiente",
                date_ordered=parse_fecha(row["FechaPedido"])
            )

        try:
            product = Product.objects.get(company=company, supplier=supplier, sku=row["ClaveProducto"])
        except Product.DoesNotExist:
            raise ValueError(f"Producto '{row['ClaveProducto']}' no encontrado.")

        cost = float(row["CostoUnitario"])
        qty = int(row["Cantidad"])
        tax = float(row["PorcentajeImpuesto"])
        mpkg = int(row["EmpaqueMaster"])
        ipkg = int(row["EmpaqueInner"])
        if cost < 0 or qty <= 0 or tax < 0 or mpkg <= 0 or ipkg <= 0:
            raise ValueError(f"Fila {idx+1}: Valores numéricos no válidos.")

        sin_cargo = row["EsMercanciaSinCargo"].upper() == "S"
        if sin_cargo and cost != 0:
            raise ValueError(f"Fila {idx+1}: Mercancía sin cargo debe tener costo 0.")
        if not sin_cargo and cost == 0:
            raise ValueError(f"Fila {idx+1}: Mercancía con cargo no puede tener costo 0.")

        clave_detalle = (row["Orden"], row["SucursalDestino"], row["ClaveProducto"])
        if clave_detalle in detalles_por_clave:
            if detalles_por_clave[clave_detalle] != sin_cargo:
                pass
            else:
                raise ValueError(f"Fila {idx+1}: Producto duplicado en sucursal sin diferencia de cargo.")
        detalles_por_clave[clave_detalle] = sin_cargo

        warehouse = Warehouse.objects.get(company=company, company_warehouse_id=row["SucursalDestino"])

        detalles_a_guardar.append({
            "orden_clave": clave_orden,
            "product": product,
            "warehouse": warehouse,
            "cost": cost,
            "qty": qty,
            "tax": tax,
            "packing_unit": row["Unidad"],
            "mpkg": mpkg,
            "ipkg": ipkg,
            "no_charge": sin_cargo,
            "desc": row["Descripcion"]
        })

   
    for orden in ordenes_por_clave.values():
        orden.save()

    for detalle in detalles_a_guardar:
        order = ordenes_por_clave[detalle["orden_clave"]]
        d = OrderDetail(
            order=order,
            product=detalle["product"],
            warehouse=detalle["warehouse"],
            cost=detalle["cost"],
            quantity=detalle["qty"],
            tax_rate=detalle["tax"],
            packing_unit=detalle["packing_unit"],
            master_package=detalle["mpkg"],
            inner_package=detalle["ipkg"],
            no_charge=detalle["no_charge"],
            description=detalle["desc"]
        )
        d.calculate()

    for orden in ordenes_por_clave.values():
        orden.calculate()

    return JsonResponse({
        "message": f"Archivo procesado exitosamente. Órdenes creadas: {len(ordenes_por_clave)}, registros: {len(detalles_a_guardar)}"
    })
    
    
    
      
    
@orders_router.post("/json" ,summary="Carga de órdenes vía JSON",  description="Este endpoint permite cargar múltiples órdenes en formato JSON")
@transaction.atomic
def json_orders(request, payload: dict = Body(...)):
    ordenes_response = {}

    if "ordenes" not in payload or not isinstance(payload["ordenes"], list):
        return JsonResponse({"error": "La estructura no es válida"}, status=400)

    for orden in payload["ordenes"]:
        try:
            clave_orden = orden.get("orden")
            response = {"insertado": False}

            # Validar estructura y campos requeridos
            required_order_fields = [
                "compania", "orden", "fechaPedido", "claveProveedor", "esTemporada",
                "esPagoAnticipado", "tipo", "productos"
            ]
            for field in required_order_fields:
                if field not in orden or orden[field] in [None, ""]:
                    response["respuesta"] = "La estructura no es válida"
                    ordenes_response[clave_orden] = response
                    break
            else:
                productos = orden["productos"]
                if not productos:
                    response["respuesta"] = "La orden debe contener al menos un producto"
                    ordenes_response[clave_orden] = response
                    continue

                try:
                    company = Company.objects.get(short_name=orden["compania"])
                except Company.DoesNotExist:
                    response["respuesta"] = f"No se encontró la compañía {orden['compania']}"
                    ordenes_response[clave_orden] = response
                    continue

                if Order.objects.filter(company=company, order_id=clave_orden).exists():
                    response["respuesta"] = f"La orden {clave_orden} ya existe"
                    ordenes_response[clave_orden] = response
                    continue

                try:
                    supplier = Supplier.objects.get(company=company, company_supplier_id=orden["claveProveedor"])
                except Supplier.DoesNotExist:
                    response["respuesta"] = f"No se encontró el proveedor {orden['claveProveedor']}"
                    ordenes_response[clave_orden] = response
                    continue

                detalles = []
                claves_usadas = set()
                for p in productos:
                    for attr in ["sucursalDestino", "clave", "descripcion", "costoUnitario",
                                 "cantidad", "porcentajeImpuesto", "unidad", "empaqueMaster",
                                 "empaqueInner", "esMercanciaSinCargo"]:
                        if attr not in p:
                            response["respuesta"] = "La estructura no es válida"
                            ordenes_response[clave_orden] = response
                            break
                    else:
                        try:
                            warehouse = Warehouse.objects.get(company=company, company_warehouse_id=p["sucursalDestino"])
                        except Warehouse.DoesNotExist:
                            response["respuesta"] = f"No se encontró la sucursal {p['sucursalDestino']}"
                            ordenes_response[clave_orden] = response
                            break

                        try:
                            product = Product.objects.get(company=company, supplier=supplier, sku=p["clave"])
                        except Product.DoesNotExist:
                            response["respuesta"] = f"Producto '{p['clave']}' no encontrado"
                            ordenes_response[clave_orden] = response
                            break

                        costo = float(p["costoUnitario"])
                        cantidad = int(p["cantidad"])
                        impuesto = float(p["porcentajeImpuesto"])
                        master = int(p["empaqueMaster"])
                        inner = int(p["empaqueInner"])
                        sin_cargo = p["esMercanciaSinCargo"]

                        if cantidad <= 0:
                            response["respuesta"] = f"El valor de cantidad para el producto {p['clave']} de la sucursal {p['sucursalDestino']} no es válido"
                            ordenes_response[clave_orden] = response
                            break
                        if costo < 0:
                            response["respuesta"] = f"El valor de costoUnitario para el producto {p['clave']} de la sucursal {p['sucursalDestino']} no es válido"
                            ordenes_response[clave_orden] = response
                            break
                        if master <= 0 or inner <= 0:
                            response["respuesta"] = f"El valor de empaqueMaster/Inner para el producto {p['clave']} de la sucursal {p['sucursalDestino']} no es válido"
                            ordenes_response[clave_orden] = response
                            break

                        clave_detalle = (p["sucursalDestino"], p["clave"])
                        if clave_detalle in claves_usadas:
                            response["respuesta"] = f"El producto {p['clave']} se especificó más de una vez para la sucursal {p['sucursalDestino']}"
                            ordenes_response[clave_orden] = response
                            break
                        claves_usadas.add(clave_detalle)

                        if sin_cargo and costo != 0:
                            response["respuesta"] = f"El producto {p['clave']} en la sucursal {p['sucursalDestino']} es mercancía sin cargo, su costo debe ser 0"
                            ordenes_response[clave_orden] = response
                            break
                        if not sin_cargo and costo == 0:
                            response["respuesta"] = f"El producto {p['clave']} en la sucursal {p['sucursalDestino']} no es mercancía sin cargo, su costo debe ser mayor a 0"
                            ordenes_response[clave_orden] = response
                            break

                        detalles.append({
                            "product": product,
                            "warehouse": warehouse,
                            "cost": costo,
                            "quantity": cantidad,
                            "tax_rate": impuesto,
                            "packing_unit": p["unidad"],
                            "master_package": master,
                            "inner_package": inner,
                            "no_charge": sin_cargo,
                            "description": p["descripcion"]
                        })

                if response.get("respuesta"):
                    continue

                orden_obj = Order.objects.create(
                    company=company,
                    supplier=supplier,
                    order_id=clave_orden,
                    is_season=orden["esTemporada"],
                    is_prepaid=orden["esPagoAnticipado"],
                    category=orden["tipo"],
                    status="new",
                    date_ordered=datetime.strptime(orden["fechaPedido"], "%Y-%m-%d %H:%M:%S")
                )

                for d in detalles:
                    detail = OrderDetail.objects.create(order=orden_obj, **d)
                    detail.calculate()

                orden_obj.calculate()

                response = {
                    "insertado": True,
                    "referencia": orden_obj.id,
                    "fechaInsercion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        except Exception as e:
            response = {
                "insertado": False,
                "respuesta": "Ocurrió un error al insertar la orden"
            }

        ordenes_response[clave_orden] = response

    return JsonResponse({"ordenes": ordenes_response})

    
    
    
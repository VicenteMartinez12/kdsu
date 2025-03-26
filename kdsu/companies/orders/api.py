from ninja import NinjaAPI, File
from ninja.files import UploadedFile
from django.http import JsonResponse
import mimetypes
from datetime import datetime
import tempfile, os
from kdsu.companies.utils.csv import read_csv
from kdsu.companies.utils.xlsx import read_xlsx
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product
from .models import Order, OrderDetail
from django.db import transaction


api = NinjaAPI(urls_namespace="orders_api")

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

@api.post("/orders/upload")
@transaction.atomic
def upload_orders(request, file: UploadedFile = File(...)):
    ext = file.name.split('.')[-1].lower()
    if ext not in ["csv", "xlsx"]:
        return JsonResponse({"error": "Archivo no válido. Debe ser CSV o XLSX."}, status=400)

    temp_path = os.path.join(tempfile.gettempdir(), file.name)
    with open(temp_path, 'wb+') as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)

    try:
        if ext == "csv":
            data = read_csv(temp_path)
        else:
            data = read_xlsx(temp_path)
    except Exception as e:
        return JsonResponse({"error": f"Error al leer el archivo: {str(e)}"}, status=400)

    cleaned_data = []
    for row in data:
        cleaned_row = {key.replace(' ', ''): value for key, value in row.items()}
        cleaned_data.append(cleaned_row)
    data = cleaned_data

    required_columns = [
        "Compania", "Orden", "FechaPedido", "ClaveProveedor", "EsTemporada",
        "EsPagoAnticipado", "Tipo", "SucursalDestino", "ClaveProducto",
        "NumeroArticulo", "Descripcion", "CostoUnitario", "Cantidad",
        "PorcentajeImpuesto", "Unidad", "EmpaqueMaster", "EmpaqueInner", "EsMercanciaSinCargo"
    ]

    missing = [col for col in required_columns if col not in data[0]]
    if missing:
        return JsonResponse({"error": f"Faltan columnas: {', '.join(missing)}"}, status=400)

    registros = 0
    ordenes_creadas = {}
    detalles_por_orden = {}

    for idx, row in enumerate(data):
        cleaned = {k: clean_text(v) for k, v in row.items() if v not in [None, ""]}
        for col in required_columns:
            if col not in cleaned or cleaned[col] == "":
                return JsonResponse({"error": f"Fila {idx+1}: El campo '{col}' está vacío o nulo."}, status=400)

        clave = (clean_text(row["Compania"]), clean_text(row["Orden"]))

        try:
            company = Company.objects.get(short_name=clean_text(row["Compania"]))
        except Company.DoesNotExist:
            return JsonResponse({"error": f"La compañía '{row['Compania']}' no existe."}, status=400)

        if clave not in ordenes_creadas:
            if Order.objects.filter(company=company, order_id=clean_text(row["Orden"])).exists():
                return JsonResponse({"error": f"La orden '{row['Orden']}' ya existe para la compañía '{row['Compania']}'."}, status=400)

            try:
                supplier = Supplier.objects.get(company=company, company_supplier_id=clean_text(row["ClaveProveedor"]))
                warehouse = Warehouse.objects.get(company=company, company_warehouse_id=clean_text(row["SucursalDestino"]))
            except Exception as e:
                return JsonResponse({"error": f"Error al buscar catálogos: {str(e)}"}, status=400)

            order = Order.objects.create(
                company=company,
                supplier=supplier,
                order_id=clean_text(row["Orden"]),
                is_season=clean_text(row["EsTemporada"]).upper() == "S",
                is_prepaid=clean_text(row["EsPagoAnticipado"]).upper() == "S",
                category=clean_text(row["Tipo"]),
                status="Pendiente",
                date_ordered=parse_fecha(row["FechaPedido"])
            )
            ordenes_creadas[clave] = order

        order = ordenes_creadas[clave]

        try:
            product = Product.objects.get(
                company=company,
                supplier=order.supplier,
                sku=clean_text(row["ClaveProducto"]),
            )
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Producto '{row['ClaveProducto']}' no encontrado."}, status=400)

        try:
            cost = float(row["CostoUnitario"])
            quantity = int(row["Cantidad"])
            tax = float(row["PorcentajeImpuesto"])
            mpkg = int(row["EmpaqueMaster"])
            ipkg = int(row["EmpaqueInner"])
        except ValueError:
            return JsonResponse({"error": f"Fila {idx+1}: Datos numéricos inválidos."}, status=400)

        if cost < 0 or quantity <= 0 or tax < 0 or mpkg <= 0 or ipkg <= 0:
            return JsonResponse({"error": f"Fila {idx+1}: Los valores numéricos deben ser mayores a 0 y no negativos."}, status=400)

        sin_cargo = clean_text(row["EsMercanciaSinCargo"]).upper() == "S"
        if sin_cargo and cost != 0:
            return JsonResponse({"error": f"Fila {idx+1}: Mercancía sin cargo debe tener costo 0."}, status=400)
        if not sin_cargo and cost == 0:
            return JsonResponse({"error": f"Fila {idx+1}: Mercancía con cargo no puede tener costo 0."}, status=400)
            

        clave_uni = (clean_text(row["Orden"]), clean_text(row["SucursalDestino"]), clean_text(row["ClaveProducto"]))
        if clave_uni in detalles_por_orden:
            if detalles_por_orden[clave_uni] != sin_cargo:
                pass
            else:
                return JsonResponse({"error": f"Fila {idx+1}: Producto duplicado para sucursal y orden sin diferencia de cargo."}, status=400)
        else:
            detalles_por_orden[clave_uni] = sin_cargo

        OrderDetail.objects.create(
            order=order,
            product=product,
            warehouse=warehouse,
            cost=cost,
            quantity=quantity,
            tax_rate=tax,
            packing_unit=clean_text(row["Unidad"]),
            master_package=mpkg,
            inner_package=ipkg,
            no_charge=sin_cargo,
            description=clean_text(row["Descripcion"])
        )
        registros += 1

    for orden in ordenes_creadas.values():
        orden.calculate()

    return JsonResponse({"message": f"Archivo procesado exitosamente. Órdenes creadas: {len(ordenes_creadas)}, registros: {registros}"})

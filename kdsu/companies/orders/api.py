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

    for row in data:
        if not row.get("Compania") or not row.get("Orden"):
            continue

        key = (clean_text(row["Compania"]), clean_text(row["Orden"]))

        if key not in ordenes_creadas:
            try:
                company = Company.objects.get(short_name=clean_text(row["Compania"]))
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
            ordenes_creadas[key] = order

        else:
            order = ordenes_creadas[key]

        try:
            product = Product.objects.get(company=order.company, sku=clean_text(row["ClaveProducto"]))
        except Product.DoesNotExist:
            return JsonResponse({"error": f"Producto '{row['ClaveProducto']}' no encontrado."}, status=400)

        OrderDetail.objects.create(
            order=order,
            product=product,
            warehouse=warehouse,
            cost=float(row["CostoUnitario"]),
            quantity=int(row["Cantidad"]),
            tax_rate=float(row["PorcentajeImpuesto"]),
            packing_unit=clean_text(row["Unidad"]),
            master_package=int(row["EmpaqueMaster"]),
            inner_package=int(row["EmpaqueInner"]),
            no_charge=clean_text(row["EsMercanciaSinCargo"]).upper() == "S",
            description=clean_text(row["Descripcion"])
        )
        registros += 1

    for orden in ordenes_creadas.values():
        orden.calculate()

    return JsonResponse({"message": f"Archivo procesado exitosamente. Órdenes creadas: {len(ordenes_creadas)}, registros: {registros}"})
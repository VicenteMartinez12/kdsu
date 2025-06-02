import io

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from decimal import Decimal
from .models import Order, OrderDetail
from .forms import OrderForm, OrderDetailForm
from django.conf import settings
from django.shortcuts import get_object_or_404
import pdfkit
from kdsu.companies import pdf_config
from django.template.loader import render_to_string
from django.http import HttpResponse
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse
from io import BytesIO
import json
import os
from reportlab.lib.utils import ImageReader
from django.views.decorators.http import require_GET
from xml.etree.ElementTree import Element, SubElement, ElementTree,fromstring,parse






def plantilla_consultas_view(request):
    orders = Order.objects.select_related('supplier').all()
    
    # Proveedores únicos (por ID) usados en las órdenes
    suppliers = orders.values_list('supplier__id', 'supplier__short_name').distinct()

    return render(request, 'orders/plantilla_consultas.html', {
        'orders': orders,
        'suppliers': suppliers
    })
    
    
def plantilla_pdf_view(request):
    orders = Order.objects.select_related('supplier').all()
    
    # Proveedores únicos (por ID) usados en las órdenes
    suppliers = orders.values_list('supplier__id', 'supplier__short_name').distinct()

    return render(request, 'orders/plantilla_pdf.html', {
        'orders': orders,
        'suppliers': suppliers
    })



   
def index2(request):
    return render(request, 'orders/index.html')


def descarga_pedidos_view(request):
    orders_qs = Order.objects.select_related('company', 'supplier') \
                             .prefetch_related('orderdetail_set__warehouse__address') \
                             .all()

    companias = orders_qs.values_list('company__id', 'company__name').distinct()
    estatuses = orders_qs.values_list('status', flat=True).distinct()

    # Valores por defecto
    default_company_id = companias[0][0] if companias else None
    selected_company_id = request.GET.get('company_id', str(default_company_id))
    selected_status = request.GET.get('status', 'Nuevo')

    # Aplicar filtros
    if selected_company_id:
        orders_qs = orders_qs.filter(company_id=selected_company_id)
    if selected_status:
        orders_qs = orders_qs.filter(status=selected_status)

    return render(request, 'orders/descargaPedidos.html', {
        'orders': orders_qs,
        'companias': companias,
        'estatuses': estatuses,
        'selected_company_id': str(selected_company_id),
        'selected_status': selected_status
    })






def obtener_tabla_descarga_pedidos(request):
    company_id = request.GET.get('compania_id')
    status = request.GET.get('estatus')

    orders = Order.objects.select_related('company', 'supplier') \
                          .prefetch_related('orderdetail_set__warehouse__address') \
                          .all()

    if company_id:
        orders = orders.filter(company_id=company_id)
    if status:
        orders = orders.filter(status=status)

    tbody_html = render_to_string('orders/partials/tabla_descarga_pedidos.html', {
        'orders': orders
    })

    return JsonResponse({'tbody': tbody_html})




class OrderTestView(View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        return render(request, 'orders/prueba.html', {'orders': orders})

    def post(self, request, *args, **kwargs):
        order_form = OrderForm(request.POST)
        detail_form = OrderDetailForm(request.POST)

        if order_form.is_valid():
            order = order_form.save()
            order.calculate()
            return JsonResponse({'message': 'Orden creada y calculada', 'order_id': order.id})

        if detail_form.is_valid():
            order_detail = detail_form.save()
            order_detail.calculate()
            order_detail.order.calculate()
            return JsonResponse({'message': 'Detalle creado y calculado', 'order_detail_id': order_detail.id})

        return JsonResponse({'error': 'Invalid data'}, status=400)
    
    
    
    # modales de pantallas


def obtener_detalles_orden(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    detalles = []
    costos = []

    for detalle in order.orderdetail_set.select_related('product', 'warehouse'):
        detalles.append({
            'product': detalle.product.sku,
            'warehouse': detalle.warehouse.name
        })
        costos.append({
            'cost': str(detalle.cost),
            'quantity': detalle.quantity,
            'subtotal': str(detalle.subtotal),
            'tax_rate': str(detalle.tax_rate),
            'tax_value': str(detalle.tax_value),
            'total': str(detalle.total),
        })

    return JsonResponse({
        'detalles': detalles,
        'costos': costos,
        'order_id': order.order_id
    })
    
    
    
    

def obtener_detalle_descarga_pedidos(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    
    detalles = []
    for detalle in order.orderdetail_set.select_related('product'):
        detalles.append({
            'sku': detalle.product.sku,
            'descripcion': detalle.description,
            'sin_cargo': 'Sí' if detalle.no_charge else 'No',
            'cantidad': detalle.quantity,
            'empaque': detalle.master_package,
            'subempaque': detalle.inner_package,
        })

    return JsonResponse({
        'descargaPedidos': detalles,
        'order_id': order.order_id
    })
    
    
    
    
    
    ################ Creacion del pdf
    
    
def pdf_header(p, width, height, company, order, page_num):
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'tony.png')
    margin_left = 20
    rect_x = width - 150
    rect_y = height - 115
    rect_width = 130
    rect_height = 60

    # Logo
    if os.path.exists(logo_path):
        p.drawImage(logo_path, margin_left, height - 100, width=100, height=50, mask='auto')

    # Títulos centrales
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, height - 60, company.name)
    p.drawCentredString(width / 2, height - 80, "ORDEN DE MERCANCÍA")
    warehouse = order.orderdetail_set.first().warehouse if order.orderdetail_set.exists() else None
    if warehouse:
        sucursal_text = f"{warehouse.company_warehouse_id} - {warehouse.name}"
    else:
        sucursal_text = "Sucursal no disponible"

    p.drawCentredString(width / 2, height - 100, sucursal_text)

    # Cuadro a la derecha
    p.rect(rect_x, rect_y, rect_width, rect_height)
    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 5, rect_y + rect_height - 12, "NO.PEDIDO:")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(rect_x + 65, rect_y + rect_height - 12, f"{order.order_id}")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 5, rect_y + rect_height - 24, "FECHA:")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(rect_x + 65, rect_y + rect_height - 24, f"{order.date_ordered.strftime('%d/%m/%Y')}")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 5, rect_y + rect_height - 36, "ENTREGA:")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(rect_x + 65, rect_y + rect_height - 36, "ALMACÉN")

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 5, rect_y + rect_height - 48, "PÁGINA:")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(rect_x + 65, rect_y + rect_height - 48, f"{page_num}")

    # Proveedor y Razón Social
    p.setFont("Helvetica", 8)
    p.drawString(margin_left, height - 150, "CVE.PROVEEDOR:")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(margin_left + 75, height - 150, f"{order.supplier.company_supplier_id}")

    p.setFont("Helvetica", 8)
    p.drawString(margin_left + 220, height - 150, "RAZÓN SOCIAL:")
    p.setFont("Helvetica-Bold", 8)
    p.drawString(margin_left + 285, height - 150, f"{order.supplier.name}")
    
    
    
    
    
    
    
    
    
    
def pdf_footer(p, width, company, warehouse):
    start_y = 20
    box_height = 60

    margin_sides = 20  # mismo margen que la tabla
    usable_width = width - 2 * margin_sides

    box1_width = usable_width * 0.39
    box2_width = usable_width * 0.39
    box3_width = usable_width - box1_width - box2_width  # Ajuste dinámico

    # Caja 1 - Factura A
    p.rect(margin_sides, start_y, box1_width, box_height)
    margin_x = margin_sides + 5
    margin_y = start_y + box_height - 12
    line_spacing = 10

    p.setFont("Helvetica", 7)
    p.drawString(margin_x, margin_y, "FACTURAR A:")
    margin_y -= line_spacing
    p.setFont("Helvetica-Bold", 7)
    p.drawString(margin_x, margin_y, f"{company.name}")
    margin_y -= line_spacing
    address = company.address
    p.drawString(margin_x, margin_y, f"{address.street} {address.exterior_number}, {address.neighborhood}")
    margin_y -= line_spacing
    p.drawString(margin_x, margin_y, f"CP {address.postcode} {address.city}, {address.state}")

    # Línea divisoria horizontal
    p.line(margin_sides, start_y + 12, margin_sides + box1_width, start_y + 12)
    p.setFont("Helvetica", 7)
    p.drawString(margin_x, start_y + 2, "POR TRANSPORTES:")
    p.setFont("Helvetica-Bold", 7)
    p.drawString(margin_x + 75, start_y + 2, "PROVEEDOR")

    # Caja 2 - Consignar a
    box2_x = margin_sides + box1_width
    p.rect(box2_x, start_y, box2_width, box_height)
    margin_x = box2_x + 5
    margin_y = start_y + box_height - 12

    p.setFont("Helvetica", 7)
    p.drawString(margin_x, margin_y, "CONSIGNAR A:")
    margin_y -= line_spacing
    p.setFont("Helvetica-Bold", 7)
    p.drawString(margin_x, margin_y, f"{warehouse.company_warehouse_id}  {warehouse.name}")
    margin_y -= line_spacing
    wh_address = warehouse.address
    p.drawString(margin_x, margin_y, f"{wh_address.street} {wh_address.exterior_number}, {wh_address.neighborhood}")
    margin_y -= line_spacing
    p.drawString(margin_x, margin_y, f"{wh_address.city}, {wh_address.state}")

    # Caja 3 - Vacía
    box3_x = box2_x + box2_width
    p.rect(box3_x, start_y, box3_width, box_height)






    
@require_GET
def export_pdf(request):
    order_ids = request.GET.getlist('order_ids[]')

    if not order_ids:
        return HttpResponse("Parámetros faltantes", status=400)

    orders = Order.objects.filter(id__in=order_ids).select_related('company')

    if not orders.exists():
        return HttpResponse("No se encontraron órdenes", status=404)

    first_company = orders[0].company
    if not all(order.company_id == first_company.id for order in orders):
        return HttpResponse("Todas las órdenes deben pertenecer a la misma compañía.", status=400)

    company = first_company

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ordenes.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    for order in orders:
        page_number = 1
        pdf_header(p, width, height, company, order, page_number)

        y_position = height - 160

        if order.is_prepaid:
            headers = ["SKU", "Cantidad", "U/M", "Descripción", "No. Art.", "Empaque", "P. Unit", "Total", "Bultos"]
            col_x_positions = [20, 80, 130, 160, 320, 370, 420, 470, 520]
        else:
            headers = ["SKU", "Cantidad", "U/M", "Descripción", "No. Art.", "Empaque", "Bultos"]
            col_x_positions = [20, 80, 125, 175, 420, 470, 530]

        cell_height = 22
        text_vertical_offset = 4

        p.setFont("Helvetica-Bold", 9)
        for idx, header in enumerate(headers):
            next_col_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
            p.rect(col_x_positions[idx], y_position - cell_height, next_col_x - col_x_positions[idx], cell_height)
            cell_center_x = (col_x_positions[idx] + next_col_x) / 2
            p.drawCentredString(cell_center_x, y_position - cell_height + text_vertical_offset + 4, header)

        y_position -= 35
        p.setFont("Helvetica", 8)

        subtotal = 0
        iva = 0
        total = 0

        details = order.orderdetail_set.all()
        for i, detail in enumerate(details):
            bultos = ""
            if detail.master_package and detail.inner_package:
                if detail.quantity % (detail.master_package * detail.inner_package) == 0:
                    bultos = str(detail.quantity // (detail.master_package * detail.inner_package))

            if order.is_prepaid:
                detail_values = [
                    detail.product.sku,
                    str(detail.quantity),
                    detail.product.packing_unit,
                    detail.product.description[:30],
                    detail.product.mpn,
                    f"{detail.master_package}/{detail.inner_package}",
                    f"${detail.cost:.2f}",
                    f"${detail.subtotal:.2f}",
                    bultos
                ]
            else:
                detail_values = [
                    detail.product.sku,
                    str(detail.quantity),
                    detail.product.packing_unit,
                    detail.product.description[:30],
                    detail.product.mpn,
                    f"{detail.master_package}/{detail.inner_package}",
                    bultos
                ]

            for idx, val in enumerate(detail_values):
                x = col_x_positions[idx]
                next_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
                center_x = (x + next_x) / 2
                align = 'left'

                if order.is_prepaid:
                    if idx in [0, 2, 4]:
                        align = 'center'
                    elif idx in [1, 5, 6, 7, 8]:
                        align = 'right'
                else:
                    if idx in [0, 2, 4]:
                        align = 'center'
                    elif idx in [1, 5, 6]:
                        align = 'right'

                if align == 'center':
                    p.drawCentredString(center_x, y_position, val)
                elif align == 'right':
                    p.drawRightString(next_x - 2, y_position, val)
                else:
                    p.drawString(x, y_position, val)

            subtotal += detail.subtotal
            iva += detail.tax_value
            total += detail.total

            y_position -= 18

            if i + 1 == len(details):
                if y_position < 100:
                    p.showPage()
                    page_number += 1
                    pdf_header(p, width, height, company, order, page_number)
                    y_position = height - 160
                    p.setFont("Helvetica-Bold", 9)
                    for idx, header in enumerate(headers):
                        next_col_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
                        p.rect(col_x_positions[idx], y_position - cell_height, next_col_x - col_x_positions[idx], cell_height)
                        cell_center_x = (col_x_positions[idx] + next_col_x) / 2
                        p.drawCentredString(cell_center_x, y_position - cell_height + text_vertical_offset + 4, header)
                    y_position -= 35
                    p.setFont("Helvetica", 8)

            elif y_position < 115:
                p.showPage()
                page_number += 1
                pdf_header(p, width, height, company, order, page_number)
                y_position = height - 160
                p.setFont("Helvetica-Bold", 9)
                for idx, header in enumerate(headers):
                    next_col_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
                    p.rect(col_x_positions[idx], y_position - cell_height, next_col_x - col_x_positions[idx], cell_height)
                    cell_center_x = (col_x_positions[idx] + next_col_x) / 2
                    p.drawCentredString(cell_center_x, y_position - cell_height + text_vertical_offset + 4, header)
                y_position -= 35
                p.setFont("Helvetica", 8)

        if order.is_prepaid:
            if y_position < 100:
                p.showPage()
                page_number += 1
                pdf_header(p, width, height, company, order, page_number)
                y_position = height - 160

            y_position += 5
            p.setFont("Helvetica-Bold", 8)
            p.line(475, y_position + 8, 530, y_position + 8)
            p.drawRightString(460, y_position, "SUBTOTAL:")
            p.drawString(482.5, y_position, f"${subtotal:,.2f}")
            y_position -= 15
            p.drawRightString(460, y_position, "IVA:")
            p.drawString(482.5, y_position, f"${iva:,.2f}")
            y_position -= 15
            p.drawRightString(460, y_position, "TOTAL:")
            p.drawString(482.5, y_position, f"${total:,.2f}")

        first_detail = details.first()
        if first_detail and first_detail.warehouse:
            pdf_footer(p, width, company, first_detail.warehouse)
        else:
            pdf_footer(
                p,
                width,
                company,
                Warehouse(name="SIN DATOS", company_warehouse_id="N/A", address=company.address)
            )

        p.showPage()

    p.save()
    return response


###Fin de la creacion del pdf




#Exportacion del xml

@require_GET
def export_xml(request):
    order_ids = request.GET.getlist('order_ids[]')

    if not order_ids:
        return HttpResponse("Parámetros faltantes", status=400)

    orders = Order.objects.filter(id__in=order_ids).select_related('supplier')

    if not orders.exists():
        return HttpResponse("No se encontraron órdenes", status=404)

    company = orders[0].company
    root = Element("OrdenesCompras")

   
    xsd_path = os.path.join(settings.BASE_DIR, 'static', 'ordenes.xsd')
    try:
        xsd_tree = parse(xsd_path)
        schema_element = xsd_tree.getroot()
        root.append(schema_element)
    except Exception as e:
        return HttpResponse(f"Error al cargar XSD: {e}", status=500)

    for order in orders:
        orden_el = SubElement(root, "OrdenCompra", {
            "Pedido": order.order_id,
            "Fecha": order.date_ordered.isoformat(),
            "Temporada": "S" if order.is_season else "",
            "B_PagoAnt": "S" if order.is_prepaid else "N"
        })

        detalle = order.orderdetail_set.first()
        wh = detalle.warehouse if detalle else None
        wh_address = wh.address if wh else None

        if wh and wh_address:
            SubElement(orden_el, "Consignar", {
                "Sucursal": wh.company_warehouse_id,
                "Nombre": wh.name,
                "Calle": wh_address.street,
                "Nointerior": wh_address.interior_number,
                "Noexterior": wh_address.exterior_number,
                "Colonia": wh_address.neighborhood,
                "CodigoPostal": wh_address.postcode,
                "Ciudad": wh_address.city,
                "Estado": wh_address.state,
                "Entregar": "CENTRA"
            })

        detalles_el = SubElement(orden_el, "Detalles")

        for d in order.orderdetail_set.all():
            SubElement(detalles_el, "DetalleCompra", {
                "Producto": d.product.sku,
                "NoArt": d.product.mpn,
                "Descripcion": d.description,
                "Cantidad": str(d.quantity),
                "Unidad": d.packing_unit,
                "Empaque": str(d.master_package),
                "Subempaque": str(d.inner_package),
                "Cargo": "N" if d.no_charge else "S"
            })

    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="ordenes_export.xml"'
    tree = ElementTree(root)
    tree.write(response, encoding='utf-8', xml_declaration=False)
    return response


@require_GET
def export_xml_excel(request):
    order_ids = request.GET.getlist('order_ids[]')

    if not order_ids:
        return HttpResponse("Parámetros faltantes", status=400)

    orders = Order.objects.filter(id__in=order_ids).select_related('supplier')

    if not orders.exists():
        return HttpResponse("No se encontraron órdenes", status=404)

    root = Element("OrdenesCompras")

    for order in orders:
        orden_el = SubElement(root, "OrdenCompra", {
            "Pedido": order.order_id,
            "Fecha": order.date_ordered.isoformat(),
            "Temporada": "S" if order.is_season else "",
            "B_PagoAnt": "S" if order.is_prepaid else "N"
        })

        detalle = order.orderdetail_set.first()
        wh = detalle.warehouse if detalle else None
        wh_address = wh.address if wh else None

        if wh and wh_address:
            SubElement(orden_el, "Consignar", {
                "Sucursal": wh.company_warehouse_id,
                "Nombre": wh.name,
                "Calle": wh_address.street,
                "Nointerior": wh_address.interior_number,
                "Noexterior": wh_address.exterior_number,
                "Colonia": wh_address.neighborhood,
                "CodigoPostal": wh_address.postcode,
                "Ciudad": wh_address.city,
                "Estado": wh_address.state,
                "Entregar": "CENTRA"
            })

        detalles_el = SubElement(orden_el, "Detalles")

        for d in order.orderdetail_set.all():
            SubElement(detalles_el, "DetalleCompra", {
                "Producto": d.product.sku,
                "NoArt": d.product.mpn,
                "Descripcion": d.description,
                "Cantidad": str(d.quantity),
                "Unidad": d.packing_unit,
                "Empaque": str(d.master_package),
                "Subempaque": str(d.inner_package),
                "Cargo": "N" if d.no_charge else "S"
            })

    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="ordenes_excel.xml"'
    tree = ElementTree(root)
    tree.write(response, encoding='utf-8', xml_declaration=False)
    return response





#Aqui termina la exportacion de los xml




#Exportacion del JSON 

@require_GET
def export_json(request):
    order_ids = request.GET.getlist('order_ids[]')

    if not order_ids:
        return HttpResponse("Parámetros faltantes", status=400)

    orders = Order.objects.filter(id__in=order_ids)

    if not orders.exists():
        return HttpResponse("No se encontraron órdenes", status=404)

    data = []

    for order in orders:
        detalle = order.orderdetail_set.first()
        wh = detalle.warehouse if detalle else None
        wh_address = wh.address if wh else None

        order_data = {
            "Pedido": order.order_id,
            "Fecha": order.date_ordered.strftime('%Y-%m-%d'),
            "Temporada": "S" if order.is_season else "",
            "B_PagoAnt": "S" if order.is_prepaid else "N",
            "Consignar": {},
            "Detalles": []
        }

        if wh and wh_address:
            order_data["Consignar"] = {
                "Sucursal": wh.company_warehouse_id,
                "Nombre": wh.name,
                "Calle": wh_address.street,
                "Nointerior": wh_address.interior_number,
                "Noexterior": wh_address.exterior_number,
                "Colonia": wh_address.neighborhood,
                "CodigoPostal": wh_address.postcode,
                "Ciudad": wh_address.city,
                "Estado": wh_address.state,
                "Entregar": "CENTRA"
            }

        for d in order.orderdetail_set.all():
            detail = {
                "Producto": d.product.sku,
                "NoArt": d.product.mpn,
                "Descripcion": d.description,
                "Cantidad": d.quantity,
                "Unidad": d.packing_unit,
                "Empaque": d.master_package,
                "Subempaque": d.inner_package,
                "Cargo": "N" if d.no_charge else "S"
            }
            order_data["Detalles"].append(detail)

        data.append(order_data)

    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="ordenes.json"'
    return response


### Aqui termina la exportacion del Json
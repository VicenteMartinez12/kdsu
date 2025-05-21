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
import os
from reportlab.lib.utils import ImageReader






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
    
    
def draw_pdf_header(p, width, height, company, order, page_num):
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
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 50, company.name)
    p.drawCentredString(width / 2, height - 75, "ORDEN DE MERCANCÍA")
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
    p.setFont("Helvetica", 10)
    p.drawString(margin_left, height - 150, "CV.PROVEEDOR:")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(margin_left + 90, height - 150, f"{order.supplier.company_supplier_id}")

    p.setFont("Helvetica", 10)
    p.drawString(margin_left + 220, height - 150, "RAZÓN SOCIAL:")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(margin_left + 300, height - 150, f"{order.supplier.name}")
    
    
    
    
    
    
    
    
    
    
def draw_footer(p, width, company, warehouse):
    start_y = 20
    box_height = 60
    box1_width = width * 0.39
    box2_width = width * 0.39
    box3_width = width - box1_width - box2_width - 20

    # Caja 1 - Factura A
    p.rect(10, start_y, box1_width, box_height)
    margin_x = 15
    margin_y = start_y + box_height - 12
    line_spacing = 10  # Espacio entre líneas

    p.setFont("Helvetica", 8)
    p.drawString(margin_x, margin_y, "FACTURAR A:")
    margin_y -= line_spacing
    p.setFont("Helvetica-Bold", 9)
    p.drawString(margin_x, margin_y, f"{company.name}")
    margin_y -= line_spacing
    address = company.address
    p.drawString(margin_x, margin_y, f"{address.street} {address.exterior_number}, {address.neighborhood}")
    margin_y -= line_spacing
    p.drawString(margin_x, margin_y, f"CP {address.postcode} {address.city}, {address.state}")

    # Línea divisoria horizontal para "POR TRANSPORTES:"
    p.line(10, start_y + 12, 10 + box1_width, start_y + 12)
    p.setFont("Helvetica", 8)
    p.drawString(15, start_y + 2, "POR TRANSPORTES:")
    p.setFont("Helvetica-Bold", 9)
    p.drawString(100, start_y + 2, "PROVEEDOR")

    # Caja 2 - Consignar a
    p.rect(10 + box1_width, start_y, box2_width, box_height)
    margin_x = 15 + box1_width
    margin_y = start_y + box_height - 12

    p.setFont("Helvetica", 8)
    p.drawString(margin_x, margin_y, "CONSIGNAR A:")
    margin_y -= line_spacing
    p.setFont("Helvetica-Bold", 9)
    p.drawString(margin_x, margin_y, f"{warehouse.company_warehouse_id}  {warehouse.name}")
    margin_y -= line_spacing
    wh_address = warehouse.address
    p.drawString(margin_x, margin_y, f"{wh_address.street} {wh_address.exterior_number}, {wh_address.neighborhood}")
    margin_y -= line_spacing
    p.drawString(margin_x, margin_y, f"{wh_address.city}, {wh_address.state}")

    # Caja 3 - Vacía
    p.rect(10 + box1_width + box2_width, start_y, box3_width, box_height)





    
def export_pdf_django(request):
    company_id = request.GET.get('company_id')
    order_ids = request.GET.getlist('order_ids[]')

    if not company_id or not order_ids:
        return HttpResponse("Parámetros faltantes", status=400)

    company = get_object_or_404(Company, id=company_id)
    orders = Order.objects.filter(id__in=order_ids)

    if not orders.exists():
        return HttpResponse("No se encontraron órdenes", status=404)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ordenes.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    for order in orders:
        page_number = 1
        draw_pdf_header(p, width, height, company, order, page_number)

        y_position = height - 160

        if order.is_prepaid:
            headers = ["SKU", "Cantidad", "U/M", "Descripción", "No. Art.", "Empaque", "P. Unit", "Total", "Bultos"]
            col_x_positions = [20, 80, 130, 160, 320, 370, 420, 470, 520]
        else:
            headers = ["SKU", "Cantidad", "U/M", "Descripción", "No. Art.", "Empaque", "Bultos"]
            col_x_positions = [20, 80, 150, 200, 420, 470, 530]

        cell_height = 22
        text_vertical_offset = 4

        p.setFont("Helvetica-Bold", 9)
        for idx, header in enumerate(headers):
            next_col_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
            p.rect(col_x_positions[idx], y_position - cell_height, next_col_x - col_x_positions[idx], cell_height)
            cell_center_x = (col_x_positions[idx] + (col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570)) / 2
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
                p.drawString(col_x_positions[idx], y_position, val)

            subtotal += detail.subtotal
            iva += detail.tax_value
            total += detail.total

            y_position -= 18

            if i + 1 == len(details):
                if y_position < 100:
                    p.showPage()
                    page_number += 1
                    draw_pdf_header(p, width, height, company, order, page_number)
                    y_position = height - 160
                    p.setFont("Helvetica-Bold", 9)
                    for idx, header in enumerate(headers):
                        next_col_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
                        p.rect(col_x_positions[idx], y_position - cell_height, next_col_x - col_x_positions[idx], cell_height)
                        p.drawString(col_x_positions[idx] + 2, y_position - cell_height + text_vertical_offset + 4, header)
                    y_position -= 35
                    p.setFont("Helvetica", 8)

            elif y_position < 115:
                p.showPage()
                page_number += 1
                draw_pdf_header(p, width, height, company, order, page_number)
                y_position = height - 160
                p.setFont("Helvetica-Bold", 9)
                for idx, header in enumerate(headers):
                    next_col_x = col_x_positions[idx + 1] if idx + 1 < len(col_x_positions) else 570
                    p.rect(col_x_positions[idx], y_position - cell_height, next_col_x - col_x_positions[idx], cell_height)
                    p.drawString(col_x_positions[idx] + 2, y_position - cell_height + text_vertical_offset + 4, header)
                y_position -= 35
                p.setFont("Helvetica", 8)

        # Mostrar totales solo si es prepago
        if order.is_prepaid:
            if y_position < 100:
                p.showPage()
                page_number += 1
                draw_pdf_header(p, width, height, company, order, page_number)
                y_position = height - 160

            y_position += 5
            p.setFont("Helvetica-Bold", 8)
            p.line(450, y_position + 8, 510, y_position + 8)
            p.drawRightString(450, y_position, "SUBTOTAL:")
            p.drawString(460, y_position, f"${subtotal:,.2f}")
            y_position -= 15
            p.drawRightString(450, y_position, "IVA:")
            p.drawString(460, y_position, f"${iva:,.2f}")
            y_position -= 15
            p.drawRightString(450, y_position, "TOTAL:")
            p.drawString(460, y_position, f"${total:,.2f}")

        # Footer seguro
        first_detail = details.first()
        if first_detail and first_detail.warehouse:
            draw_footer(p, width, company, first_detail.warehouse)
        else:
            draw_footer(
                p,
                width,
                company,
                Warehouse(name="SIN DATOS", company_warehouse_id="N/A", address=company.address)
            )

        p.showPage()

    p.save()
    return response













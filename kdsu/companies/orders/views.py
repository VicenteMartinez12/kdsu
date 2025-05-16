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
    rect_y = height - 100
    rect_width = 130
    rect_height = 60

    if os.path.exists(logo_path):
        p.drawImage(logo_path, margin_left, height - 90, width=100, height=40, mask='auto')

    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 50, company.name)
    p.drawCentredString(width / 2, height - 75, "ORDEN DE MERCANCÍA")
    p.drawCentredString(width / 2, height - 100, order.category)

    p.rect(rect_x, rect_y, rect_width, rect_height)

    p.setFont("Helvetica", 8)
    p.drawString(rect_x + 5, rect_y + rect_height - 12, f"NO.PEDIDO: {order.order_id}")
    p.drawString(rect_x + 5, rect_y + rect_height - 24, f"FECHA: {order.date_ordered.strftime('%d/%m/%Y')}")
    p.drawString(rect_x + 5, rect_y + rect_height - 36, "ENTREGA: ALMACÉN")
    p.drawString(rect_x + 5, rect_y + rect_height - 48, f"PÁGINA: {page_num} de 1")


    p.setFont("Helvetica", 10)
    p.drawString(margin_left, height - 140, f"NO.PROVEEDOR: {order.supplier.company_supplier_id}")
    p.drawString(margin_left + 150, height - 140, f"RAZÓN SOCIAL: {order.supplier.name}")

    
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

    for page_number, order in enumerate(orders, start=1):
        # Dibuja el encabezado para cada orden
        draw_pdf_header(p, width, height, company, order, page_number)

        # Encabezado de tabla
        y_position = height - 130
        p.setFont("Helvetica-Bold", 9)
        headers = ["SKU", "Cantidad", "U/M", "Descripción", "No. Art.", "Empaque", "Bultos", "P. Unit", "Total"]
        col_x_positions = [20, 80, 130, 160, 300, 350, 420, 470, 520]

        for idx, header in enumerate(headers):
            p.drawString(col_x_positions[idx], y_position, header)
        y_position -= 15

        p.setFont("Helvetica", 8)

        for detail in order.orderdetail_set.all():
            bultos = ""
            if detail.product.master_package and detail.product.inner_package:
                if detail.quantity % (detail.product.master_package * detail.product.inner_package) == 0:
                    bultos = str(detail.quantity // (detail.product.master_package * detail.product.inner_package))

            detail_values = [
                detail.product.sku,
                str(detail.quantity),
                detail.product.packing_unit,
                detail.product.description[:30],
                detail.product.mpn,
                f"{detail.product.master_package}/{detail.product.inner_package}",
                bultos,
                f"${detail.cost:.2f}" if order.is_prepaid else "",
                f"${detail.subtotal:.2f}" if order.is_prepaid else ""
            ]

            for idx, val in enumerate(detail_values):
                p.drawString(col_x_positions[idx], y_position, val)

            y_position -= 12

            if y_position < 50:
                p.showPage()
                draw_pdf_header(p, width, height, company, order, page_number)
                y_position = height - 130
                for idx, header in enumerate(headers):
                    p.drawString(col_x_positions[idx], y_position, header)
                y_position -= 15

        # Termina la página y pasa a la siguiente orden
        p.showPage()

    p.save()
    return response
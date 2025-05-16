from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .models import Order, OrderDetail
from .forms import OrderForm, OrderDetailForm
from django.conf import settings
from django.shortcuts import get_object_or_404
import pdfkit
from kdsu.companies import pdf_config
from django.template.loader import render_to_string
from django.http import HttpResponse
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product








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
    
    
    
    
def export_orders_pdf(request):
    company_id = request.GET.get('company_id')
    order_ids = request.GET.getlist('order_ids[]')

    if not company_id or not order_ids:
        return HttpResponse("Faltan parámetros", status=400)

    company = get_object_or_404(Company, id=company_id)
    orders = Order.objects.filter(id__in=order_ids).prefetch_related('orderdetail_set', 'supplier')

    if not orders.exists():
        return HttpResponse("No se encontraron órdenes.", status=404)

    # Renderizar el HTML como string
    html_string = render_to_string('orders/pdf.html', {
        'company': company,
        'orders': orders
    })

    # Ruta de salida (puede ser en memoria o temporal)
    output_path = 'output.pdf'

    # Generar el PDF
    pdfkit.from_string(html_string, output_path, configuration=pdf_config.PDFKIT_CONFIG)

    # Devolver el archivo como respuesta o hacer lo que necesites
    with open(output_path, 'rb') as f:
        pdf_content = f.read()

    response = HttpResponse(pdf_content, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ordenes.pdf"'
    return response

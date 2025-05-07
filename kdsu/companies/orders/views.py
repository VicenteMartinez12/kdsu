from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .models import Order, OrderDetail
from .forms import OrderForm, OrderDetailForm
from django.conf import settings




def plantilla_consultas_view(request):
    return render(request, 'orders/plantilla_consultas.html')


   
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

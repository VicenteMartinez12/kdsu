from django.forms import ModelForm
from .models import Order, OrderDetail

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['company', 'supplier', 'warehouse', 'order_id', 'is_season', 'is_prepaid', 'category', 'status']

class OrderDetailForm(ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'cost', 'quantity', 'tax_rate']

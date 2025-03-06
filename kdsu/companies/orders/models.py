from django.db import models
from decimal import Decimal

# Importing models from the catalogs app
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product

# Order Model
class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20)
    is_season = models.BooleanField(default=False)
    is_prepaid = models.BooleanField(default=False)
    category = models.CharField(max_length=20)
    subtotal = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    tax_value = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    total = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    status = models.CharField(max_length=20)
    

     
        

    def __str__(self):
        return self.order_id

# OrderDetail Model
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=12, decimal_places=4)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax_value = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    total = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal('0.0000'))
    
    def __str__(self):
        return f'{self.product} - {self.order.order_id}'
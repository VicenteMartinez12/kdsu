from django.db import models

from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=100)
    exterior_number = models.CharField(max_length=10)
    interior_number = models.CharField(max_length=10)
    reference = models.CharField(max_length=200)
    postcode = models.CharField(max_length=5)
    neighborhood = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.street} {self.exterior_number}, {self.neighborhood}, {self.city}'
    
class Company(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)
    rfc = models.CharField(max_length=13, validators=[MinLengthValidator(12)])
    image_logo = models.CharField(max_length=250)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Warehouse(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_warehouse_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    
    # Campos para latitud y longitud
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=6, 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name

    # Función estática que regresa un array con los diferentes estados de las direcciones
    @staticmethod
    def get_warehouses_states():
        return Warehouse.objects.values_list('address__state', flat=True).distinct()

    # Función estática que regresa un array con las diferentes ciudades, filtradas por estado
    @staticmethod
    def get_warehouses_cities(state=None):
        if state:
            return Warehouse.objects.filter(address__state=state).values_list('address__city', flat=True).distinct()
        return Warehouse.objects.values_list('address__city', flat=True).distinct()

    # Función estática que regresa las sucursales filtradas por estado y ciudad
    @staticmethod
    def get_warehouses_locations(state=None, city=None):
        if state and not city:
            raise ValidationError("Si se proporciona una ciudad, también debe proporcionarse un estado.")
        
        # Filtrar por estado y ciudad si se pasan ambos parámetros
        queryset = Warehouse.objects.all()
        
        if state:
            queryset = queryset.filter(address__state=state)
        if city:
            queryset = queryset.filter(address__city=city)

        return queryset



class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    company_supplier_id = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=20)
    rfc = models.CharField(max_length=13, validators=[MinLengthValidator(12)])
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sku = models.CharField(max_length=50)
    mpn = models.CharField(max_length=50)
    description = models.TextField()
    packing_unit = models.CharField(max_length=50)
    master_package = models.IntegerField()
    inner_package = models.IntegerField()

    def __str__(self):
        return self.sku

     
    
    
    





from ninja import ModelSchema, Schema
from .models import Company, Warehouse, Supplier, Product

# Schemas basados en ModelSchema
class CompanySchema(ModelSchema):
    class Meta:
        model = Company
        fields = "__all__"

class WarehouseSchema(ModelSchema):
    class Meta:
        model = Warehouse
        fields = "__all__"

class SupplierSchema(ModelSchema):
    class Meta:
        model = Supplier
        fields = "__all__"

class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        fields = "__all__"

# Schema para manejar errores 404
class NotFoundSchema(Schema):
    message: str

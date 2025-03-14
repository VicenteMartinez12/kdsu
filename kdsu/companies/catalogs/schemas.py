from ninja import ModelSchema, Schema
from .models import Company, Warehouse, Supplier, Product, Address

# Schemas basados en ModelSchema

class AddressSchema(ModelSchema):
    class Meta:
        model = Address
        fields = "__all__"


class CompanySchema(ModelSchema):
    address: AddressSchema 
    class Meta:
        model = Company
        fields = "__all__"
        
        

class WarehouseSchema(ModelSchema):
    address: AddressSchema 
    class Meta:
        model = Warehouse
        fields = "__all__"

class SupplierSchema(ModelSchema):
    address: AddressSchema
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

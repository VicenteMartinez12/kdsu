from ninja import NinjaAPI
from .schemas import CompanySchema, WarehouseSchema, SupplierSchema, ProductSchema, NotFoundSchema, AddressSchema
from .models import Company, Warehouse, Supplier, Product
from typing import List, Optional, Union

api = NinjaAPI(urls_namespace="catalogs_api")


# Endpoint de Company
@api.get("/companies", response=Union[List[CompanySchema], NotFoundSchema])
def get_companies(request, name: Optional[str] = None):
    queryset = Company.objects.select_related("address").all()
    if name:
        queryset = queryset.filter(name__icontains=name) | queryset.filter(short_name__icontains=name)
    if not queryset.exists():
        return {"message": "No se encontró ninguna compañía"}
    return queryset

@api.get("/companies/{company_id}", response={200: CompanySchema, 404: NotFoundSchema})
def get_company(request, company_id: int):
    try:
        company = Company.objects.select_related("address").get(id=company_id)
        return 200, company
    except Company.DoesNotExist:
        return 404, {"message": "No se encontró ninguna compañía"}

# Endpoint de Warehouse
@api.get("/warehouses", response=Union[List[WarehouseSchema], NotFoundSchema])
def get_warehouses(request, company: Optional[int] = None, company_warehouse_id: Optional[str] = None):
    queryset = Warehouse.objects.all()
    if company:
        queryset = queryset.filter(company_id=company)
    if company_warehouse_id and company:
        queryset = queryset.filter(company_warehouse_id=company_warehouse_id, company_id=company)
    if company_warehouse_id:
        return {"message": "Se necesita tambien el parametro de compañia"}
    if not queryset.exists():
        return {"message": "No se encontró ningún almacén"}
    return queryset

@api.get("/warehouses/{warehouse_id}", response={200: WarehouseSchema, 404: NotFoundSchema})
def get_warehouse(request, warehouse_id: int):
    try:
        return 200, Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return 404, {"message": "No se encontró ningún almacén"}


# Endpoint de Supplier
@api.get("/suppliers", response=Union[List[SupplierSchema], NotFoundSchema])
def get_suppliers(request, company: Optional[int] = None, name: Optional[str] = None, rfc: Optional[str] = None):
    queryset = Supplier.objects.all()
    if company:
        queryset = queryset.filter(company_id=company)
    if name:
        queryset = queryset.filter(name__icontains=name) | queryset.filter(short_name__icontains=name)
    if rfc:
        queryset = queryset.filter(rfc=rfc)
    if not queryset.exists():
        return {"message": "No se encontró ningún proveedor"}
    return queryset

@api.get("/suppliers/{supplier_id}", response={200: SupplierSchema, 404: NotFoundSchema})
def get_supplier(request, supplier_id: int):
    try:
        return 200, Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
        return 404, {"message": "No se encontró ningún proveedor"}


# Endpoint de Product
@api.get("/products", response=Union[List[ProductSchema], NotFoundSchema])
def get_products(request, supplier: Optional[int] = None):
    queryset = Product.objects.all()
    if supplier:
        queryset = queryset.filter(supplier_id=supplier)
    if not queryset.exists():
        return {"message": "No se encontraron productos"}
    return queryset

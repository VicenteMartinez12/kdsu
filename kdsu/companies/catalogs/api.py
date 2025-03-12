from ninja import NinjaAPI
from .schemas import CompanySchema, WarehouseSchema, SupplierSchema, ProductSchema, NotFoundSchema
from .models import Company, Warehouse, Supplier, Product
from typing import List, Optional, Union

api = NinjaAPI(urls_namespace="catalogs_api")

# Endpoints de Company con ? para búsqueda y manejo de errores
@api.get("/companies", response=Union[List[CompanySchema], NotFoundSchema])
def get_companies(request, company_id: Optional[int] = None, name: Optional[str] = None):
    queryset = Company.objects.all()
    if company_id:
        queryset = queryset.filter(id=company_id)
    if name:
        queryset = queryset.filter(name__icontains=name) | queryset.filter(short_name__icontains=name)
    if not queryset.exists():
        return {"message": "No se encontró ninguna compañía"}
    return queryset

# Endpoints de Warehouse con ? para búsqueda y manejo de errores
@api.get("/warehouses", response=Union[List[WarehouseSchema], NotFoundSchema])
def get_warehouses(request, warehouse_id: Optional[int] = None, company: Optional[int] = None, company_warehouse_id: Optional[str] = None):
    queryset = Warehouse.objects.all()
    if warehouse_id:
        queryset = queryset.filter(id=warehouse_id)
    if company:
        queryset = queryset.filter(company_id=company)
    if company_warehouse_id:
        queryset = queryset.filter(company_warehouse_id=company_warehouse_id)
    if not queryset.exists():
        return {"message": "No se encontró ningún almacén"}
    return queryset

# Endpoints de Supplier con ? para búsqueda y manejo de errores
@api.get("/suppliers", response=Union[List[SupplierSchema], NotFoundSchema])
def get_suppliers(request, supplier_id: Optional[int] = None, company: Optional[int] = None, name: Optional[str] = None, rfc: Optional[str] = None):
    queryset = Supplier.objects.all()
    if supplier_id:
        queryset = queryset.filter(id=supplier_id)
    if company:
        queryset = queryset.filter(company_id=company)
    if name:
        queryset = queryset.filter(name__icontains=name) | queryset.filter(short_name__icontains=name)
    if rfc:
        queryset = queryset.filter(rfc=rfc)
    if not queryset.exists():
        return {"message": "No se encontró ningún proveedor"}
    return queryset

# Endpoints de Product con ? para búsqueda y manejo de errores
@api.get("/products", response=Union[List[ProductSchema], NotFoundSchema])
def get_products(request, supplier: Optional[int] = None):
    queryset = Product.objects.all()
    if supplier:
        queryset = queryset.filter(supplier_id=supplier)
    if not queryset.exists():
        return {"message": "No se encontraron productos"}
    return queryset
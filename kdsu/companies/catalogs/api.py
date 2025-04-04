from ninja import NinjaAPI
from .schemas import CompanySchema, WarehouseSchema, SupplierSchema, ProductSchema, NotFoundSchema, AddressSchema
from .models import Company, Warehouse, Supplier, Product
from typing import List, Optional, Union
from ninja import Router

catalogs_router = Router(tags=["Catálogos"])


# Endpoint de Company
@catalogs_router.get("/companies", response=Union[List[CompanySchema], NotFoundSchema], summary="Carga los registros de compañias",  description="Este endpoint permite cargar registros de las compañias y se puede filtrar por nombre")
def get_companies(request, name: Optional[str] = None):
    queryset = Company.objects.select_related("address").all()
    if name:
        queryset = queryset.filter(name__icontains=name) | queryset.filter(short_name__icontains=name)
    if not queryset.exists():
        return {"message": "No se encontró ninguna compañía"}
    return queryset

@catalogs_router.get("/companies/{company_id}", response={200: CompanySchema, 404: NotFoundSchema}, summary="Carga los registros de compañias filtrado por id",  description="Este endpoint permite cargar registros de las compañias y se puede filtrar por el id")
def get_company(request, company_id: int):
    try:
        company = Company.objects.select_related("address").get(id=company_id)
        return 200, company
    except Company.DoesNotExist:
        return 404, {"message": "No se encontró ninguna compañía"}

# Endpoint de Warehouse
@catalogs_router.get("/warehouses", response=Union[List[WarehouseSchema], NotFoundSchema], summary="Carga los registros de almacenes",  description="Este endpoint permite cargar registros de los almacenes y se puede filtrar almacenes de una compañia")
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

@catalogs_router.get("/warehouses/{warehouse_id}", response={200: WarehouseSchema, 404: NotFoundSchema},summary="Carga los registros de almacenes",  description="Este endpoint permite cargar registros de los almacenes y se puede filtrar por id" )
def get_warehouse(request, warehouse_id: int):
    try:
        return 200, Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return 404, {"message": "No se encontró ningún almacén"}


# Endpoint de Supplier
@catalogs_router.get("/suppliers", response=Union[List[SupplierSchema], NotFoundSchema], summary="Carga los registros de los proveedores",  description="Este endpoint permite cargar registros de los proveedores y se puede filtrar id de la compañia, nombre y rfc")
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

@catalogs_router.get("/suppliers/{supplier_id}", response={200: SupplierSchema, 404: NotFoundSchema}, summary="Carga los registros de los proveedores",  description="Este endpoint permite cargar registros de los proveedores y se puede filtrar por id")
def get_supplier(request, supplier_id: int):
    try:
        return 200, Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
        return 404, {"message": "No se encontró ningún proveedor"}


# Endpoint de Product
@catalogs_router.get("/products", response=Union[List[ProductSchema], NotFoundSchema], summary="Carga los registros de los proveedores",  description="Este endpoint permite cargar registros de los productos y se puede filtrar por proveedor")
def get_products(request, supplier: Optional[int] = None):
    queryset = Product.objects.all()
    if supplier:
        queryset = queryset.filter(supplier_id=supplier)
    if not queryset.exists():
        return {"message": "No se encontraron productos"}
    return queryset

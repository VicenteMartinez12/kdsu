# api.py - Contiene la configuración de NinjaAPI y los endpoints
from ninja import NinjaAPI
from .schemas import CompanySchema, WarehouseSchema, SupplierSchema, ProductSchema, NotFoundSchema
from .models import Company, Warehouse, Supplier, Product
from typing import List, Optional

api = NinjaAPI(urls_namespace="catalogs_api")

# Endpoints de Company
@api.get("/companies", response=List[CompanySchema])
def get_companies(request, name: Optional[str] = None):
    if name:
        return Company.objects.filter(name__icontains=name) | Company.objects.filter(short_name__icontains=name)
    return Company.objects.all()

@api.get("/companies/{company_id}", response={200: CompanySchema, 404: NotFoundSchema})
def get_company(request, company_id: int):
    try:
        return 200, Company.objects.get(id=company_id)
    except Company.DoesNotExist:
        return 404, {"message": "Company not found"}

# Endpoints de Warehouse
@api.get("/warehouses", response=List[WarehouseSchema])
def get_warehouses(request, company: Optional[int] = None, company_warehouse_id: Optional[str] = None):
    queryset = Warehouse.objects.all()
    if company:
        queryset = queryset.filter(company_id=company)
    if company_warehouse_id:
        queryset = queryset.filter(company_warehouse_id=company_warehouse_id)
    return queryset

@api.get("/warehouses/{warehouse_id}", response={200: WarehouseSchema, 404: NotFoundSchema})
def get_warehouse(request, warehouse_id: int):
    try:
        return 200, Warehouse.objects.get(id=warehouse_id)
    except Warehouse.DoesNotExist:
        return 404, {"message": "Warehouse not found"}

# Endpoints de Supplier
@api.get("/suppliers", response=List[SupplierSchema])
def get_suppliers(request, company: Optional[int] = None, name: Optional[str] = None, rfc: Optional[str] = None):
    queryset = Supplier.objects.all()
    if company:
        queryset = queryset.filter(company_id=company)
    if name:
        queryset = queryset.filter(name__icontains=name) | queryset.filter(short_name__icontains=name)
    if rfc:
        queryset = queryset.filter(rfc=rfc)
    return queryset

@api.get("/suppliers/{supplier_id}", response={200: SupplierSchema, 404: NotFoundSchema})
def get_supplier(request, supplier_id: int):
    try:
        return 200, Supplier.objects.get(id=supplier_id)
    except Supplier.DoesNotExist:
        return 404, {"message": "Supplier not found"}

# Endpoints de Product
@api.get("/products", response=List[ProductSchema])
def get_products(request, supplier: Optional[int] = None):
    queryset = Product.objects.all()
    if supplier:
        queryset = queryset.filter(supplier_id=supplier)
    return queryset
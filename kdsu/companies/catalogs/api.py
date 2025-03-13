from ninja import NinjaAPI
from .schemas import CompanySchema, WarehouseSchema, SupplierSchema, ProductSchema, NotFoundSchema
from .models import Company, Warehouse, Supplier, Product
from typing import List, Optional, Union

api = NinjaAPI(urls_namespace="catalogs_api")

# Endpoints de Company con búsqueda en name y short_name
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

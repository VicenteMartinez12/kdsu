from ninja import NinjaAPI
from kdsu.companies.catalogs.api import catalogs_router
from kdsu.companies.orders.api import orders_router
from django.http import JsonResponse

api = NinjaAPI(
    title="KDSU API",
    version="1.0",
    description="",

  

)

@api.exception_handler(Exception)
def global_exception_handler(request, exc):
    return JsonResponse({"error": str(exc)}, status=400)

api.add_router("/catalogs", catalogs_router)
api.add_router("/orders", orders_router)



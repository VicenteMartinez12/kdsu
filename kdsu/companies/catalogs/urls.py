from django.urls import path
from .api import api  # Importar la API definida en `api.py`

urlpatterns = [
    path("api/v1/", api.urls),  # Esto expone los endpoints en `/api/v1/`
]

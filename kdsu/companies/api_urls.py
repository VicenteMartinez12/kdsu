from django.urls import path
from .main_api import api  

urlpatterns = [
    path("v1/", api.urls),
]

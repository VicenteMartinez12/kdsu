from django.urls import path
from .views import CustomSwaggerView

urlpatterns = [
    path("api/v1/docs", CustomSwaggerView.as_view(), name="custom-docs")
]

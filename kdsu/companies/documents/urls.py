from django.urls import path
from .views import DocTestView, factura_test_view

urlpatterns = [
    path('prueba/', DocTestView.as_view(), name='prueba'),
    path('cfdi-test/', factura_test_view, name='cfdi_test'),
]

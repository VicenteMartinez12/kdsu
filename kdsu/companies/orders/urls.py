from django.urls import path
from .views import OrderTestView

urlpatterns = [
    path('prueba/', OrderTestView.as_view(), name='prueba'),
]
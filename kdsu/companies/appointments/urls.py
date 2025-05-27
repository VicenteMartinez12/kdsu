from django.urls import path
from .views import AppTestView

urlpatterns = [
    path('prueba/', AppTestView.as_view(), name='prueba'),
]

from django.urls import path
from .views import OrderTestView,plantilla_consultas_view,index2

urlpatterns = [
 
    path('prueba/', OrderTestView.as_view(), name='prueba'),
    path('plantilla_consultas/',plantilla_consultas_view, name='plantilla_consultas'),
    path('',index2, name='index2')
]
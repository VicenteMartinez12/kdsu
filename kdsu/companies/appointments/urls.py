from django.urls import path
from .views import AppTestView
from .views import CalendarTest
from .views import calendario
from . import views

urlpatterns = [
    path('prueba/', AppTestView.as_view(), name='prueba'),
    path('cal/', CalendarTest.as_view(), name='cal'),
    path('calendario/', calendario, name='calendario'),
    path('orders_to_be_appointed/', views.orders_to_be_appointed,
         name='orders_to_be_appointed'),
]

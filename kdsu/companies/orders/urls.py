from django.urls import path
from .views import OrderTestView,plantilla_consultas_view,index2,obtener_detalles_orden,plantilla_pdf_view,export_pdf,export_xml,export_xml_excel

urlpatterns = [
 
    path('prueba/', OrderTestView.as_view(), name='prueba'),
    path('plantilla_consultas/',plantilla_consultas_view, name='plantilla_consultas'),
    path('',index2, name='index2'),
    path('detalle_orden/<int:order_id>/', obtener_detalles_orden, name='detalle_orden'),
     path('plantilla_pdf/',plantilla_pdf_view, name='plantilla_pdf'),
   path('export_pdf/', export_pdf, name='export_pdf'),
   path('export_xml/', export_xml, name='export_xml'),
  path('export_xml_excel/', export_xml_excel, name='export_xml_excel'),


]
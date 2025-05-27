from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core import serializers
# Create your views here.

from .models import Appointment, AppointmentCategory, AppointmentDocuments, TransportationCategory, LoadCategory
from kdsu.companies.documents.models import Company, Supplier
from django.contrib.auth.models import User

class AppTestView(View):
    def get(self, request, *args, **kwargs):
        _cia = Company.objects.filter(short_name='TONY')
        _supplier = Supplier.objects.filter(short_name='NORMA')
        """acat = AppointmentCategory()
        tcat = TransportationCategory()
        lcat = LoadCategory()
        usr = User() """
        appointmento = Appointment.objects.filter(
            company__in=_cia).filter(supplier__in=_supplier)
        docs = AppointmentDocuments.objects.filter(
            appointment__in=appointmento)

        validated = Appointment.validate_documents(appointmento, docs)
        #print(docs)
        return JsonResponse({'message': 'oks', 'resp': validated})
        #return JsonResponse({'message': 'oks', 'resp': list(docs.values())})
        return JsonResponse({'message': 'oks', 'resp': validated})

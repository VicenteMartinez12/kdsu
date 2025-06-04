from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core import serializers
# Create your views here.
from datetime import datetime, timedelta
from django.core.serializers import serialize
from kdsu.companies.documents.models import Documento, Desglose
from django.core.serializers.json import DjangoJSONEncoder
import json
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
        # print(docs)
        return JsonResponse({'message': 'oks', 'resp': validated})
        # return JsonResponse({'message': 'oks', 'resp': list(docs.values())})
        return JsonResponse({'message': 'oks', 'resp': validated})


class CalendarTest(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cal.html')


def calendario(request):
    wd = datetime.today().weekday()
    start = datetime.today().date() - timedelta(days=(datetime.today().weekday()+1))
    end = get_date_n_weeks_from_now(3) + timedelta(days=(6-(wd+1)))
    apps = Appointment.objects.filter(requested_date__range=(start, end)).order_by('requested_date')
    data  = serializers.serialize('json', apps)
   # Step 1: parse string into Python objects
    parsed = json.loads(data)
    # Step 2: extract only the "fields" part
    fields_only = [item['fields'] for item in parsed]
    # Step 3: optionally re-serialize to JSON for frontend
    appointments_json = json.dumps(fields_only)
    loadCats = LoadCategory.objects.all()
    transCats = TransportationCategory.objects.all()
    #print()
    return render(request, 'calendario.html',
    {'appointments_json': appointments_json,
     'loadCats': loadCats,
     'transCats': transCats})


##get list
def orders_to_be_appointed(request):
    type = request.GET.get('type')
    #model query with type
    data = ()
    return JsonResponse({'data': ()})

##post
def storeAppointment(request):
    bresult = False
    if request.method == "POST":
        try:
            data = json.loads(request.body)




            ##################################################################
            bills = data['FACTURAS']
            for bill in bills:
                #update every doc
                 AppointmentDocuments.objects.filter(folio=bill.folio).update(
                    packages=bill.totalBultos,
                    weight=bill.totalPeso
                )
            bresult = True
            ###################################################################
            return JsonResponse({'result':bresult})
        except json.JSONDecodeError:
            return JsonResponse({'result': bresult}, status=400)
    return

def get_date_n_weeks_from_now(n):
    """
    Calculates the date n weeks from the current date.

    Args:
        n: The number of weeks to add (can be positive or negative).

    Returns:
        A datetime.date object representing the calculated date.
    """
    today = datetime.today().date()
    delta = timedelta(weeks=n)
    future_date = today + delta
    return future_date

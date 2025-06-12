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
from .models import Appointment, AppointmentCategory, AppointmentDocuments, AppointmentConfirmation, Platform, APPOINTMENT_STATUSES, TransportationCategory, LoadCategory
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
    apps = Appointment.objects.filter(
        requested_date__range=(start, end)).order_by('requested_date')
    data = serializers.serialize('json', apps)
   # Step 1: parse string into Python objects
    parsed = json.loads(data)
    # Step 2: extract only the "fields" part
    fields_only = [item['fields'] for item in parsed]
    # Step 3: optionally re-serialize to JSON for frontend
    appointments_json = json.dumps(fields_only)
    loadCats = LoadCategory.objects.all()
    transCats = TransportationCategory.objects.all()
    appCats = AppointmentCategory.objects.filter(status='activo')
    # print()
    return render(request, 'calendario.html',
                  {'appointments_json': appointments_json,
                   'loadCats': loadCats,
                   'transCats': transCats,
                   'appCats': appCats})


# get list
def orders_to_be_appointed(request):
    docs = Documento.objects.all()
    return JsonResponse({'docs_json':  list(docs.values())})

# post
def orders_by_date(request):
    if request.method == "POST":
     try:
        data = json.loads(request.body)
        date_string = data['date']  # Example date string
        date_object = datetime.strptime(date_string, "%Y-%m-%d").date()
        docs = Appointment.objects.filter(requested_date=date_object)
        result = [
            {
                "id": doc.id,
                "company_id": Company.objects.get(id=doc.company_id).short_name,
                "volume": doc.volume,
                "weight": doc.weight,
                "total_packages": doc.total_packages,
                "status": doc.status,
                "appointment_category_id": AppointmentCategory.objects.get(id=doc.appointment_category_id).name,
            }
            for doc in docs
        ]
     except json.JSONDecodeError:
         return JsonResponse({'docs_json':  list(())})
    return JsonResponse({'docs_json':  result})

def orders_detail_by_appointment(request):
    if request.method == "GET":
     try:
        ##adoc
        adocs = Appointment.objects.get(id=1).with_docs()
        ##iterate and get docs
        docs = [
            {
                "cia":  Company.objects.get(id=adoc.document.compania_id).short_name,
                "supplier":  Supplier.objects.get(id=adoc.document.proveedor_id).short_name,
                "bill":  adoc.document.folio,
                "packages":   adoc.document.totalBultos,
                "date":  adoc.document.fecha.date()
            }
              for adoc in adocs
        ]
        ##map
     except json.JSONDecodeError:
            return JsonResponse({'docs_json':  list(())})
    return JsonResponse({'docs_json':  docs})

def storeAppointment(request):
    bresult = False
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ##################################################################
            now = datetime.now()
            newApp = Appointment(
                company=Company.objects.get(id=1),
                supplier=Supplier.objects.get(id=1),  # data[0]['PROVEEDOR']
                appointment_category=AppointmentCategory.objects.get(
                    id=data['ID_TIPOCITA']),
                transportation_category=TransportationCategory.objects.get(
                    id=data['ID_TRANSPORTE']),
                load_category=LoadCategory.objects.get(id=data['ID_CARGA']),
                request_user=User.objects.get(id=1),
                volume=data['VOLUMEN'],
                weight=data['PESO'],
                total_packages=data['BULTOS'],
                total_pallets=data['PALLETS'],
                carrier_name=data['TRANSPORTISTA'],
                carrier_license_plates=data['PLACAS'],
                carrier_driver=data['CHOFER'],
                status=APPOINTMENT_STATUSES.get('SOLICITADA')
            )
            newApp.save()
            ##################################################################
            ac = AppointmentConfirmation(
                appointment=newApp,
                assigned_date=now,
                timespan=0,
                platform=Platform.objects.get(id=1),
                confirmation_date=now,
                confirming_user=User.objects.get(id=1)
            )
            ac.save()
            ##################################################################
            """  print(repr(Documento.objects.filter(folio="FAB82784")[0] ))
            print("eso tilin") """
            bills = data['FACTURAS']
            for bill in bills:
                # update every doc

                ad = AppointmentDocuments(
                    appointment = newApp,
                    document=Documento.objects.filter(folio="FAB82784")[0],
                    packages = bill['BULTOSXCITA'],
                    weight = bill['PESOXCITA'],
                    delivered_packages = 0,
                    rejected_packages = 0
                )
                ad.save()
            bresult = True
            ###################################################################
            return JsonResponse({'result': bresult})
        except json.JSONDecodeError:
            return JsonResponse({'result': bresult}, status=400)
    return JsonResponse({'result': bresult}, status=400)


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

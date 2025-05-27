from django.db import models


from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.db.models import Value
from django.db.models.functions import Concat
from decimal import Decimal
from kdsu.companies.catalogs.models import Company, Supplier, Warehouse, Product
from django.contrib.auth.models import User
from kdsu.companies.documents.models import Documento, Desglose
from django.db.models import Q
STATUSES = (
 ( "ACTIVO", "activo"),
    ("INACTIVO", "inactivo")
)



class AppointmentCategory(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUSES)


class TransportationCategory(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUSES)


class LoadCategory(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUSES)


PLATFORM_STATUSES = (
   ("ENTRADA", "entrada"),
   ( "SALIDA", "salida")
)


class Platform(models.Model):
    name = models.CharField(max_length=100)
    operation = models.CharField(
        max_length=30,
        choices=PLATFORM_STATUSES)
    is_virtual = models.BooleanField()
    status = models.CharField(
        max_length=10,
        choices=STATUSES)


APPOINTMENT_STATUSES = {
    "CAPTURA": "en captura",
    "SOLICITADA": "solicitada",
    "CONFIRMADA": "confirmada",
    "ENTREGADA": "entregada",
    "CANCELADA": "cancelada",
    "RECHAZADA": "rechazada"
}


class Appointment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    appointment_category = models.ForeignKey(
        AppointmentCategory, on_delete=models.CASCADE)
    transportation_category = models.ForeignKey(
        TransportationCategory, on_delete=models.CASCADE)
    load_category = models.ForeignKey(LoadCategory, on_delete=models.CASCADE)
    requested_date = models.DateTimeField(auto_now_add=True)
    request_user = models.ForeignKey(User, on_delete=models.CASCADE)
    volume = models.IntegerField()
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('0.00'))
    total_packages = models.IntegerField()
    total_pallets = models.IntegerField()
    carrier_name = models.CharField(max_length=100)
    carrier_license_plates = models.CharField(max_length=100)
    carrier_driver = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=APPOINTMENT_STATUSES)

    def validate_documents(_appointment, appointment_documents):
        resp = {
            "valido": True,
            "validaciones": []
        }
        _appointment = _appointment[0]
        ciaO = Company.objects.get(short_name=_appointment.company.short_name)
        supplierO = Supplier.objects.get(
            company_supplier_id=_appointment.supplier.company_supplier_id)

        for doc in appointment_documents:
            tdoc = doc.document
            folio = tdoc.folio
            """ docs = Documento.objects.filter(
                compania=ciaO, supplier=supplierO) """
            # Todos los documents deben pertenecer al mismo Company y supplier del appointment
            hasSameApp = doc.appointment.company == ciaO
            hasSameSupplier = doc.appointment.supplier == supplierO

            if not hasSameApp or not hasSameSupplier:
                resp['valido'] = False
                resp['validaciones'].append(
                    {folio: f"El documento {folio} no pertenece a la misma compañía y proveedor"}
                )

        # Todos los documents deben tener información de desglose
        for doc in appointment_documents:
            tdoc = doc.document
            folio = tdoc.folio
            if not Desglose.objects.filter(documento=tdoc).exists():
                resp['valido'] = False
                resp['validaciones'].append(
                    {folio: f"El documento {folio} no tiene información de desglose"}
                )

        # Ningún document debe estar relacionado en otro appointment(diferente al que se recibe como parámetro)
        # que tenga estatus “en captura”, “solicitada” o “confirmada”
        for doc in appointment_documents:
            tdoc = doc.document
            folio = tdoc.folio
            hasValidStatus = Appointment.objects.filter(
                ~Q(id=_appointment.id),
                ~Q(status__in=["en captura", "solicitada", "confirmada"]),
            ).exists()
            existsOnAD = AppointmentDocuments.objects.filter(
                document=tdoc).exists()
            print(hasValidStatus, existsOnAD)
            if  hasValidStatus and  existsOnAD:
                resp['valido'] = False
                resp['validaciones'].append(
                    {folio: f"El documento {folio} está en otra cita pendiente de entrega", })



        # Buscar todos los appointment_document que tengan el mismo documento y
        #  que pertenezcan a un appointment con estatus “entregada”
        # la suma total de “delivered_packages” de todos los resultados más los packages del
        # appointment_document actual no deben ser mayores a los “bultos” (packages)
        #  del document original.
        for doc in appointment_documents:
            tdoc = doc.document
            folio = tdoc.folio
            total_delivered = sum(
                ad.delivered_packages for ad in appointment_documents.all()
                if ad.appointment.status == "ENTREGADA"
            )
            if total_delivered + doc.delivered_packages > doc.packages:
                resp['valido'] = False
                resp['validaciones'].append(
                    {folio: f"Se programaron para entrega más bultos de los pendientes por recibir para el documento {folio}"})

        return resp


class AppointmentDocuments(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    document = models.ForeignKey(Documento, on_delete=models.CASCADE)
    packages = models.IntegerField()
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('0.00'))
    delivered_packages = models.IntegerField()
    rejected_packages = models.IntegerField()

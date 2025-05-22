from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
# Create your views here.

from .models import Factura

from .forms import UploadXMLForm
import tempfile, os


class DocTestView(View):
    def get(self, request, *args, **kwargs):
        doc = Factura.validar_cfdi(
            'kdsu/companies/documents/schemas/A59404.xml')
        return JsonResponse({'message': 'oks', 'resp': doc})


def factura_test_view(request):
    facturas = Factura.objects.all()
    load_result = None

    if request.method == 'POST':
        form = UploadXMLForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Ruta directa del servidor
            ruta_manual = form.cleaned_data.get('ruta_directa')

            if ruta_manual:
                if os.path.exists(ruta_manual):
                    load_result = Factura.cargar_cfdi(ruta_manual)
                else:
                    load_result = {'error': 'La ruta proporcionada no existe en el servidor.'}

            # 2. Carga de archivo manual (form upload)
            elif form.cleaned_data.get('xml_file'):
                xml_file = form.cleaned_data['xml_file']
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    for chunk in xml_file.chunks():
                        tmp.write(chunk)
                    tmp_path = tmp.name
                load_result = Factura.cargar_cfdi(tmp_path)

    else:
        form = UploadXMLForm()

    return render(request, 'cfdi/prueba.html', {
        'facturas': facturas,
        'form': form,
        'load_result': load_result,
    })
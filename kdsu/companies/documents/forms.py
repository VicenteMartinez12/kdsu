from django import forms

class UploadXMLForm(forms.Form):
    xml_file = forms.FileField(required=False, label='Selecciona un archivo XML')
    ruta_directa = forms.CharField(required=False, label='O ingresa la ruta directa del XML en el servidor')

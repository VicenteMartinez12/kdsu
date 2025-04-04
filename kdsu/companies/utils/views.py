# kdsu/companies/utils/views.py

from django.views.generic import TemplateView

class CustomSwaggerView(TemplateView):
    template_name = "docs.html" 

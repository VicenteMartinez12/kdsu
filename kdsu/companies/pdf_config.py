import os
import pdfkit

# Ruta absoluta al ejecutable wkhtmltopdf.exe
WKHTMLTOPDF_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'bin', 'wkhtmltopdf.exe'))


# Configuración de pdfkit
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

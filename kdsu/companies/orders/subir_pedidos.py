

import requests

url = "http://127.0.0.1:8000/api/v1/orders/upload"
file_path = "kdsu/companies/orders/ejemplos/pruebaApi.csv"

with open(file_path, 'rb') as f:
    files = {'file': (file_path, f)}
    response = requests.post(url, files=files)

print("✅ Status:", response.status_code)
print("📄 Raw Response Text:", response.text)  # Muestra todo, aunque no sea JSON

try:
    print( "JSON:", response.json())
except Exception as e:
    print("No se pudo decodificar como JSON:", e)

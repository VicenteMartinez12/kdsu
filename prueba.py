from kdsu.companies.utils.csv import read_csv

# Define la ruta del archivo CSV
file_path = "kdsu/companies/utils/ejemplos/Inventory_v2.csv"

# Llamar a la función y manejar posibles errores
try:
    data = read_csv(file_path)
    print("Datos cargados correctamente:")
    for row in data:
        print(row)
except FileNotFoundError as e:
    print(f"Error: {e}")









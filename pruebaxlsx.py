from kdsu.companies.utils.xlsx import read_xlsx

file_path = "kdsu/companies/utils/ejemplos/pruebaxlsx.xlsx"

try:
    data = read_xlsx(file_path)
    print("Datos cargados:")
    for row in data:
        print(row)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}")

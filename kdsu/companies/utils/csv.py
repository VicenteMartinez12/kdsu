import csv
import os

def read_csv(file_path: str):
    """
    Lee un archivo CSV y lo convierte en una lista de diccionarios.
    :param file_path: Ruta del archivo CSV
    :return: Lista de diccionarios con los datos del CSV
    :raises FileNotFoundError: Si el archivo no existe
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))

    return data

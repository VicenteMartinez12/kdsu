import csv
import os
import chardet

def detect_encoding(file_path):
   
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read(100000))  
        return result['encoding']

def read_csv(file_path: str):
 
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo '{file_path}' no existe.")
    
    encoding = detect_encoding(file_path)  # Detecta la codificación antes de leer
    print(f"Codificación detectada: {encoding}")
    
    data = []
    with open(file_path, mode='r', encoding=encoding) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))
    
    return data
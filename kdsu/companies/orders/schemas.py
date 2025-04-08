from ninja import Schema
from typing import List

class Producto(Schema):
    sucursalDestino: str
    clave: str
    numeroArticulo: str
    descripcion: str
    costoUnitario: float
    cantidad: int
    porcentajeImpuesto: float
    unidad: str
    empaqueMaster: int
    empaqueInner: int
    esMercanciaSinCargo: bool

class Orden(Schema):
    compania: str
    orden: str  # Asegúrate de que el campo "orden" sea tipo `str` si en tu ejemplo lo estás pasando como un string
    fechaPedido: str  # El formato de fecha también debe coincidir con lo que esperas
    claveProveedor: str
    esTemporada: bool
    esPagoAnticipado: bool
    tipo: str
    productos: List[Producto]

    class Config:
        # Definimos el ejemplo JSON que proporcionaste
        schema_extra = {
            "example": {
                "ordenes": [
                    {
                        "compania": "TONY",
                        "orden": "47",
                        "fechaPedido": "2025-03-24 09:43:20",
                        "claveProveedor": "NORMA1",
                        "esTemporada": True,
                        "esPagoAnticipado": True,
                        "tipo": "normal",
                        "productos": [
                            {
                                "sucursalDestino": "suc299",
                                "clave": "SKU12345",
                                "numeroArticulo": "MPN12345",
                                "descripcion": "Libreta",
                                "costoUnitario": 0,
                                "cantidad": 100,
                                "porcentajeImpuesto": 16.00,
                                "unidad": "Caja",
                                "empaqueMaster": 100,
                                "empaqueInner": 10,
                                "esMercanciaSinCargo": True
                            },
                            {
                                "sucursalDestino": "suc299",
                                "clave": "SKU67890",
                                "numeroArticulo": "MPN67890",
                                "descripcion": "Pluma",
                                "costoUnitario": 32.80,
                                "cantidad": 50,
                                "porcentajeImpuesto": 0.00,
                                "unidad": "Caja",
                                "empaqueMaster": 50,
                                "empaqueInner": 5,
                                "esMercanciaSinCargo": False
                            }
                        ]
                    }
                ]
            }
        }

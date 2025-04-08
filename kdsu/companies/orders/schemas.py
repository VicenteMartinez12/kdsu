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

    
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
    orden: str 
    fechaPedido: str  
    claveProveedor: str
    esTemporada: bool
    esPagoAnticipado: bool
    tipo: str
    productos: List[Producto]

    
from typing import Any, Dict, List, Optional, Union
from groovindb.src.client import ModelDelegate

class PrismaLikeClient:
    clientes: ModelDelegate
    cobranzas: ModelDelegate
    empresas: ModelDelegate
    facturas_a_cobrar: ModelDelegate
    facturas_a_pagar: ModelDelegate
    movimientos: ModelDelegate
    pagos: ModelDelegate
    proveedores: ModelDelegate
    tesoreria: ModelDelegate
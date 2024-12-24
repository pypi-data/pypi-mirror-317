"""
Configuración del sistema de logging para GroovinDB.
"""
import logging
from typing import Dict, Any

def configure_logging(config: Dict[str, Any]) -> None:
    """
    Configura el sistema de logging según la configuración proporcionada.
    
    Args:
        config: Diccionario con la configuración de debug
    """
    level = config.get('level', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Crear logger específico para GroovinDB
    logger = logging.getLogger('groovindb')
    logger.setLevel(getattr(logging, level)) 
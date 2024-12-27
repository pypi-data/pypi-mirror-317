"""
Módulo de configuración para GroovinDB.
"""
from typing import Dict, Any, Optional
import os
import json
from pathlib import Path

class ConfigError(Exception):
    """Error de configuración."""
    pass

class Config:
    """Clase de configuración."""
    
    def __init__(
        self,
        driver: str,
        host: str,
        database: str,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        schema: Optional[str] = "public",
        cache: Optional[Dict[str, Any]] = None
    ):
        """Inicializar configuración."""
        self.driver = driver
        self.host = host
        self.database = database
        self.port = port or self._get_default_port()
        self.user = user
        self.password = password
        self.schema = schema
        self.cache = cache

    def _get_default_port(self) -> int:
        """Obtener puerto por defecto según el driver."""
        ports = {
            "postgresql": 5432,
            "mysql": 3306
        }
        return ports.get(self.driver, 5432)

    @classmethod
    def load(cls, path: Path) -> "Config":
        """Cargar configuración desde archivo."""
        if not path.exists():
            raise ConfigError(f"El archivo de configuración no existe: {path}")
            
        try:
            with open(path) as f:
                data = json.load(f)
            return cls(**data)
        except json.JSONDecodeError as e:
            raise ConfigError(f"Error al decodificar JSON: {e}")
        except Exception as e:
            raise ConfigError(f"Error al cargar configuración: {e}")

    def save(self, path: Path) -> None:
        """Guardar configuración en archivo."""
        try:
            with open(path, "w") as f:
                json.dump(self.to_dict(), f, indent=4)
        except Exception as e:
            raise ConfigError(f"Error al guardar configuración: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Convertir configuración a diccionario."""
        return {
            "driver": self.driver,
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password,
            "schema": self.schema,
            "cache": self.cache
        }

    def validate(self) -> None:
        """Validar configuración."""
        if self.driver not in ["postgresql", "mysql"]:
            raise ConfigError(f"Driver no soportado: {self.driver}")
            
        if not self.host:
            raise ConfigError("Host no especificado")
            
        if not self.database:
            raise ConfigError("Base de datos no especificada")
            
        if self.port and (self.port < 1 or self.port > 65535):
            raise ConfigError(f"Puerto inválido: {self.port}")

    def get_connection_string(self) -> str:
        """Obtener string de conexión."""
        auth = ""
        if self.user:
            auth = self.user
            if self.password:
                auth += f":{self.password}"
            auth += "@"
            
        return f"{self.driver}://{auth}{self.host}:{self.port}/{self.database}"

    def merge(self, data: Dict[str, Any]) -> "Config":
        """Fusionar con otro diccionario de configuración."""
        merged = self.to_dict()
        merged.update(data)
        return Config(**merged)

    def load_environment(self) -> None:
        """Cargar configuración desde variables de entorno."""
        env_mapping = {
            "GROOVIN_DRIVER": "driver",
            "GROOVIN_HOST": "host",
            "GROOVIN_PORT": "port",
            "GROOVIN_DATABASE": "database",
            "GROOVIN_USER": "user",
            "GROOVIN_PASSWORD": "password",
            "GROOVIN_SCHEMA": "schema"
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                if config_key == "port":
                    value = int(value)
                setattr(self, config_key, value) 
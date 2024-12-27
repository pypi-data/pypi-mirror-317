import click
import os
import json
from typing import Dict, Any
import questionary
from pathlib import Path
import asyncio

def load_config() -> Dict[str, Any]:
    """Carga la configuración desde el archivo groovindb.json"""
    config_path = Path.cwd() / "groovindb.json"
    if config_path.is_file():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

def save_config(config: Dict[str, Any], path: Path) -> None:
    """Guarda la configuración en el archivo especificado"""
    with open(path, "w") as f:
        json.dump(config, f, indent=2)

def generate_stub_file(models: list, stubs_dir: str = None) -> None:
    """Genera un archivo stub simple para autocompletado"""
    if not stubs_dir:
        stubs_dir = "stubs"
    
    stub_dir = Path(stubs_dir)
    stub_dir.mkdir(parents=True, exist_ok=True)
    
    stub_content = [
        "from typing import Any, Dict, List, Optional",
        "from groovindb.src.client import ModelDelegate",
        "",
        "class PrismaLikeClient:",
        *[f"    {model}: ModelDelegate" for model in sorted(models)]
    ]
    
    # Escribir el archivo stub
    with open(stub_dir / "client.pyi", "w") as f:
        f.write("\n".join(stub_content))
    
    # Crear __init__.py
    (stub_dir / "__init__.py").touch()
    
    # Crear un archivo py vacío para asegurar que Python reconozca el directorio como módulo
    with open(stub_dir / "client.py", "w") as f:
        f.write("# Este archivo está intencionalmente vacío\n")

async def run_introspection():
    """Ejecuta la introspección de la base de datos"""
    from groovindb import GroovinDB
    
    config = load_config()
    if not config:
        click.echo("❌ No se encontró configuración. Ejecuta 'groovindb init' primero")
        return

    db = GroovinDB(config)
    await db.connect()
    click.echo("\n✨ Introspección completada exitosamente")
    click.echo("\nModelos disponibles:")
    for model in sorted(db.available_models):
        click.echo(f"  - {model}")
    
    await db.disconnect()
    return db.available_models

@click.group()
def cli():
    """GroovinDB CLI - Herramienta de gestión para GroovinDB"""
    pass

@cli.command()
def init():
    """Inicializa un nuevo proyecto GroovinDB"""
    questions = [
        {
            'type': 'select',
            'name': 'driver',
            'message': 'Selecciona el driver de base de datos:',
            'choices': ['postgresql', 'mysql']
        },
        {
            'type': 'input',
            'name': 'host',
            'message': 'Host de la base de datos:',
            'default': 'localhost'
        },
        {
            'type': 'input',
            'name': 'port',
            'message': 'Puerto:',
            'default': lambda answers: '5432' if answers['driver'] == 'postgresql' else '3306'
        },
        {
            'type': 'input',
            'name': 'database',
            'message': 'Nombre de la base de datos:'
        },
        {
            'type': 'input',
            'name': 'user',
            'message': 'Usuario:'
        },
        {
            'type': 'password',
            'name': 'password',
            'message': 'Contraseña:'
        },
        {
            'type': 'input',
            'name': 'schema',
            'message': 'Esquema (default: public):',
            'default': 'public'
        },
        {
            'type': 'select',
            'name': 'cache_type',
            'message': 'Tipo de caché a utilizar:',
            'choices': ['memory', 'redis']
        },
        {
            'type': 'input',
            'name': 'cache_ttl',
            'message': 'Tiempo de vida del caché (segundos):',
            'default': '300'
        },
        {
            'type': 'select',
            'name': 'debug_level',
            'message': 'Nivel de logging:',
            'choices': ['ERROR', 'WARNING', 'INFO', 'DEBUG'],
            'default': 'INFO'
        },
        {
            'type': 'input',
            'name': 'stubs_location',
            'message': 'Directorio para los stubs (default: stubs):',
            'default': 'stubs'
        }
    ]
    
    answers = questionary.prompt(questions)
    if not answers:
        return
        
    if answers['cache_type'] == 'redis':
        redis_questions = [
            {
                'type': 'input',
                'name': 'redis_url',
                'message': 'URL de Redis:',
                'default': 'redis://localhost'
            }
        ]
        redis_answers = questionary.prompt(redis_questions)
        if redis_answers:
            answers.update(redis_answers)
    
    driver = answers.pop('driver')
    cache_config = {
        'type': answers.pop('cache_type'),
        'ttl': int(answers.pop('cache_ttl')),
        'url': answers.pop('redis_url', 'redis://localhost')
    }
    debug_level = answers.pop('debug_level')
    stubs_location = answers.pop('stubs_location')
    
    config = {
        driver: {
            'user': answers['user'],
            'password': answers['password'],
            'database': answers['database'],
            'host': answers['host'],
            'port': int(answers['port']),
            'schema': answers['schema']
        },
        'cache': cache_config,
        'debug': {
            'level': debug_level
        },
        'stubs': {
            'location': stubs_location
        }
    }
    config_path = Path.cwd() / "groovindb.json"
    save_config(config, config_path)
    click.echo(f"✨ Configuración guardada en {config_path}")
    
    should_introspect = questionary.confirm(
        "¿Deseas realizar la introspección de la base de datos ahora?",
        default=True
    ).ask()
    
    if should_introspect:
        click.echo("\nRealizando introspección...")
        available_models = asyncio.run(run_introspection())
        
        if available_models:
            generate_stub_file(available_models, stubs_location)
            click.echo(f"\n✨ Archivo de tipos generado para autocompletado en {stubs_location}/")

@cli.command()
def introspect():
    """Realiza la introspección de la base de datos y genera los modelos"""
    asyncio.run(run_introspection())

if __name__ == '__main__':
    cli() 
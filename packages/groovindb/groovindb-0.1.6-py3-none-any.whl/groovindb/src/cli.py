import click
import os
import json
from typing import Dict, Any
import questionary
from pathlib import Path
import asyncio

def load_config() -> Dict[str, Any]:
    """Carga la configuración desde el archivo groovindb.json"""
    if os.path.exists("groovindb.json"):
        with open("groovindb.json", "r") as f:
            return json.load(f)
    return {}

def save_config(config: Dict[str, Any]) -> None:
    """Guarda la configuración en el archivo groovindb.json"""
    with open("groovindb.json", "w") as f:
        json.dump(config, f, indent=2)

def generate_stub_file(models: list, stubs_dir: str = None) -> None:
    """Genera un archivo stub simple para autocompletado"""
    stub_content = [
        "from typing import Any, Dict, List, Optional",
        "from src.client import ModelDelegate",
        "",
        "class PrismaLikeClient:",
        *[f"    {model}: ModelDelegate" for model in sorted(models)]
    ]
    
    # Si no se especifica un directorio, usar el directorio actual
    if stubs_dir is None:
        stubs_dir = "stubs"
    
    stub_dir = Path(stubs_dir)
    stub_dir.mkdir(parents=True, exist_ok=True)
    
    with open(stub_dir / "client.pyi", "w") as f:
        f.write("\n".join(stub_content))
    
    (stub_dir / "__init__.py").touch()

async def run_introspection():
    """Ejecuta la introspección de la base de datos"""
    from src.main import GroovinDB
    
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
    save_config(config)
    click.echo("✨ Configuración guardada exitosamente")
    
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
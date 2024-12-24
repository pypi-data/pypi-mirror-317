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

def generate_stub_file(db: 'GroovinDB') -> None:
    """Genera un archivo stub simple para autocompletado"""
    stub_content = [
        "from typing import Any, Dict, List, Optional",
        "from src.client import ModelDelegate",
        "",
        "class PrismaLikeClient:",
        *[f"    {model}: ModelDelegate" for model in sorted(db.available_models)]
    ]
    
    stub_dir = Path("src/stubs")
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
        
    generate_stub_file(db)
    click.echo("\n✨ Archivo de tipos generado para autocompletado")
    
    await db.disconnect()

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
        }
    }
    save_config(config)
    click.echo("✨ Configuración guardada exitosamente")
    
    # Preguntar si quiere realizar la introspección
    should_introspect = questionary.confirm(
        "¿Deseas realizar la introspección de la base de datos ahora?",
        default=True
    ).ask()
    
    if should_introspect:
        click.echo("\nRealizando introspección...")
        asyncio.run(run_introspection())

@cli.command()
def introspect():
    """Realiza la introspección de la base de datos y genera los modelos"""
    asyncio.run(run_introspection())

if __name__ == '__main__':
    cli() 
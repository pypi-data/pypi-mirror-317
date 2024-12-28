import click
import json
import asyncio
from .core.db import GroovinDB

@click.group()
def cli():
    """GroovinDB CLI"""
    pass

@cli.command()
def init():
    """Inicializa un nuevo proyecto GroovinDB"""
    config = {
        'driver': click.prompt('Driver', type=click.Choice(['postgresql', 'mysql']), default='postgresql'),
        'host': click.prompt('Host', default='localhost'),
        'port': click.prompt('Port', type=int, default=5432),
        'database': click.prompt('Database'),
        'user': click.prompt('User'),
        'password': click.prompt('Password', hide_input=True),
        'schema': click.prompt('Schema', default='public')
    }

    with open("groovindb.json", "w") as f:
        json.dump(config, f, indent=2)
    
    click.echo("✅ Configuración creada")

    if click.confirm('¿Deseas generar los tipos automáticamente?', default=True):
        async def run_introspect():
            db = GroovinDB()
            try:
                await db.introspect()
                click.echo("✅ Tipos generados")
            finally:
                await db.disconnect()

        asyncio.run(run_introspect())

@cli.command()
def introspect():
    """Genera tipos desde la base de datos"""
    async def run():
        db = GroovinDB()
        try:
            await db.introspect()
            click.echo("✅ Tipos generados")
        finally:
            await db.disconnect()

    asyncio.run(run())

if __name__ == "__main__":
    cli() 
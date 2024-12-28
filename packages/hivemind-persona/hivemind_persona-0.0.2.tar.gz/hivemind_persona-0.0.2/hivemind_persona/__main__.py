import click
from hivemind_core.database import ClientDatabase, get_db_kwargs
from hivemind_core.server import HiveMindWebsocketProtocol
from hivemind_core.service import HiveMindService
from ovos_utils.xdg_utils import xdg_data_home

from hivemind_persona import PersonaProtocol


@click.command(help="Start listening for HiveMind connections")
@click.option("--persona", help="path to persona .json file", required=True)
@click.option("--host", help="HiveMind host", type=str, default="0.0.0.0")
@click.option("--port", help="HiveMind port number", type=int, required=False)
@click.option("--ssl", help="use wss://", type=bool, default=False)
@click.option("--cert_dir", help="HiveMind SSL certificate directory", type=str, default=f"{xdg_data_home()}/hivemind")
@click.option("--cert_name", help="HiveMind SSL certificate file name", type=str, default="hivemind")
@click.option("--db-backend", type=click.Choice(['redis', 'json', 'sqlite'], case_sensitive=False), default='json',
              help="Select the database backend to use. Options: redis, sqlite, json.")
@click.option("--db-name", type=str, default="clients",
              help="[json/sqlite] The name for the database file. ~/.cache/hivemind-core/{name}")
@click.option("--db-folder", type=str, default="hivemind-core",
              help="[json/sqlite] The subfolder where database files are stored. ~/.cache/{db_folder}}")
@click.option("--redis-host", default="localhost", help="[redis] Host for Redis. Default is localhost.")
@click.option("--redis-port", default=6379, help="[redis] Port for Redis. Default is 6379.")
@click.option("--redis-password", required=False, help="[redis] Password for Redis. Default None")
def listen(persona: str, host: str, port: int,
           ssl: bool, cert_dir: str, cert_name: str,
           db_backend, db_name, db_folder,
           redis_host, redis_port, redis_password):
    kwargs = get_db_kwargs(db_backend, db_name, db_folder, redis_host, redis_port, redis_password)
    websocket_config = {
        "host": host,
        "port": port,
        "ssl": ssl,
        "cert_dir": cert_dir,
        "cert_name": cert_name,
    }
    service = HiveMindService(agent_protocol=PersonaProtocol,
                              agent_config={"persona": persona},
                              network_protocol=HiveMindWebsocketProtocol,
                              network_config=websocket_config,
                              db=ClientDatabase(**kwargs))
    service.run()


if __name__ == "__main__":
    listen()

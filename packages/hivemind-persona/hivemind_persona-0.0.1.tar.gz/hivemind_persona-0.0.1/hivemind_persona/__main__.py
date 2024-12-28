import argparse

from hivemind_persona import PersonaProtocol

from hivemind_core.server import HiveMindWebsocketProtocol
from hivemind_core.service import HiveMindService


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona", help="path to persona .json file", required=True)
    args = parser.parse_args()

    service = HiveMindService(agent_protocol=PersonaProtocol,
                              agent_config={"persona": args.persona},
                              network_protocol=HiveMindWebsocketProtocol)
    service.run()


if __name__ == "__main__":
    run()

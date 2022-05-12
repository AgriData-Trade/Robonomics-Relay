import json
from os import environ
from substrateinterface import Keypair
import logging

__all__ = "Config"

logger = logging.getLogger("AgriData Relay/Config")

class NodeConfig:
    __slots__ = ("id", "_mnemonic", "seed", "keypair")
    def __init__(self, id: str, mnemonic: str):
        self._mnemonic = mnemonic
        self.keypair = Keypair.create_from_mnemonic(self._mnemonic, ss58_format=32)
        self.seed = self.keypair.seed_hex
        self.id = id

class Config:
    __slots__ = ("nodes", "mqtt_url")

    def __init__(self):
        self.nodes: dict[str, NodeConfig] = {}
        f = open('config.json')
        for node in json.load(f):
            self.nodes[node["id"]] = NodeConfig(node["id"], node["mnemonic"])
        f.close()
            
        self.mqtt_url = environ.get("MQTT_URL")

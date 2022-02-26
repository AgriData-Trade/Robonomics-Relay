from os import environ
from substrateinterface import Keypair
import logging

__all__ = "Config"

logger = logging.getLogger("AgriData Relay/Config")


class Config:
    __slots__ = ("_mnemonic", "keypair", "seed", "database_url", "mqtt_url")

    def __init__(self):
        self._mnemonic = environ.get("MNEMONIC_SEED")
        logger.info(f"Configured with mnemonic: {self._mnemonic}")
        self.keypair = Keypair.create_from_mnemonic(self._mnemonic, ss58_format=32)
        logger.info(f"Configured with keypair: {self.seed}")
        self.seed = self.keypair.seed_hex
        logger.info(f"Configured with seed: {self.seed}")
        self.database_url = environ.get("RELAY_DATABASE_URL")
        logger.info(f"Configured with database_url: {self.database_url}")
        self.mqtt_url = environ.get("MQTT_URL")
        logger.info(f"Configured with mqtt_url: {self.mqtt_url}")

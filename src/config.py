from os import environ
from substrateinterface import Keypair
import logging

__all__ = "Config"

logger = logging.getLogger("AgriData Relay/Config")

class DatabaseConfig:
    __slots__ = ("user", "password", "db", "host", "port")

    def __init__(self, user: str, password: str, db: str, host: str, port: str):
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port

class Config:
    __slots__ = ("_mnemonic", "keypair", "seed", "database", "mqtt_url", "enable_db")

    def __init__(self):
        self._mnemonic = environ.get("MNEMONIC_SEED")
        self.keypair = Keypair.create_from_mnemonic(self._mnemonic, ss58_format=32)
        self.seed = self.keypair.seed_hex
        enable_db = environ.get("ENABLE_DATABASE")
        self.enable_db = enable_db
        if enable_db:
            self.database = DatabaseConfig(
                user=environ.get("POSTGRES_USER"),
                password=environ.get("POSTGRES_PASSWORD"),
                db=environ.get("POSTGRES_DB"),
                host=environ.get("DB_HOST"),
                port=environ.get("DB_PORT"),
            )
        else:
            self.database = None
        self.mqtt_url = environ.get("MQTT_URL")

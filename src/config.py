from os import environ
from substrateinterface import Keypair

__all__ = "Config"


class Config:
    __slots__ = ("_mnemonic", "keypair", "seed", "database_url")

    def __init__(self):
        self._mnemonic = environ.get("MNEMONIC_SEED")
        self.keypair = Keypair.create_from_mnemonic(self._mnemonic, ss58_format=32)
        self.seed = self.keypair.seed_hex
        self.database_url = environ.get("DATABASE_URL")

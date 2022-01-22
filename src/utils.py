from substrateinterface import SubstrateInterface
import nacl.secret
import base64
from config import Config
from database import DataItem
import base64


def connect_robonomics() -> SubstrateInterface:
    substrate = SubstrateInterface(
        url="wss://kusama.rpc.robonomics.network",
        ss58_format=32,
        type_registry_preset="substrate-node-template",
        type_registry={
            "types": {
                "Record": "Vec<u8>",
                "Parameter": "Bool",
                "LaunchParameter": "Bool",
                "<T as frame_system::Config>::AccountId": "AccountId",
                "RingBufferItem": {
                    "type": "struct",
                    "type_mapping": [
                        ["timestamp", "Compact<u64>"],
                        ["payload", "Vec<u8>"],
                    ],
                },
                "RingBufferIndex": {
                    "type": "struct",
                    "type_mapping": [
                        ["start", "Compact<u64>"],
                        ["end", "Compact<u64>"],
                    ],
                },
            }
        },
    )
    return substrate


def encrypt(seed: str, data: str) -> str:
    # b = bytes(seed[0:32], "utf8")
    # box = nacl.secret.SecretBox(b)
    # data = bytes(data, "utf-8")
    # encrypted = box.encrypt(data)
    text = base64.b64encode(data.encode("utf-8")).decode("ascii")
    return text


def decrypt(seed: str, encrypted_data: str) -> str:
    # b = bytes(seed[0:32], "utf8")
    # box = nacl.secret.SecretBox(b)
    # decrypted = box.decrypt(base64.b64decode(encrypted_data))
    decrypted = base64.b64decode(encrypted_data)
    return decrypted


def send_data(data: DataItem, config: Config) -> str | None:
    substrate = connect_robonomics()
    text = encrypt(config.seed, data.to_json())

    call = substrate.compose_call(
        call_module="Datalog", call_function="record", call_params={"record": text}
    )
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=config.keypair)
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    return receipt.extrinsic_hash

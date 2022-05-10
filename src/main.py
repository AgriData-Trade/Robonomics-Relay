from typing import Optional

from config import Config
from utils import send_data
import asyncio
from asyncio_mqtt import Client

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

logger = logging.getLogger("AgriData Relay")

received_fields: dict[str, int] = {}


async def subscribe(
    config: Config
):
    async with Client(config.mqtt_url) as client:
        logger.info("Connected to MQTT broker")
        await client.subscribe("agridata/sensors/#")
        async with client.filtered_messages("#") as messages:
            logger.info("Subscribed to sensors")
            async for message in messages:
                _, _, sensor_id = message.topic.split("/")
                logger.info(f"Relaying data: {sensor_id}, {message.payload.decode()}")
                hash = send_data(message.payload.decode(), config)
                logger.info(f"Sent data: {hash}")


async def main():
    config = Config()
    while True:
        try:
            await subscribe(config)
        except TimeoutError:
            # just mqtt timeout
            pass
        except Exception as e:
            logger.exception(e)
            await asyncio.sleep(10)


asyncio.run(main())

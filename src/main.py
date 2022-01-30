from typing import Optional

from config import Config
from database import Database
from utils import send_data
import asyncio
from asyncio_mqtt import Client
from database import DataItem

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


async def subscribe(
    config: Config, data: dict[str, DataItem], database: Optional[Database] = None
):
    async with Client(config.mqtt_url) as client:
        logger.info("Connected to MQTT broker")
        async with client.filtered_messages("sensors/#") as messages:
            logger.info("Subscribed to sensors")
            await client.subscribe("sensors/#")
            async for message in messages:
                _, sensor_id, field = message.topic.split("/")
                logger.info(f"Received: {sensor_id} {field} {message.payload.decode()}")
                if sensor_id in data:
                    if field == "test":
                        logger.info(
                            f"Sending data: {sensor_id}, {data.get(sensor_id).to_json()}"
                        )
                        hash = send_data(data[sensor_id], config)
                        logger.info(f"{sensor_id} sent, hash: {hash}")
                        if database is not None:
                            database.insert_data(data[sensor_id], hash)
                        data[sensor_id] = DataItem(
                            battery_voltage=0,
                            clockBattery_voltage=0,
                            temperature_celsius=0,
                            nitrate_mg_P_L=0,
                            nitrate_mV=0,
                            speciicConductivity_mS_P_cm=0,
                            salinity_psu=0,
                            totalDissolvedSolids_g_P_L=0,
                            rawCoductivity_uS_P_cm=0,
                            pH_units=0,
                            pH_mV=0,
                            referece_mV=0,
                            sensor_id=sensor_id,
                        )

                    else:
                        data[sensor_id].__setattr__(
                            field, float(message.payload.decode())
                        )
                else:
                    data[sensor_id] = DataItem(
                        battery_voltage=0,
                        clockBattery_voltage=0,
                        temperature_celsius=0,
                        nitrate_mg_P_L=0,
                        nitrate_mV=0,
                        speciicConductivity_mS_P_cm=0,
                        salinity_psu=0,
                        totalDissolvedSolids_g_P_L=0,
                        rawCoductivity_uS_P_cm=0,
                        pH_units=0,
                        pH_mV=0,
                        referece_mV=0,
                        sensor_id=sensor_id,
                    )
                    data[sensor_id].__setattr__(field, float(message.payload.decode()))


async def main():
    config = Config()
    database = Database(config.database_url)
    data: dict[str, DataItem] = {}
    while True:
        try:
            await subscribe(config, data, database)
        except TimeoutError:
            # just mqtt timeout
            pass
        except Exception as e:
            logger.exception(e)
            await asyncio.sleep(10)


asyncio.run(main())

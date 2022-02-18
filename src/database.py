from datetime import datetime
import psycopg2
import json
from dataclasses import dataclass
import logging

logger = logging.getLogger("AgriData Relay/Database")


@dataclass
class DataItem:
    temperature_kelvin: float
    nitrate_mg_P_L: float
    nitrate_mV: float
    speciifcConductivity_mS_P_cm: float
    salinity_psu: float
    totalDissolvedSolids_g_P_L: float
    rawCoductivity_uS_P_cm: float
    pH_units: float
    pH_mV: float
    referece_mV: float
    sensor_id: str

    def to_json(self):
        return json.dumps(
            self, default=lambda o: o.__dict__, sort_keys=True, separators=(",", ":")
        )

    def to_dict(self):
        return self.__dict__


class Database:
    def __init__(self, database: str) -> None:
        self.conn = psycopg2.connect(database)
        self.cursor = self.conn.cursor()
        logger.info("Connected to database")

    def __del__(self) -> None:
        self.conn.close()

    def insert_data(self, data: DataItem, hash: str) -> None:
        self.cursor.execute(
            """
            INSERT INTO agridata."Log"(
	            node_id,
                hash,
                nitrate,
                temperature_kelvin, 
                "nitrate_mg_P_L", 
                "nitrate_mV", 
                "specificConductivity_mS_P_cm", 
                salinity_psu, 
                "totalDissolvedSolids_g_P_L", 
                "rawCoductivity_uS_P_cm", 
                "pH_units", 
                "pH_mV", 
                "referece_mV"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            data.sensor_id,
            hash,
            data.temperature_celsius,
            data.nitrate_mg_P_L,
            data.nitrate_mV,
            data.specificConductivity_mS_P_cm,
            data.salinity_psu,
            data.totalDissolvedSolids_g_P_L,
            data.rawCoductivity_uS_P_cm,
            data.pH_units,
            data.pH_mV,
            data.referece_mV,
        )
        logger.info("Inserted data")

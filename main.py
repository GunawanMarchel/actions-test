import logging
import logging.handlers
import os
import json
import xmltodict
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get('https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-JawaBarat.xml')
    if r.status_code == 200:
        data_dict = xmltodict.parse(r.text)
        # data_json = json.dumps(data_dict["data"]["forecast"]["area"][2], indent=4)
        # with open("sample.json", "w") as outfile:
        #     outfile.write(data_json)
        # data = r.json()
        # temperature = data["forecast"]["temp"]
        level = {
            "0": "Cerah",
            "1": "Cerah Berawan",
            "2": "Cerah Berawan",
            "3": "Berawan",
            "4": "Berawan Tebal",
            "5": "Udara Kabur",
            "10": "Asap",
            "45": "Kabut",
            "60": "Hujan Ringan",
            "61": "Hujan Sedang",
            "63": "Hujan Lebat",
            "80": "Hujan Lokal",
            "95": "Hujan Petir",
            "97": "Hujan Petir",
        }
        data = data_dict["data"]["forecast"]["area"][2]
        parameter = data["parameter"][2]["timerange"][0]
        celcius = parameter["value"][0]["#text"]
        fareheit = parameter["value"][1]["#text"]
        logger.info(f'{data["@domain"]}, {data["@description"]}: {level.get(data["@level"])}, Max Temperature {celcius}°C|{fareheit}°F This information is provided by BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)')
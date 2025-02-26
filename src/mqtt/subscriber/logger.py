import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("mqtt.log"),
    ]
)

logger = logging.getLogger("mqtt")

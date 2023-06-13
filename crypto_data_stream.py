import time
import logging
import requests
import json
import os
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(funcName)s: %(levelname)s: %(message)s"
)
logger = logging.getLogger("crypto_api_streaming")
api_key = os.environ.get("COINMARKETCAP_API_KEY")

class DataConfig:
    """
    Obtains the global variables from config.json
    """

    CONFIG_FILE = "config.json"  # Path to the configuration file

    @classmethod
    def load_config(cls):
        """
        Loads the configuration from the JSON file.
        """
        try:
            with open(cls.CONFIG_FILE, "r") as f:
                config = json.load(f)
            return config
        except Exception as e:
            logger.exception(
                f"Failed to load configuration from {cls.CONFIG_FILE}: {e}"
            )
            raise

    @classmethod
    def get_url(cls):
        """
        Returns the url from the configuration.
        """
        config = cls.load_config()
        return config.get("url", {})

    @classmethod
    def get_headers(cls):
        """
        Returns the headers from the configuration.
        """
        config = cls.load_config()
        return config.get("headers", {})

    @classmethod
    def get_parameters(cls):
        """
        Returns the parameters from the configuration.
        """
        config = cls.load_config()
        return config.get("parameters", {})


def data_stream():
    try:
        # These are the Kafka brokers defined in docker-compose-kafka.yml
        producer = KafkaProducer(bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'])    
    except Exception as e:
        logger.error(f'Cannot connect to Kafka producer due to: {e}')
    producer = KafkaProducer(bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'])    

    url = DataConfig.get_url()
    parameters = DataConfig.get_parameters()
    headers = DataConfig.get_headers()

    headers["X-CMC_PRO_API_KEY"] = api_key

    response = requests.get(url, headers=headers, params=parameters)
    data = json.loads(response.text)

    process_and_send_data(producer, data, 'BTC', 'btc_prices')
    process_and_send_data(producer, data, 'ETH', 'eth_prices')


def process_and_send_data(producer, data, symbol, topic):
    price_data = data['data'][symbol]['quote']['USD']

    extracted_data = {
        'timestamp': data['status']['timestamp'],
        'name': data['data'][symbol]['name'],
        'price': price_data['price'],
        'volume_24h': price_data['volume_24h'],
        'percent_change_24h': price_data['percent_change_24h']
    }
    producer.send(topic, json.dumps(extracted_data).encode('utf-8'))

if __name__ == "__main__":
    data_stream()


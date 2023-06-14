import os
import time
import requests
import json
import logging
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger("crypto_data_stream")


def data_stream():
    """
    Gets the data from the API and sends it to Kafka producer
    """
    try:
        api_key = os.environ.get("COINMARKETCAP_API_KEY")
    except:
        logger.error(f"API key couldn't be obtained from the os.")
    
    producer = KafkaProducer(bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'])    

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BTC',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

    end_time = time.time() + 120 # the script will run for 2 minutes
    while True:
        if time.time() > end_time:
            break

        response = requests.get(url, headers=headers, params=parameters)
        data = json.loads(response.text)

        process_and_send_data(producer, data, 'BTC', 'btc_prices')

        time.sleep(10)


def process_and_send_data(producer, data, symbol, topic):
    """
    Modifies the data and sends it to the topic
    """
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


import time
import requests
import json
import os
from kafka import KafkaProducer


def data_stream():
    producer = KafkaProducer(bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'])    

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': 'BTC,ETH',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': "5620aaf5-fcb8-4295-8612-3a4528f938cc"
    }

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


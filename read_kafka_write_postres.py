import mysql.connector
import logging
import json
import time
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')


conn = mysql.connector.connect(
    host="mysql",
    database="mysql",
    user="mysql",
    password="mysql",
    port=3306
)
cur = conn.cursor()


consumer = KafkaConsumer(
    'btc_prices',
    bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'],
    auto_offset_reset='latest',  # Start consuming from the latest offset
    enable_auto_commit=False  # Disable auto-commit to have manual control over offsets
)


current_timestamp = time.time()
five_minutes_ago = current_timestamp - (5 * 60)


def create_new_tables_in_postgres():
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS btc_prices 
        (timestamp VARCHAR(50), name VARCHAR(10), price FLOAT, volume_24h FLOAT, percent_change_24h FLOAT)""")
        logging.info("Table created successfully in Postgres server")
    except Exception as e:
        logging.error(f'Tables cannot be created due to: {e}')


def write_data_to_postgres():
    end_time = time.time() + 120
    for msg in consumer: 
        kafka_message = json.loads(msg.value.decode('utf-8'))

        if time.time() > end_time:
            break

        try:
            # Create an SQL INSERT statement
            insert_query = f"INSERT INTO btc_prices (timestamp, name, price, volume_24h, percent_change_24h) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(insert_query, (kafka_message['timestamp'], kafka_message['name'], kafka_message['price'], kafka_message['volume_24h'], kafka_message['percent_change_24h']))
            conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")



if __name__ == "__main__":
    create_new_tables_in_postgres()
    write_data_to_postgres()

    cur.close()
    conn.close()



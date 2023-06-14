import mysql.connector
import logging
import json
import time
from kafka import KafkaConsumer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(funcName)s:%(levelname)s:%(message)s')
logger = logging.getLogger("read_kafka_write_mysql")


try:
    conn = mysql.connector.connect(
        host="mysql",
        database="mysql",
        user="mysql",
        password="mysql",
        port=3306
    )
    cur = conn.cursor()
    logger.info('MySQL server connection is successful')
except Exception as e:
    logger.error(f"Couldn't create the MySQL connection due to: {e}")

try:
    consumer = KafkaConsumer(
        'btc_prices',
        bootstrap_servers=['kafka1:19092', 'kafka2:19093', 'kafka3:19094'],
        auto_offset_reset='latest',  # Start consuming from the latest offset
        enable_auto_commit=False  # Disable auto-commit to have manual control over offsets
    )
    logger.info("Kafka connection successful")
except Exception as e:
    logger.error(f"Kafka connection is not successsful. {e}")


def create_new_tables_in_mysql():
    """
    Creates the btc_prices table in MySQL server.
    """
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS btc_prices 
        (timestamp VARCHAR(50), name VARCHAR(10), price FLOAT, volume_24h FLOAT, percent_change_24h FLOAT)""")
        logging.info("Table created successfully in MySQL server")
    except Exception as e:
        logging.error(f'Tables cannot be created due to: {e}')


def insert_data_into_mysql():
    """
    Insert the latest messages coming to Kafka consumer to MySQL table.
    """
    end_time = time.time() + 120 # the script will run for 2 minutes
    for msg in consumer: 
        if time.time() > end_time:
            break

        kafka_message = json.loads(msg.value.decode('utf-8'))
        try:
            # Create an SQL INSERT statement
            insert_query = f"INSERT INTO btc_prices (timestamp, name, price, volume_24h, percent_change_24h) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(insert_query, (kafka_message['timestamp'], kafka_message['name'], kafka_message['price'], kafka_message['volume_24h'], kafka_message['percent_change_24h']))
            conn.commit()
        except Exception as e:
            logging.error(f"Error inserting data: {e}")



if __name__ == "__main__":
    create_new_tables_in_mysql()
    insert_data_into_mysql()

    cur.close()
    conn.close()



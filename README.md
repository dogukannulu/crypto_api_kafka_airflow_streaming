# Information
![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/8cf1c934-967d-43b7-8b37-30d7504cb181)


This repo illustrates a streaming data pipeline.

Gets BTC prices from Crypto API with an API key. Sends the price data to Kafka topics every 10 seconds using Airflow. Every message is read by Kafka consumer and written to MySQL table.

`crypto_data_stream_dag.py` -> The DAG script that writes the API data to a Kafka producer every 10 seconds. In parallel, the messages are consumed and written to MySQL table.

`crypto_data_stream.py` -> The script that gets the data from API and sends it to Kafka topic

`read_kafka_write_mysql.py` -> The script that reads the Kafka consumer data and writes it to MySQL tables.


## Apache Airflow

Run the following command to clone the necessary repo on your local

```bash
git clone https://github.com/dogukannulu/docker-airflow.git
```
After cloning the repo, run the following command only once:

```bash
docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
```

Then change the docker-compose-LocalExecutor.yml file with the one in this repo and add `requirements.txt` file in the folder. This will bind the Airflow container with Kafka container and necessary modules will automatically be installed:

```bash
docker-compose -f docker-compose-LocalExecutor.yml up -d
```

Now you have a running Airflow container and you can access the UI at `https://localhost:8080`

## Apache Kafka

`docker-compose-kafka.yml` will create a multinode Kafka cluster. We can define the replication factor as 3 since there are 3 nodes (kafka1, kafka2, kafka3). We can also see the Kafka UI on `localhost:8888`. It also creates the MySQL server and binds it to Kafka and Airflow.

We should only run:

```bash
docker-compose -f docker-compose-kafka.yml up -d
```

![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/0cd84ffa-8d20-4db8-8900-c5d3413e0403)

After accessing to Kafka UI, we can create the topic `btc_prices`. Then, we can see the messages coming to Kafka producer:

![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/693e858e-6bca-4967-ac70-edb5304db723)


## Running DAGs

After these steps, we should move all .py scripts under dags folder in `docker-airflow` repo. Then we can see that `crypto_data_stream` appears in DAGS page.

<img width="866" alt="image" src="https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/bcc0726a-3739-4e2a-a62f-ee1869ce545f">


When we turn the OFF button to ON, we can see that the data will be sent to Kafka topics every 10 seconds. We can check from Kafka UI as well.

![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/fd8bbf33-fe9a-4d99-be79-b023500d4372)

## MySQL
I created the MySQL server as a Docker container. Every env variable is located in `docker-compose-kafka.yml`. I also defined them in the scripts.

By running the following command, we can access to MySQL server:

```bash
docker exec -it mysql mysql -u mysql -p
```

After access, we can run the following commands and see that the Kafka topic messages are inserted into MySQL table successfuly

```bash
SHOW databases;
USE mysql;
SHOW tables;
select * from btc_prices;
```

<img width="587" alt="image" src="https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/f8f69518-1b0d-47cc-b4c5-b11e4a01e7ae">



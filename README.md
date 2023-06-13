# Information

This repo gets BTC and ETH prices from Crypto API with an API key. Sends the price data to Kafka topics every 5 minutes using Airflow. This illustrates a streaming pipeline overall.

`airflow_dag.py` -> The main DAG script

`crypto_data_stream.py` -> The script that gets the data from API and sends it to Kafka topic

`config.json` -> The configuration file that keeps URL, parameters and headers necessary for obtaining data from the API


## Apache Airflow:

Run the following command to clone the necessary repo on your local

```bash
git clone https://github.com/dogukannulu/docker-airflow.git
```
After cloning the repo, run the following command only once:

```bash
docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
```

Then change the docker-compose-LocalExecutor.yml file with the one in this repo and add requirements.txt file in the folder. This will bind the Airflow container with Kafka container and necessary modules will automatically be installed:

```bash
docker-compose -f docker-compose-LocalExecutor.yml up -d
```

Now you have a running Airflow container and you can reach out to that on `https://localhost:8080`

## Apache Kafka:

`docker-compose-kafka.yml` will create a multinode Kafka cluster. We can define the replication factor as 3 since there are 3 nodes (kafka1, kafka2, kafka3). We can also see the Kafka UI on `localhost:8888` 

We should only run:

```bash
docker-compose -f docker-compose-kafka.yml up -d
```

![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/0cd84ffa-8d20-4db8-8900-c5d3413e0403)

After reaching to Kafka UI, we can create topics `btc_prices` and `eth_prices`.

## Running DAG:

After these steps, we should move `crypto_data_stream.py`, `airflow_dag.py` and `config.json` under dags folder in `docker-airflow` repo. Then we can see that `crypto_data_stream` DAG appears in DAGS page.

![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/65a6d7e1-fc9f-448b-bf47-3d1454fec16e)


When we turn the OFF button into ON, we can see that the data will be sent to Kafka topics every 5 minutes.

![image](https://github.com/dogukannulu/crypto_api_kafka_airflow_streaming/assets/91257958/fd8bbf33-fe9a-4d99-be79-b023500d4372)




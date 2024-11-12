
*This script uses kafka-python library from this Location*

git+https://github.com/dpkp/kafka-python.git


Follow this link and setup Kafka on Docker/Podman

https://bigdatabook.gchandra.com/chapter_08/kafka/kafka-software.html

```bash
# Create Kafka topic with 3 partitions
podman exec -it kafka kafka-topics.sh \
    --create \
    --topic transactions-topic \
    --bootstrap-server localhost:9092 \
    --partitions 3 \
    --replication-factor 1
```

**Open New Terminal**

```
git clone https://github.com/gchandra10/python_kafka_cc_frauddetection_demo.git

cd python_kafka_cc_frauddetection_demo

poetry update
```

**Train an model and store the result as joblib file**

```
poetry run python train_initial_model.py
```

**Run the Transaction Generation**

```
poetry run python run_generator.py
```

**Open 3 more terminals and run the following**

```
poetry run python run_consumer.py 1
```

```
poetry run python run_consumer.py 2
```

```
poetry run python run_consumer.py 3
```

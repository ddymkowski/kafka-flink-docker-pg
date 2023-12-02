import logging
import sys

from pyflink.common import Types
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaProducer, FlinkKafkaConsumer
from pyflink.datastream.formats.csv import CsvRowSerializationSchema
from pyflink.datastream.formats.json import JsonRowDeserializationSchema


def read_from_kafka(env):
    deserialization_schema = JsonRowDeserializationSchema.builder().type_info(
        Types.ROW_NAMED(['data', 'error', 'traceback', 'details'],
                        [Types.MAP(key_type_info=Types.STRING(), value_type_info=Types.STRING()),
                         Types.STRING(), Types.STRING(),
                         Types.STRING()])).build()

    kafka_consumer = FlinkKafkaConsumer(
        topics='binance-feed',
        deserialization_schema=deserialization_schema,
        properties={'bootstrap.servers': 'kafka:9092', }
    )
    kafka_consumer.set_start_from_earliest()

    env.add_source(kafka_consumer).print()
    env.execute()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("file:///opt/flink/lib/flink-sql-connector-kafka-1.16.0.jar")

    print("start reading data from kafka")
    read_from_kafka(env)

from kafka import KafkaConsumer
from pymongo import MongoClient
from prometheus_client import start_http_server, Counter, Summary, Gauge
import json
import logging
import time

logging.basicConfig(level=logging.INFO)

# Start Prometheus metrics server
start_http_server(8000)

# Define metrics
trade_counter = Counter('trades_ingested_total', 'Total number of trades ingested')
insert_latency = Summary('mongodb_insert_latency_seconds', 'Time spent inserting into MongoDB')
total_trades_gauge = Gauge('mongodb_total_trades', 'Current total number of trades in MongoDB')

# Kafka setup
consumer = KafkaConsumer(
    'binance-trades',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='binance-consumer'
)

# MongoDB setup
mongo = MongoClient('mongodb://mongo:27017/')
db = mongo.binance
collection = db.trades

logging.info("Consumer started. Listening to 'binance-trades' topic...")

# Consume and insert
@insert_latency.time()
def insert_trade(trade):
    collection.insert_one(trade)
    trade_counter.inc()

for message in consumer:
    try:
        trade = message.value
        logging.info(f"Inserting trade: {trade['s']} @ {trade['p']}")
        insert_trade(trade)
        count = collection.count_documents({})
        total_trades_gauge.set(count)  # Update gauge with current count
        logging.info(f"Inserted trade. Total count: {count}")
    except Exception as e:
        logging.error(f"Failed to insert: {e}")

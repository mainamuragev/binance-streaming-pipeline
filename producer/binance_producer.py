import json
import time
import websocket
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

def create_producer():
    for attempt in range(10):
        try:
            print(f"Attempt {attempt+1}: Connecting to Kafka...")
            return KafkaProducer(
                bootstrap_servers="kafka:9092",
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
        except NoBrokersAvailable:
            print("Kafka not ready, retrying in 5s...")
            time.sleep(5)
    raise Exception("Kafka broker not available after 10 retries")

producer = create_producer()

def on_message(ws, message):
    data = json.loads(message)
    producer.send("binance-trades", value=data)
    print("Sent:", data)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    subscribe_msg = {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@trade"],
        "id": 1
    }
    ws.send(json.dumps(subscribe_msg))

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

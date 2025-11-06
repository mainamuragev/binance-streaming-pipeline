from kafka import KafkaProducer
import json
import websocket
import logging

logging.basicConfig(level=logging.INFO)

# Binance WebSocket endpoint
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def on_message(ws, message):
    try:
        trade = json.loads(message)
        logging.info(f"Sent: {trade}")
        producer.send('trades', value=trade)  # ✅ Topic aligned with consumer
    except Exception as e:
        logging.error(f"Failed to send message: {e}")

def on_error(ws, error):
    logging.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info("WebSocket closed")

def on_open(ws):
    logging.info("WebSocket connection opened")

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        BINANCE_WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

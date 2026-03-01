```markdown
#  Binance Streaming Pipeline

Real-time crypto trade ingestion pipeline using Kafka, MongoDB, Prometheus, and Grafana. Streams Binance trades via WebSocket, persists them in MongoDB, and exposes metrics for observability. Fully containerized with Docker Compose for modularity, transparency, and performance monitoring.

---

##  Features

-  Live trade ingestion from Binance WebSocket
-  Kafka-based streaming architecture
-  MongoDB persistence
-  Prometheus metrics (`/metrics` endpoint)
-  Grafana dashboard for observability
-  Docker Compose orchestration

---

##  Architecture

```
Binance WebSocket → Kafka → Consumer → MongoDB
                             ↘ Prometheus → Grafana
```

- **Producer**: Connects to Binance and publishes trades to Kafka
- **Consumer**: Subscribes to Kafka, inserts trades into MongoDB, exposes metrics
- **Monitoring**: Prometheus scrapes metrics; Grafana visualizes them

---

##  Setup

```bash
git clone https://github.com/mainamuragev/binance-streaming-pipeline.git
cd binance-streaming-pipeline
docker compose up --build
```

Access services:

- Prometheus: [http://localhost:9090](http://localhost:9090)
- Grafana: [http://localhost:3000](http://localhost:3000)
  - Login: `admin` / `admin`

---

##  Metrics Exposed

- `trades_ingested_total`
- `mongodb_insert_latency_seconds`
- `mongodb_total_trades`
- Python process metrics (`process_*`, `python_gc_*`)

---

##  Grafana Panels (Suggested)

- Total trades ingested
- Ingestion rate (`rate(trades_ingested_total[1m])`)
- MongoDB insert latency (avg, p95)
- Trade count in MongoDB
---

##  License

MIT — feel free to fork, modify, and share.

---

##  Author

Built by [Maina Murage](https://github.com/mainamuragev) — backend/data engineer passionate about streaming pipelines, observability, and infrastructure clarity.
```



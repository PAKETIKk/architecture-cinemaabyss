from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer
from threading import Thread
import os
import json
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route("/api/events/movie", methods=["POST"])
def movie():
    data = request.get_json()
    event = {
        "movie_id": data.get("movie_id"),
        "title": data.get("title"),
        "action": data.get("action"),
        "user_id": data.get("user_id")
    }
    PRODUCER.send(
        "movie-events",
        value=event
    )
    return jsonify({ "status": "success" }), 201

@app.route("/api/events/user", methods=["POST"])
def user():
    data = request.get_json()
    event = {
        "user_id": data.get("user_id"),
        "username": data.get("username"),
        "action": data.get("action"),
        "timestamp": data.get("timestamp")
    }
    PRODUCER.send(
        "user-events",
        value=event
    )
    return jsonify({ "status": "success" }), 201

@app.route("/api/events/payment", methods=["POST"])
def payment():
    data = request.get_json()
    event = {
        "payment_id": data.get("payment_id"),
        "user_id": data.get("user_id"),
        "amount": data.get("amount"),
        "status": data.get("status"),
        "timestamp": data.get("timestamp"),
        "method_type": data.get("method_type")
    }
    PRODUCER.send(
        "payment-events",
        value=event
    )
    return jsonify({ "status": "success" }), 201

@app.route("/api/events/health")
def health():
    return jsonify({ "status": True }), 200

def consume_events():
    app.logger.info("Consumer запущен")
    try:
        for message in CONSUMER:
            app.logger.info(
                "Events: topic=%s, value=%s",
                message.topic,
                message.value,
            )
            CONSUMER.commit()
    except Exception:
        app.logger.exception("Ошибка consumer")


# Переменные окружения
KAFKA_BROKERS = os.getenv("KAFKA_BROKERS")
# KafkaProducer, KafkaConsumer
PRODUCER = KafkaProducer(
    bootstrap_servers=KAFKA_BROKERS.split(","),
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)
CONSUMER = KafkaConsumer(
    "movie-events",
    "user-events",
    "payment-events",
    bootstrap_servers=KAFKA_BROKERS.split(","),
    group_id="events-service",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)
# Запуск сервиса
if __name__ == "__main__":
    Thread(target=consume_events, daemon=True).start()

    port = int(os.getenv("PORT", 8082))
    app.run(host="0.0.0.0", port=port)
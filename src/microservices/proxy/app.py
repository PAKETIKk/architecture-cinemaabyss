from flask import Flask, request, jsonify
import os
import random
import requests

app = Flask(__name__)

@app.route("/api/movies", methods=["GET", "POST"])
def movies():
    url = MONOLITH_URL
    if GRADUAL_MIGRATION: 
        random_v = random.uniform(0, 100)
        url = MONOLITH_URL if random_v > MOVIES_MIGRATION_PERCENT else MOVIES_SERVICE_URL
    app.logger.info(
        "Proxy: %s %s -> %s",
        request.method,
        request.path,
        url,
    )
    if request.method == "GET":
        movie_id = request.args.get("id")
        if movie_id:
            response = requests.get(
                f'{url}/api/movies',
                params={'id': movie_id}
            )
            return jsonify(response.json()), response.status_code
        else:
            response = requests.get(
                f'{url}/api/movies'
            )
            return jsonify(response.json()), response.status_code
    elif request.method == "POST":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.post(
            f'{url}/api/movies',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code

@app.route("/api/users", methods=["GET", "POST"])
def users():
    url = MONOLITH_URL
    if request.method == "GET":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.get(
            f'{url}/api/users',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    elif request.method == "POST":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.post(
            f'{url}/api/users',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code

@app.route("/api/payments", methods=["GET", "POST"])
def payments():
    url = MONOLITH_URL
    if request.method == "GET":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.get(
            f'{url}/api/payments',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    elif request.method == "POST":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.post(
            f'{url}/api/payments',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code

@app.route("/api/subscriptions", methods=["GET", "POST"])
def subscriptions():
    url = MONOLITH_URL
    if request.method == "GET":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.get(
            f'{url}/api/subscriptions',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code
    elif request.method == "POST":
        headers = {}
        if request.content_type:
            headers["Content-Type"] = request.content_type
        response = requests.post(
            f'{url}/api/subscriptions',
            data=request.get_data(),
            params=list(request.args.items(multi=True)),
            headers=headers
        )
        return jsonify(response.json()), response.status_code

@app.route("/health")
def health():
    return jsonify({ "status": True }), 200

# Переменные окружения
MONOLITH_URL                = os.getenv("MONOLITH_URL")
MOVIES_SERVICE_URL          = os.getenv("MOVIES_SERVICE_URL")
EVENTS_SERVICE_URL          = os.getenv("EVENTS_SERVICE_URL")
GRADUAL_MIGRATION           = bool(os.getenv("GRADUAL_MIGRATION"))
MOVIES_MIGRATION_PERCENT    = int(os.getenv("MOVIES_MIGRATION_PERCENT"))

# Запуск сервиса
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
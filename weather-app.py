import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response



@app.route("/weather")
def get_weather():
    request_dt = dt.datetime.now()
    location = request.args.get("q")
    date_history = request.args.get("dt")
    url_weather = "http://api.weatherapi.com/v1"
    url_json = "history.json" if bool(date_history and date_history.strip()) else "current.json"
    url = f"{url_weather}/{url_json}"

    KEY = "1d58ea1fd5334dd59a9175841231902"
    query_params = {
        "key": KEY,
        "q" : location,
        "dt": date_history
    }
    payload = {
        "requester_name": "Ihor Yevtushenko",
        "location": "Kyiv,Ukraine",
        "date": request_dt
    }
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, params=query_params)

    result = {
        "data": payload,
        "weather": json.loads(response.text)
    }

    return result
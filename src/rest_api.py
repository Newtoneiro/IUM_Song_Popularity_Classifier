from flask import Flask, request
from datetime import datetime

from main_models import LSTMModel, LinearRegressionModel


naive_model = LinearRegressionModel()
lstm_model = LSTMModel()
app = Flask(__name__)


def log(id, chosen_model, input_data, output_data):
    with open("service_logs.log", "a") as f:
        f.write(f"[{datetime.now()}] - ID: {id}\n")
        f.write(f"Predicion made with {chosen_model}\n")
        f.write(f"Input data: {input_data}\n")
        f.write(f"Output data: {output_data}\n")


@app.route("/predict", methods=["POST"])
def serve_foo():
    data = request.json
    if not (req_id := data.get("id")):
        return "No id provided. id field is necessary.", 400
    if not (inputs := data.get("week_inputs")):
        return "No data provided. week_inputs field is necessary.", 400
    if not (future_points := data.get("future_points")):
        return "No future points provided. future_points field is necessary.", 400
    sum = 0
    for let in req_id:
        sum += ord(let)
    model = naive_model if sum % 2 == 0 else lstm_model
    try:
        precitions = model.predict([float(x) for x in inputs], int(future_points))
    except ValueError as err:
        return [err.args], 400

    result = [str(x) for x in precitions]
    log(req_id, model.__class__.__name__, inputs, result)
    return result


if __name__ == "__main__":
    app.run(port=8888)

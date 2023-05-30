import pytest
import json
from src.rest_api import app


def get_response(body):
    response = app.test_client().post(
        "/predict", data=json.dumps(body), content_type="application/json"
    )
    return response


@pytest.mark.parametrize("id", ["1", "2"])
@pytest.mark.parametrize("future_points", [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize(
    "week_inputs",
    [
        [1.0, 2.0, 3.0, 4.0],
        [1.0, 2.0, 3.0, 4.0, 5.0],
    ],
)
def test_predictions(id, future_points, week_inputs):
    body = {
        "id": id,
        "future_points": future_points,
        "week_inputs": week_inputs,
    }
    response = get_response(body)
    assert response.status_code == 200
    assert [
        float(elem) for elem in response.json[: len(body["week_inputs"])]
    ] == week_inputs
    assert len(response.json) == len(week_inputs) + future_points


def test_request_without_id():
    body = {
        "future_points": 1,
        "week_inputs": [1, 2, 3, 4, 5],
    }
    response = get_response(body)
    assert response.text == "No id provided. id field is necessary."
    assert response.status_code == 400


def test_request_without_future_points():
    body = {
        "id": "klasjfklaj",
        "week_inputs": [1, 2, 3, 4, 5],
    }
    response = get_response(body)
    assert (
        response.text == "No future points provided. future_points field is necessary."
    )
    assert response.status_code == 400


def test_request_without_week_inputs():
    body = {
        "id": "klasjfklaj",
        "future_points": 1,
    }
    response = get_response(body)
    assert response.text == "No data provided. week_inputs field is necessary."
    assert response.status_code == 400

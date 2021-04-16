from flask import Flask, request
import json
import pickle
from utils.input_processor import process_input
from database.database import Database

database = Database()


app = Flask(__name__)

# Load the model
regressor = pickle.load(open("regressor.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))


@app.route("/")
def index() -> str:
    try:
        return "Connection established"
    except:
        return "There was a problem connecting to the database"


@app.route("/predict", methods=["POST"])
def predict() -> str:
    """
    Creates a route to return the prediction given the user inputs.
    :return: list of predictions of the price
    """
    user_input = request.data
    try:
        inputs = process_input(user_input)
        predictions = regressor.predict(inputs)
        # output = json.dumps({"Predicted price": predictions.tolist()})
        result = [round(float(prediction), 2) for prediction in predictions]
        output = json.dumps({"Predicted price": result})
        # return output, 200
    except (KeyError, json.JSONDecodeError):
        output = json.dumps(
            {"Error": "Data could not be processed. Please check the input values."}
        )
        return output, 400

    finally:
        database.create_record(user_input.decode(), output)
        return output, 200

    # try:
    #    predictions = regressor.predict(inputs)
    # except:
    #    output = json.dumps({"Error": "Predictions failed"})
    #    return output, 500


@app.route("/last_requests", methods=["GET"], defaults={"number_of_records": 10})
@app.route("/last_requests/<number_of_records>", methods=["GET"])
def last_requests(number_of_records: int) -> list:
    retrieved_requests = []
    """
    Creates route to return a specified number of last requests made using the API. Returns 10 requests by default.
    :param number_of_records: the number of last requests to be returned (int)
    :return: the number of last requests made using the API
    """
    try:
        retrieved_requests = database.get_recent_records(number_of_records)
    except:
        output = json.dumps(
            {
                "Error": """Request to retrieve {number_of_records} records failed. Please change the
                                          number of records to be retrieved.""".format(
                    number_of_records=number_of_records
                )
            }
        )

    return json.dumps({"last_requests": retrieved_requests}), 200

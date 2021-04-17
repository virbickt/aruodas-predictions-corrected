from flask import Flask, request
import json
import pickle
from utils.input_processor import process_input
from database.database import Database

database = Database()


app = Flask(__name__)

# Load the models
regregssor = pickle.load(open("regressor.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))


@app.route("/")
def index() -> str:
    try:
        return "Connection established"
    except:
        return "There was a problem loading the app"


@app.route("/predict", methods=["POST"])
def predict() -> str:
    """
    Creates a route to return the prediction given the user inputs.
    :return: list of predictions of the price
    """
    user_input = request.data

    # try process the data and catch errors
    try:
        inputs = process_input(user_input)

    # catch json decoding-related errors
    except (KeyError, json.JSONDecodeError):
        output = json.dumps(
            {"Error": f"Data could not be processed. Please check the syntax"}
        )
        return output, 400

    # catch missing values in input data
    except ValueError as e:
        output = json.dumps({"Error": f"Wrong inputs: {e}"})
        return output, 400

    # try scaling the inputs
    try:
        inputs_scaled = scaler.transform(inputs)

    except Exception as e:
        output = json.dumps({"Error": f"Scaling step failed: {e}"})
        return output, 400

    # try making a prediction
    try:
        predictions = regressor.predict(inputs_scaled)
        result = [float(prediction) for prediction in predictions]
        output = json.dumps({"Predicted price": result})
    except Exception as e:
        output = json.dumps({"Error": f"Prediction failed: {e}"})
        return output, 400

    # try inserting the prediction outputted into database
    try:
        database.create_record(user_input.decode(), output)
        return output, 200

    except Exception as e:
        output = json.dumps(
            {"Error": f"The output could not be inserted into database: {e}"}
        )
        return output, 500


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

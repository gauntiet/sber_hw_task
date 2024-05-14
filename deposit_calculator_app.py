import json
import logging
from flask import Flask, request
from waitress import serve
from deposit_calculator import DepositCalculator


NAME = __file__.split("/",)[-1].split(".")[0]
logging.basicConfig(
    filename=f"{NAME}.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO)
app = Flask(NAME)


def serialize_error(error_msg: str) -> tuple[str, int]:
    return json.dumps({"error": error_msg}), 400

@app.route("/", methods=["POST", "GET", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"])
def calculate_deposit():
    data = request.data
    logger = logging.getLogger(NAME)
    if request.method == "POST":
        try:
            data = json.loads(data)
        except ValueError:
            logger.error(f"cant deserialize data from json - data:{data}")
            return serialize_error("deserialization failed, data should be in json")
        deposit_calculator = DepositCalculator(data)
        deposit_dict, validation_msg = deposit_calculator.calculate_deposit()
        if deposit_dict:
            return json.dumps(deposit_dict), 200
        else:
            logger.error(f"data for deposit calculation is not valid - data:{data}, validation_msg:{validation_msg}")
            return serialize_error(validation_msg)
    else:
        return serialize_error("use POST method for this request")


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=9999)
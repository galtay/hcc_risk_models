from flask import Flask, request, url_for, jsonify, abort, make_response
import random
import sys
import json
import hcc_risk_models as hrm


app = Flask(__name__)
app.secret_key = 'This is really unique and secret'
base_route = '/hcc_risk_models/api/v1.0'



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route(base_route + '/')
def home():
    return jsonify({'message': 'hello'})


@app.route(base_route + '/models', methods=['GET'])
def list_models():
    return jsonify(hrm.VALID_MODEL_DESCRIPTIONS)


@app.route(base_route + '/models/<model_name>', methods=['GET'])
def describe_model(model_name):
    # return json 404 if model name not valid
    if model_name not in hrm.VALID_MODEL_DESCRIPTIONS:
        abort(404)

    if model_name == 'V2216_79_O2':
        from hcc_risk_models.v2216_79_O2 import risk_model
        model = risk_model.V2216_79_O2()
    elif model_name == 'V2217_79_O1':
        from hcc_risk_models.v2217_79_O1 import risk_model
        model = risk_model.V2217_79_O1()

    description = model.return_model_description()
    return jsonify(description)


@app.route(base_route + '/models/<model_name>/evaluate', methods=['POST'])
def evaluate_model(model_name):
    # return json 404 if model name not valid
    if model_name not in hrm.VALID_MODEL_DESCRIPTIONS:
        abort(404)

    if model_name == 'V2216_79_O2':
        from hcc_risk_models.v2216_79_O2 import risk_model
        model = risk_model.V2216_79_O2()
    elif model_name == 'V2217_79_O1':
        from hcc_risk_models.v2217_79_O1 import risk_model
        model = risk_model.V2217_79_O1()

    demographics, diagnoses = model.input_json_to_dataframes(request.json)
    result = model.evaluate_risk(demographics, diagnoses)

    return jsonify(result)

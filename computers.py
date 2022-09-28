#!/usr/bin/python3
"""
    + Make a flask app that serves a single endpoint at the pathname /computers, supporting the GET method.

    + Save the contents of this gist as the raw data for the computers as a variable in your python
    code: https://gist.github.com/dcripplinger/a613107e75adf6aa9243985970cab54b

    + The endpoint should return a json list of the raw data, in the same format as it appears, but
    with the objects sorted based on the field name "model", in alphabetical order.

    + Do not mutate the original raw data while handling a request.

    + If the request includes a query parameter "screen_size" (e.g. /computers?screen_size=13in), the
    returned list should only include objects with a matching screen_size, as an exact string match.

    + If screen_size is not passed in as a query parameter, all results should be returned in the list.

    Zip or tar the project and email the compressed file to me so that I can run it on my machine to
    test it out, or share it with me whichever way you prefer, as long as I can examine the code
    and run the app.

    No written tests are needed.

    Feel free to look stuff up on the internet.

    Feel free to email me with any questions.
"""

from copy import copy
from flask import Flask, jsonify, request

## ——————————————— VIRTUAL DATABASE —————————————————————
COMPUTERS_DB = [
                {
                    "id": "1",
                    "model": "Lenovo Thinkpad",
                    "disk_space": "512GB",
                    "screen_size": "13in"
                },
                {
                    "id": "2",
                    "model": "Legion 5",
                    "disk_space": "1TB",
                    "screen_size": "17in"
                },
                {
                    "id": "3",
                    "model": "Macbook Pro",
                    "disk_space": "1TB",
                    "screen_size": "15in"
                },
                {
                    "id": "4",
                    "model": "Surface Pro 7",
                    "disk_space": "256GB",
                    "screen_size": "13in"
                },
                {
                    "id": "5",
                    "model": "Surface Pro 6",
                    "disk_space": "512GB",
                    "screen_size": "13in"
                }
            ]

app = Flask(__name__)


# ———————————— SERVICE FUNCTIONS —————————————
def filter_by_argument(data_set, key=None, value=None):
    """ Filter data_set by argument"""
    response_data = []
    for computer in data_set:
        # Check value in data_set by key (i.e. "column")
        if value == computer.get(key, None):
            response_data.append(computer)

    return response_data

def sort_by_argument(data_set, key='model'):
    """ Sorting data_set by argument"""
    response_data = sorted(data_set, key=lambda d: d[key])
    return response_data


# ——————————————— ENDPOINTS ———————————————————
@app.route("/computers/sorted/", methods=['GET'])
def sorted_computers():
    """ Endpoint handler
        responds with various ways of sorting values

        Request example:
            /computers/sorted/?screen_size """

    ### Make a "request" to the "database"
    data = copy(COMPUTERS_DB)  # It would be complex data, in that case I would use deepcopy
    if len(request.args):
        arg = list(request.args)[0]  # pick the first argument only
        if arg in data[0].keys():
            # If arg is in the record...
            data = sort_by_argument(data, arg)  # Sort query result by title
    return jsonify(data)  # Reply in the same format


@app.route("/computers/", methods=['GET'])
def computers():
    """ Endpoint handler
        responds always sorted by model + filtering

        Request example:
            /computers/?model=123&disk_space=123&screen_size=123 """

    ### Make a "request" to the "database"
    data = copy(COMPUTERS_DB)
    data = sort_by_argument(data, 'model')  # Sort the query result by a model title

    if len(request.args):
        ### There are some arguments, filter data by the arguments
        for arg in request.args:
            # Filter results by each argument value
            argument_value = request.args.get(arg, None)
            data = filter_by_argument(data, arg, argument_value)

    else:
        ### Default case (no arguments)
        pass  # ** used for debug **

    return jsonify(data)  # Reply just data


# ————————————— ERROR HANDLER ————————————————
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"result": "wrong path"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=8765)

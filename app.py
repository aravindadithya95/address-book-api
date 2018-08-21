from flask import Flask, request, make_response, jsonify

# import configuration file
import config

# import data store and its methods for CRUD
import es_store as data_store

app = Flask(__name__)


@app.route('/contact', methods=['GET'])
def list_contacts():
    """
    This endpoint will provide a listing of all contacts, allowing for a defined pageSize
    (number of results allowed back), and the ability to offset by page number to get multiple pages.
    """

    # get query parameters
    try:
        page_size = int(request.args.get('pageSize'))
        page = int(request.args.get('page'))
    except ValueError:
        return make_response('Invalid query parameter(s).', 400)
    query = request.args.get('query')

    # check if page number is valid
    if page <= 0:
        return make_response('Invalid page number.', 400)

    # read the data store
    return make_response(jsonify(data_store.search_contacts(page_size, page, query)), 200)


@app.route('/contact', methods=['POST'])
def create_contact():
    """This endpoint creates the contact."""
    
    # create the contact
    res = data_store.create_contact(request.form)

    # send response
    return make_response(res['description'], res['status'])


@app.route('/contact/<string:name>', methods=['GET'])
def get_contact(name):
    """This endpoint returns the contact details by a unique name."""

    # read the contact
    res = data_store.read_contact(name)

    # check if it exists
    if res is None:
        return make_response('Contact does not exist.', 404)

    # send response
    return make_response(jsonify(res), 200)


@app.route('/contact/<string:name>', methods=['PUT'])
def update_contact(name):
    """This endpoint updates the contact by a unique name."""

    # update the contact
    res = data_store.update_contact(name, request.form)
    
    # send response
    return make_response(res['description'], res['status'])


@app.route('/contact/<string:name>', methods=['DELETE'])
def delete_contact(name):
    """This endpoint deletes the contact by a unique name."""

    # delete the contact
    res = data_store.delete_contact(name)
    
    # send response
    return make_response(res['description'], res['status'])


if __name__ == '__main__':
    app.run(
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port'],
        debug=True
    )
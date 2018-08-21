from flask import Flask, request, make_response

import json

# import configuration file
import config

# import data store and its methods for CRUD
import es_store as data_store

app = Flask(__name__)


@app.route('/contact', methods=['GET'])
def list_contacts():
    """
    This endpoint will provite a listing of all contacts, allowing for a defined pageSize
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
    res = data_store.read({
        'query_string': {
            'default_field': 'name',
            'query': query
        }
    })

    # extract requested data in range
    data = []
    for i in range(page_size * (page - 1), page_size):
        if (i >= len(res['hits']['hits'])):
            break
        data.append(res['hits']['hits'][i]['_source'])

    # send response
    return make_response(json.dumps(data), 200)


@app.route('/contact', methods=['POST'])
def create_contact():
    """This endpoint creates the contact."""

    # check if name exists in the request
    if 'name' not in request.form or not request.form['name']:
        return make_response('Invalid POST request', 400)

    # create the document
    data = {
        'name': request.form['name'],
        'phone': request.form['phone'] if 'phone' in request.form else '',
        'email': request.form['email'] if 'email' in request.form else '',
        'address': request.form['address'] if 'address' in request.form else ''
    }

    # read the data store
    res = data_store.read({
        'term': {
            '_id': data['name'].lower()
        }
    })

    # check if name already exists
    if res['hits']['total'] > 0:
        return make_response('Contact name must be unique.', 400)

    # create new document
    success = data_store.create(data)

    # send response
    if success:
        return make_response('Contact successfully created.', 201)
    else:
        return make_response('Field(s) too long', 400)


@app.route('/contact/<string:name>', methods=['GET'])
def get_contact(name):
    """This endpoint returns the contact details by a unique name."""

    # read the data store
    res = data_store.read({
        'term': {
            '_id': name.lower()
        }
    })

    # check if it exists
    if res['hits']['total'] == 0:
        return make_response('Contact does not exist.', 404)

    # send response
    return make_response(json.dumps(res['hits']['hits'][0]['_source']), 200)


@app.route('/contact/<string:name>', methods=['PUT'])
def update_contact(name):
    """This endpoint updates the contact by a unique name."""

    # read the data store
    res = data_store.read({
        'term': {
            '_id': name.lower()
        }
    })

    # check if it exists
    if res['hits']['total'] == 0:
        return make_response('Contact does not exist.', 404)

    data = {}
    if 'phone' in request.form:
        data['phone'] = request.form['phone']
    if 'email' in request.form:
        data['email'] = request.form['email']
    if 'address' in request.form:
        data['address'] = request.form['address']
    
    # update contact
    success = data_store.update(name, data)

    # send response
    if success:
        return make_response('Contact succesfully updated.', 200)
    else:
        return make_response('Field(s) too long', 400)


@app.route('/contact/<string:name>', methods=['DELETE'])
def delete_contact(name):
    """This endpoint deletes the contact by a unique name."""

    # read the data store
    res = data_store.read({
        'term': {
            '_id': name.lower()
        }
    })

    # check if it exists
    if res['hits']['total'] == 0:
        return make_response('Contact does not exist.', 404)

    # delete contact
    data_store.delete(name)

    # send response
    return make_response('Contact succesfully deleted.', 200)


if __name__ == '__main__':
    app.run(
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port'],
        debug=True
    )
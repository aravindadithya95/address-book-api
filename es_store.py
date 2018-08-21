from elasticsearch import Elasticsearch

# import configuration file
import config

# connect to elasticsearch
es = Elasticsearch(
    config.ELASTICSEARCH_CONFIG['hosts']
)


def create(index, doc_type, id, doc):
    """Creates a document in the data store."""

    es.create(
        index=index,
        doc_type=doc_type,
        id=id,
        body=doc
    )


def read(index, doc_type, id):
    """Searches unique documents in the data store."""

    res = es.search(
        index=index,
        doc_type=doc_type,
        body={
            'query': {
                'term': {
                    '_id': id
                }
            }
        }
    )

    return res['hits']['hits'][0]['_source'] if res['hits']['total'] > 0 else None


def update(index, doc_type, id, doc):
    """Updates document in the data store."""

    es.update(
        index=index,
        doc_type=doc_type,
        id=id,
        body={
            'doc': doc
        }
    )


def delete(index, doc_type, id):
    """Deletes document in the data store."""

    es.delete(
        index=index,
        doc_type=doc_type,
        id=id
    )


def search(index, doc_type, field, query, offset, size):
    """Searches documents based on query string query in the data store"""

    res = es.search(
        index=index,
        doc_type=doc_type,
        body={
            'query': {
                'query_string': {
                    'default_field': field,
                    'query': query
                }
            }
        },
        from_=offset,
        size=size
    )

    result = []
    for i in range(res['hits']['total']):
        result.append(res['hits']['hits'][i]['_source'])
    
    return result


def create_contact(data):
    """Creates a new contact in the data store."""

    # check if name exists
    if 'name' not in data or not data['name']:
        return create_response('"name" field is required.', 400)
    
    # check bounds
    if not check_bounds(data):
        return create_response('Field(s) too long.', 400)
    
    # check if contact name is unique
    if read_contact(data['name']) is not None:
        return create_response('Contact name must be unique.', 400)

    # construct the contact document
    contact = {
        'name': data['name'],
        'phone': data['phone'] if 'phone' in data else '',
        'email': data['email'] if 'email' in data else '',
        'address': data['address'] if 'address' in data else ''
    }

    # create new contact
    create(
        index='address-book',
        doc_type='contact',
        id=contact['name'].lower(),
        doc=contact
    )

    # send response
    return create_response('Contact successfully createad', 201)


def read_contact(name):
    """Reads a unique contact in the data store."""

    # read the data store
    return read(
        index='address-book',
        doc_type='contact',
        id=name.lower()
    )


def update_contact(name, data):
    """Updates a unique contact in the data store."""

    # check if the contact exists
    if read_contact(name) is None:
        return create_response('Contact does not exist.', 404)
    
    # check bounds
    if not check_bounds(data):
        return create_response('Field(s) too long.', 400)

    # construct contact
    contact = {}
    if 'phone' in data:
        contact['phone'] = data['phone']
    if 'email' in contact:
        contact['email'] = data['email']
    if 'address' in contact:
        contact['address'] = data['address']
    
    # update contact
    update(
        index='address-book',
        doc_type='contact',
        id=name.lower(),
        doc=contact
    )

    # send response
    return create_response('Contact succesfully updated.', 200)


def delete_contact(name):
    """Deletes a unique contact in the data store."""

    # check if the contact exists
    if read_contact(name) is None:
        return create_response('Contact does not exist.', 404)
    

    # delete contact
    delete(
        index='address-book',
        doc_type='contact',
        id=name.lower()
    )

    # send response
    return create_response('Contact succesfully deleted.', 200)


def search_contacts(page_size, page, query):
    """Searches based on a query in the data store."""

    # check if page number is valid
    if page <= 0:
        return create_response('Invalid page number.', 400)
    
    # search the data store
    return search(
        index='address-book',
        doc_type='contact',
        field='name',
        query=query,
        offset=page_size * (page - 1),
        size=page_size
    )


def create_response(description, status):
    """Creates a response object"""

    return {
        'description': description,
        'status': status
    }


def check_bounds(data):
    """Checks the field lengths for a contact."""

    if (
        'name' in data and len(data['name']) > 40 or
        'phone' in data and len(data['phone']) > 20 or
        'email' in data and len(data['email']) > 50 or
        'address' in data and len(data['address']) > 100
        ):
        return False
    
    return True
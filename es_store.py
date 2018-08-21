from elasticsearch import Elasticsearch

# import configuration file
import config

# connect to elasticsearch
es = Elasticsearch(
    config.ELASTICSEARCH_CONFIG['hosts']
)


def create(data, index='address-book', doc_type='contact'):
    """Creates a document in the data store."""

    # check bounds
    if not checkBounds(data):
        return False

    es.create(
        index=index,
        doc_type=doc_type,
        id=data['name'].lower(),
        body=data
    )
    return True


def read(query, index='address-book', doc_type='contact'):
    """Searches for documents in the data store."""

    return es.search(
        index=index,
        doc_type=doc_type,
        body={
            'query': query
        }
    )


def update(id, query, index='address-book', doc_type='contact'):
    """Updates document in the data store."""

    # check bounds
    if not checkBounds(query):
        return False

    es.update(
        index=index,
        doc_type=doc_type,
        id=id.lower(),
        body={
            'doc': query
        }
    )
    return True


def delete(id, index='address-book', doc_type='contact'):
    """Deletes document in the data store."""

    es.delete(
        index=index,
        doc_type=doc_type,
        id=id.lower()
    )
    return True


def checkBounds(data):
    """Checks the field lengths"""

    if (
        'name' in data and len(data['name']) > 40 or
        'phone' in data and len(data['phone']) > 20 or
        'email' in data and len(data['email']) > 50 or
        'address' in data and len(data['address']) > 100
        ):
        return False
    else:
        return True
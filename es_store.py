from elasticsearch import Elasticsearch

# import configuration file
import config

# connect to elasticsearch
es = Elasticsearch(
    config.ELASTICSEARCH_CONFIG['hosts']
)


def create(data, index='address-book', doc_type='contact'):
    """Creates a document in the data store."""

    es.create(
        index=index,
        doc_type=doc_type,
        id=data['name'],
        body=data
    )


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

    es.update(
        index=index,
        doc_type=doc_type,
        id=id,
        body={
            'doc': query
        }
    )


def delete(id, index='address-book', doc_type='contact'):
    """Delete document in the data store."""

    es.delete(
        index=index,
        doc_type=doc_type,
        id=id
    )   
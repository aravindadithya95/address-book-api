from elasticsearch import Elasticsearch

# import configuration file
import config

# connect to elasticsearch
es = Elasticsearch(
    config.ELASTICSEARCH_CONFIG['hosts']
)

# define data model
body = {
    'mappings': {
        'contact': {
            'properties': {
                'name': { 'type': 'text' },
                'phone': { 'type': 'text' },
                'email': { 'type': 'text' },
                'address': { 'type': 'text' }
            }
        }
    }
}

# delete index if it already exists
es.indices.delete('address-book')

# create index in elasticsearch
es.indices.create(
    index='address-book',
    body=body
)
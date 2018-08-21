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
                'name': { 'type': 'keyword', 'ignore_above': 40 },
                'phone': { 'type': 'keyword', 'ignore_above': 20 },
                'email': { 'type': 'keyword', 'ignore_above': 50 },
                'address': { 'type': 'keyword', 'ignore_above': 100 }
            }
        }
    }
}

# delete index if it already exists
if es.indices.exists(index='address-book'):
    es.indices.delete('address-book')

# create index in elasticsearch
es.indices.create(
    index='address-book',
    body=body
)
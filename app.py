import config

from flask import Flask
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(
    config.ELASTICSEARCH_CONFIG['hosts']
)

@app.route('/')
def test():
    return "Hello World"

if __name__ == '__main__':
    app.run(
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port']
    )
# Address Book API
This code provides APIs to perform CRUD and search on address book entries backed by Elasticsearch.

## Getting Started
### Setting up the environment
- Make sure you have **Python 2.x** installed in your machine.
- Install `pip` and `virtualenv`.
- Activate `virtualenv` and install `flask` and `elasticsearch` using `pip`.
- Download and run the `Elasticsearch` server.
- Download or clone a local copy of this repository.
- Hosts and port numbers are configurable in `config.py`.
- Run `python es_model.py` to setup the model structure for Elasticsearch.
- Run `python test.py` to run the testcases.
- Run `python app.py` to run the application and get access to the API endpoints.

### API endpoints
The application has the following endpoints:

- `GET​ /contact?pageSize={}&page={}&query={}`
- `POST​ /contact`
- `GET​ /contact/{name}`
- `PUT​ /contact/{name}`
- `DELETE​ /contact/{name}`
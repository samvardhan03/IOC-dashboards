import requests
from datetime import datetime
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['net_zero_dashboard']

# Data Fetching and Pre-processing
def fetch_data(api_endpoints):
    data = {}
    with ThreadPoolExecutor() as executor:
        futures = []
        for metric, endpoint in api_endpoints.items():
            futures.append(executor.submit(requests.get, endpoint))
        for future in futures:
            response = future.result()
            data[response.url] = response.json()
    return data

def preprocess_data(raw_data):
    # Perform any necessary data cleaning, transformation, or normalization
    processed_data = raw_data  # Replace with your pre-processing logic
    return processed_data

# Data Storage
def store_data(processed_data):
    timestamp = datetime.now()
    data_doc = {'timestamp': timestamp, 'data': processed_data}
    db['data'].insert_one(data_doc)

def fetch_and_store_data():
    api_endpoints = {
        'GHG emissions': 'https://example.com/api/ghg',
        'Energy consumption': 'https://example.com/api/energy',
        'Cost savings': 'https://example.com/api/cost'
    }
    raw_data = fetch_data(api_endpoints)
    processed_data = preprocess_data(raw_data)
    store_data(processed_data)

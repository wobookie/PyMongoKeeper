import pymongo as mongo
import json
import bson
from bson import json_util
from bson import ObjectId

mongo_db_version = None
mongo_client = None
mongo_db = None

def init_mongo_connection(username, password):
    global mongo_client
    global mongo_db_version

    # mongo_host = 'localhost'
    # auth_db = 'admin'
    # conn_str = 'mongodb://' + username + ':' + password + '@' + mongo_host + '/' + auth_db

    mongo_host = 'gcp-singapore-experimental-00-inu5u.gcp.mongodb.net'
    auth_db = 'test?retryWrites=true'
    conn_str = 'mongodb+srv://' + username + ':' + password + '@' + mongo_host + '/' + auth_db

    try:
        mongo_client = mongo.MongoClient(conn_str)
        mongo_db_version = mongo_client.server_info().get('version')

    except Exception as error:
        print('Could not connect to server: ', error)
        return False

    return True


def init_mongo_db():
    global mongo_db

    try:
        mongo_db = mongo_client['MongoKeeperDB']

    except mongo.errors.InvalidName as error:
        print('Could not initialise database: ', error)
        return False

    return True


def get_mongo_collections():
    col_names = mongo_db.collection_names()

    return col_names


def find_documents(filter='{}', page_size=10, oid = None):
    json_docs = []
    collection = mongo_db['payments']
    query = {"$and": []}
    query["$and"].append(json.loads(filter))

    if oid:
        query["$and"].append({'_id': {'$gt': ObjectId(oid)}})

    cursor = collection.find(query).limit(page_size)

    for doc in cursor:
        json_doc = json.dumps(doc, default=json_util.default)
        json_docs.append(json_doc)

    return json_docs


def find_all_documents():
    collection = mongo_db['payments']

    return json.dumps(collection.find())


def count_documents(query = '{}'):
    collection = mongo_db['payments']

    return collection.count_documents(json.loads(query))

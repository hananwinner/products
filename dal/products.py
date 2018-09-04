import pymongo
import yaml

with open("config/config.yaml", "r") as fdr:
    config = yaml.load(fdr)

client = None
config = config["mongo"]
connection_params = {k:config[k] for k in ["host", "port"]}
db_name = config["db"]
COLLECTION_NAME = "products"
db = None
collection = None


def connect():
    global client
    global db
    global collection
    client = pymongo.MongoClient(**connection_params)
    db = client[db_name]
    collection = db[COLLECTION_NAME]


def disconnect():
    if client is not None:
        client.close()


def make_doc(product_name,photo_url,barcode,sku,price_cents,producer):
    return {
        "product_name": product_name,
        "photo_url": photo_url,
        "barcode": barcode,
        "sku":sku,
        "price_cents": price_cents,
        "producer": producer
    }


def process_new_entry(product_name, photo_url, barcode, sku, price_cents, producer):
    collection.update_one(
        filter={"sku": sku},
        update=make_doc(product_name,photo_url,barcode,sku,price_cents,producer),
        upsert=True)


def get_products(producer=None, before=None, after=None, count=0):
    _filter = {} if producer is None else {"producer": producer}
    if after is not None:
        _filter["sku"] = {"$gt": after}
        _sort = [("sku", pymongo.ASCENDING)]
        return list(collection.find(filter=_filter, sort=_sort, limit=count))
    elif before is not None:
        _filter["sku"] = {"$gt" : before}
        _sort = [("sku", pymongo.DESCENDING)]
        result = list(collection.find(filter=_filter, sort=_sort, limit=count))
        result.reverse()
        return result
    else:
        _sort = [("sku", pymongo.ASCENDING)]
        return list(collection.find(filter=_filter, sort=_sort, limit=count))


def clear():
    collection.delete_many(filter={})

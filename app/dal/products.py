import pymongo

_COLLECTION_NAME = "products"

dal_products = None


def create():
    return DalProducts()


class DalProducts(object):
    def __init__(self):
        self._client = None
        self._db = None
        self._collection = None

    def connect(self, config):
        connection_params = {k: config[k] for k in ["host", "port"]}
        db_name = config["db"]
        self._client = pymongo.MongoClient(**connection_params)
        self._db = self._client[db_name]
        self._collection = self._db[_COLLECTION_NAME]

    def disconnect(self):
        if self._client is not None:
            self._client.close()

    @staticmethod
    def _make_doc(product_name, photo_url, barcode, sku, price_cents, producer):
        return {
            "product_name": product_name,
            "photo_url": photo_url,
            "barcode": barcode,
            "sku": sku,
            "price_cents": price_cents,
            "producer": producer
        }

    def process_new_entry(self, doc):
        self._ensure_indexes()
        sku = doc["sku"]
        self._collection.replace_one(
            filter={"sku": sku},
            replacement=doc,
            upsert=True)

    def get_products(self, producer=None, before=None, after=None, count=0):
        _filter = {} if producer is None else {"producer": producer}
        if after is not None:
            _filter["sku"] = {"$gt": after}
            _sort = [("sku", pymongo.ASCENDING)]
            return list(self._collection.find(filter=_filter, sort=_sort, limit=count))
        elif before is not None:
            _filter["sku"] = {"$lt" : before}
            _sort = [("sku", pymongo.DESCENDING)]
            result = list(self._collection.find(filter=_filter, sort=_sort, limit=count))
            result.reverse()
            return result
        else:
            _sort = [("sku", pymongo.ASCENDING)]
            return list(self._collection.find(filter=_filter, sort=_sort, limit=count))

    def clear(self):
        self._collection.delete_many(filter={})

    def _ensure_indexes(self):
        sku_idx = pymongo.IndexModel([("sku", pymongo.ASCENDING)])
        producer_idx = pymongo.IndexModel([("producer", pymongo.ASCENDING)])
        self._collection.create_indexes([sku_idx, producer_idx])

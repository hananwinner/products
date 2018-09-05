import unittest
from dal import products as dal_products
import json
from test.config import mongo_config

with open("test/dal/test_products.json") as fdr:
    test_products = json.loads(fdr.read())

unique_entries = test_products["unique_entries"]
data = test_products["data"]


class TestProducts(unittest.TestCase):
    def setUp(self):
        dal_products.connect(mongo_config)
        dal_products.clear()
        [dal_products.process_new_entry(p) for p in data]
        self.assertEqual(len(dal_products.get_products()), unique_entries)

    def test(self):
        page = dal_products.get_products(count=2)
        self.assertEqual(len(page), 2)
        self.assertEqual(page[0]["sku"], 42534)
        page = dal_products.get_products(after=64124,count=2)
        self.assertEqual(len(page), 2)
        self.assertEqual(page[0]["sku"], 65908)
        self.assertEqual(page[1]["sku"], 81263)
        page = dal_products.get_products(before=1070373, count=3)
        self.assertEqual(len(page), 3)
        self.assertEqual(page[0]["sku"], 81263)
        self.assertEqual(page[1]["sku"], 99915)

    def tearDown(self):
        dal_products.clear()
        self.assertEqual(len(dal_products.get_products()), 0)
        dal_products.disconnect()

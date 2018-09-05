from pika_client.factory import create_persistent_async_consumer
import dal.products as dal_products
import json


def _on_message(body):
    doc = json.loads(body.decode("utf-8"))
    dal_products.process_new_entry(doc)


def create(config):
    return create_persistent_async_consumer(config["connection"], config["route"], _on_message)

from pika_client.factory import create_persistent_async_consumer
import json


def _consumer_callback(dal):
    def _on_message(body):
        doc = json.loads(body.decode("utf-8"))
        dal.process_new_entry(doc)
    return _on_message


def create(config, dal, **kwargs):
    return create_persistent_async_consumer(config["connection"], config["route"], _consumer_callback(dal)
                                            , queue=config["route"]["queue"], **kwargs)

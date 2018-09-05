import dal.products as dal_products
from api.products import app
import signal
import sys
from modules import consumer
from config import mongo_config, consumer_config


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit()


def exit():
    consumer.stop()
    dal_products.disconnect()
    sys.exit(0)


if __name__ == "__main__":
    dal_products.connect(mongo_config)
    consumer = consumer.create(consumer_config)
    consumer.start()
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    app.run()




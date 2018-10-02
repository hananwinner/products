import updater.consumer as consumer
import updater.config as config
from app.dal.products import create as create_dal
import logging.config
import sys

config_path = sys.argv[1] if len(sys.argv) > 1 else "updater/config/docker_config.yaml"

config.create(config_path)

logging.config.dictConfig(config.log_dict_config)
log = logging.getLogger("updater")


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit()


def exit():
    consumer.stop()
    dal_products.disconnect()
    sys.exit(0)


if __name__ == "__main__":
    dal_products = create_dal()
    dal_products.connect(config.mongo_config)

    consumer = consumer.create(config.consumer_config, dal_products, log=log)
    consumer.start()




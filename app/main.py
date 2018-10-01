from  dal.products import DalProducts
# from api.products import app
import signal
import sys
from modules import consumer
from config import mongo_config, consumer_config
import config
from flask import Flask, request, abort
from bson.json_util import dumps
from dal.products import create as create_dal
import logging
import logging.config
import time

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit()


def exit():
    consumer.stop()
    dal_products.disconnect()
    sys.exit(0)

dal_products = create_dal()

config_path = sys.argv[1] if len(sys.argv) > 1 else "config/docker_config.yaml"

config.create(config_path)

print('config.log_dict_config')
print(config.log_dict_config)
logging.config.dictConfig(config.log_dict_config)
log = logging.getLogger("products")


print('mongo_config')
print(config.mongo_config)
log.debug('connect mongo.. {}'.format(config.mongo_config))
dal_products.connect(config.mongo_config)
log.debug('finish connect mongo {} {} {}'.format(dal_products._client, dal_products._db, dal_products._collection))

consumer = consumer.create(config.consumer_config, dal_products, log=log)
consumer.start()
log.debug('consumer {}'.format(consumer))
# signal.signal(signal.SIGINT, signal_handler)
# print('Press Ctrl+C to exit')
time.sleep(5)
app = Flask(__name__)


@app.route("/products/")
def products():
    try:
        log.debug("products args {}".format(request.args))
        producer = request.args.get("producer")
        before = request.args.get("before")
        if before is not None:
            before = int(before)
        after = request.args.get("after")
        if after is not None:
            after = int(after)
        count = request.args.get("count", 0)
        if count is not None:
            count = int(count)
        r = dal_products.get_products(producer, before, after, count)
        return dumps(r)
    except ValueError:
        abort(400)





if __name__ == "__main__":



    app.run(host='0.0.0.0', debug=True, port=80)
    # app.run()




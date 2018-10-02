from dal.products import DalProducts
import signal
import sys
import config
from flask import Flask, request, abort
from bson.json_util import dumps
from dal.products import create as create_dal
import logging.config
import time

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit()


def exit():
    dal_products.disconnect()
    sys.exit(0)

dal_products = create_dal()

config_path = sys.argv[1] if len(sys.argv) > 1 else "config/docker_config.yaml"

config.create(config_path)

logging.config.dictConfig(config.log_dict_config)
log = logging.getLogger("products")
dal_products.connect(config.mongo_config)

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




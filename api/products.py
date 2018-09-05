from flask import Flask, request, jsonify, abort
from bson.json_util import dumps
import dal

app = Flask(__name__)


@app.route("/products/")
def products():
    try:
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
        r = dal.products.get_products(producer, before, after, count)
        return dumps(r)
    except ValueError:
        abort(400)


if __name__ == "__main__":
    app.run(debug=True)

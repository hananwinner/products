import dal.products as dal_products
from api.products import app
import signal
import sys


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit()


def exit():
    dal_products.disconnect()
    sys.exit(0)


if __name__ == "__main__":
    dal_products.connect()
    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C to exit')
    app.run()




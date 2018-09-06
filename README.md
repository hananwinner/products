Products Service

Requires:
* DB implemented by MongoDB
* RabbitMQ

Responsible for Products data.
Consumed using RabbitMq Queue.
Retained using MongoDB.
Exposed through REST API (python flask) at http://127.0.0.1:5000/products/

made for python 3.5.2

Run: python3.5 main.py

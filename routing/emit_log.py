#!/usr/bin/env python
import pika
import sys
from random import randint

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

severities = ["info", "warning", "error"]
severity = severities[randint(0, 2)]

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)

print(" [x] Sent %r %r" % (severity, message))

connection.close()

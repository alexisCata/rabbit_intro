#!/usr/bin/env python
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')


result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = ["info", "warning", "error"]
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_qos(prefetch_count=1)  # rabbit only sends a new message to the worker when
# it has processed and acknowledged the previous message

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True
                      )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

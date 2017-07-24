#!/usr/bin/env python
import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")


channel.basic_qos(prefetch_count=1)  # rabbit only sends a new message to the worker when
# it has processed and acknowledged the previous message

channel.basic_consume(callback,
                      queue='task_queue'
                      # ,no_ack=True
                      )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
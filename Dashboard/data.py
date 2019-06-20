import pika
import time
import sys
import ssl
import argparse
import datetime
import logging
import json
import uuid
import os

def callback(ch, method, properties, body):
    print(" [x] rk: {}, headers: {}, msg: {}, ts: {}".
          format(method.routing_key, properties.headers, body,
                 datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")))
    outFile =  open('data.txt', 'wb')
    outFile.write(body)
    outFile.close( )    
    
logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description="AMQP client")
parser.add_argument("-v", "--vhost", help='AMQP virtual host name, default: IOTSP_INTERNAL', default='IOTSP_INTERNAL', dest='vhost')
parser.add_argument("-p", "--port", help='AMQP virtual host ssl port, default: 5671', default=5671, dest='port', type=int)
parser.add_argument("-u", "--user", help='AMQP user name, default: test', default='test', dest='user')
parser.add_argument("-P", "--password", help='AMQP user password, default: test', default='test', dest='password')
parser.add_argument("-e", "--exchange", help='AMQP exchange name, default: unknown', default='unknown', dest='exchange')
parser.add_argument("-l", "--label", help='AMQP label,  must be in format a=b, default: None', default=None, dest='label')
parser.add_argument("-r", "--rmqphost", help='AMQP host ip, default: 127.0.0.1', default='127.0.0.1', dest='rmqp_host')
parser.add_argument("-k", "--routingkey", help='AMQP routing key, default: dev2app', default='dev2app', dest='routing_key')
parser.add_argument('--version', action='version', version='1.0')
args = parser.parse_args()

queue_name = args.user + ':' + datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
# uncomment line below to use Durable Q in sync with Declar Queue durable options - XX
#queue_name = 'DurableQ'
credentials = pika.PlainCredentials(args.user, args.password)

try:
    # Setup our ssl options
    context = ssl.create_default_context(cafile="cert.crt")
    parameters = pika.ConnectionParameters(
                 host=args.rmqp_host, virtual_host=args.vhost,
                 ssl_options=pika.SSLOptions(context), credentials = credentials, port=args.port)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, passive=False,
                          #durable=True, exclusive=False, auto_delete=False) # Declare a Durable queue - 10 mins on queue inactivity supported, use fixed queue_name XX
                          durable=False, exclusive=False, auto_delete=True) # Declare a queue - Data is lost when the consumer was down
    if args.label:
        lbl = args.label.split('=')
        channel.queue_bind(exchange=args.exchange, queue=queue_name, routing_key=args.routing_key,
                        arguments = {lbl[0]:lbl[1], 'x-match':'all'})
    else:
        channel.queue_bind(exchange=args.exchange, queue=queue_name, routing_key=args.routing_key)
except IndexError:
    logging.error("label format error, should be < x=y >!")
    sys.exit()
except Exception as e:
    logging.error(args.rmqp_host + " Connection error!")
    logging.error(" %s", str(e))
    logging.error(type(e))
    sys.exit()
print(' [*] Waiting for data [tags: {}]. To exit press CTRL+C'.format(args.label))
channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
    main()

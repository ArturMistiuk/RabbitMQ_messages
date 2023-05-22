import pika
from bson import ObjectId

from models import User
from producer import connection_Mongo

creds = pika.PlainCredentials('guest', 'guest')
conn_string = pika.ConnectionParameters(host='localhost', port=5672, credentials=creds)
connection = pika.BlockingConnection()

channel = connection.channel()
channel.queue_declare(queue='e_messages')


def callback(ch, method, properties, body):
    user_id = body.decode()
    if ObjectId.is_valid(user_id):
        print(f'Sending to {user_id}...')
        user = User.objects(id=user_id).first()
        user.received = True
        user.save()
        print(f'Message to {user_id} has been sent')


channel.basic_consume(queue='e_messages', on_message_callback=callback)

channel.start_consuming()


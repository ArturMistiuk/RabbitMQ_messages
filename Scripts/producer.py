import pika
from mongoengine import connect
from faker import Faker

from models import User


# Connection to MongoDB
connection_Mongo = connect('users', alias='default')  # conn_str = 'mongodb://admin:admin@localhost:27017'


# Connection to RabbitMQ
creds = pika.PlainCredentials('guest', 'guest')
conn_string = pika.ConnectionParameters(host='localhost', port=5672, credentials=creds)
connection_Rabbit = pika.BlockingConnection(conn_string)

# Creating channel for emails messages
channel = connection_Rabbit.channel()
# Clean queue from data
# channel.queue_delete(queue='e_messages')
channel.queue_declare(queue='e_messages')


def send_contacts_id(list_of_users_id):
    for user_id in list_of_users_id:
        channel.basic_publish(exchange='', routing_key='e_messages', body=str(user_id).encode())

    connection_Rabbit.close()


def make_users():
    fake_data = Faker()
    fake_users = [{'fullname': fake_data.name(), 'email': fake_data.email()} for _ in range(11)]
    return fake_users


def fill_db(users_list):
    for user in users_list:
        new_user = User(fullname=user['fullname'], email=user['email'])
        new_user.save()


if __name__ == '__main__':
    # Filling db with fake users
    User.objects.delete()
    users = make_users()
    fill_db(users)
    users_id = list(User.objects().values_list('id'))
    send_contacts_id(users_id)

import os

import django

import paho.mqtt.client as mqtt

os.environ['DJANGO_SETTINGS_MODULE'] = 'mqttchat.settings'
django.setup()

from app.models import Topic, Subscribe, Message

def on_connect( client, userdata, flags, rc):
    topic_list = Topic.objects.all()
    topics = []
    for t in topic_list:
        topic = t.topic_name
    	topics.append((str(topic), 2))
    client.subscribe(topics)

def on_message(client, userdata, message):
	body = eval(message.payload)
	topic = message.topic
	topic_id = Topic.objects.get(topic_name=topic)
	Message.objects.create(user_id=body['user_id'], topic_id=topic_id.id, message=body['message'])
	


broker_address="localhost"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message=on_message
client.username_pw_set('gun','metal')
client.connect(broker_address)
client.loop_forever()
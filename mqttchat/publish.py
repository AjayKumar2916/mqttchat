import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
	print str(message.payload.decode("utf-8"))

broker_address="localhost"
client = mqtt.Client()
client.on_message=on_message
client.username_pw_set('gun','metal')
client.connect(broker_address)
client.publish("test4","Djangathon")
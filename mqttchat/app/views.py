# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

import paho.mqtt.client as mqtt


from app.models import Topic, Subscribe, Message

def login(request, template_name="login.html"):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('dashboard'))
	if request.POST:
		username = request.POST.get('username','')
		password = request.POST.get('password','')
		user = auth.authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				topic = Subscribe.objects.filter(user_id=user.id).latest('id')
				return HttpResponseRedirect('/dashboard/?topic_id=%s'%topic.topic_id)
			
		messages.error(request,"Invalid Login Credentials!")
		return HttpResponseRedirect(reverse('login'))
	return TemplateResponse(request, template_name)

def dashboard(request, template_name="dashboard.html"):
	args = {}
	user = request.user
	args['user'] = user
	topic_list = Subscribe.objects.filter(user_id = user.id).order_by('-id')
	args['topic_list'] = topic_list	
	if request.method == "GET":
		topic_id = request.GET.get('topic_id')
		args['topicid'] = topic_id
		topic_name = Topic.objects.get(id = topic_id).topic_name	
		args['topic_name'] = topic_name
	return TemplateResponse(request, template_name, args)	

@csrf_exempt
def message(request,topic_id):
	args = {}
	message_data_list = []
	message_list = Message.objects.filter(topic_id = topic_id).order_by('-timestamp')	
	for message in message_list:
		message_data = {}
		message_data['username'] = message.username()
		message_data['message'] = message.message
		timestamp = datetime.strftime(message.timestamp, '%d-%m-%Y %I:%M %p')
		message_data['timestamp'] = str(timestamp)
		message_data_list.append(message_data)
	args['message_data_list'] = message_data_list
	return JsonResponse(args)	

@csrf_exempt
def publish(request):
	args = {}
	user_id = request.POST.get("user_id")
	topic = request.POST.get("topic")
	message = request.POST.get("message")
	username = User.objects.get(id=int(user_id)).username
	msg = {'user_id': user_id ,'message': message}
	broker_address="localhost"
	client = mqtt.Client()
	client.username_pw_set('gun','metal')
	client.connect(broker_address)
	client.publish(topic, str(msg))
	args['message'] = message
	args['username'] = username
	args['timestamp'] = datetime.strftime(datetime.now(), '%d-%m-%Y %I:%M %p')
	return JsonResponse(args)	

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('login'))


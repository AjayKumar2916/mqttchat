# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):
	topic_name = models.CharField(verbose_name='Topic Name',max_length=255, blank=True, null=False)

class Subscribe(models.Model):
	user_id = models.CharField(verbose_name='User ID', max_length=255, blank=False, null=False)
	topic_id = models.CharField(verbose_name='Topic ID', max_length=255, blank=False, null=False)

	def topicname(self):
		topic = Topic.objects.get(id=self.topic_id).topic_name
		return topic

class Message(models.Model):
	user_id = models.CharField(verbose_name='User ID', max_length=255, blank=False, null=False)
	topic_id = models.CharField(verbose_name='Topic ID', max_length=255, blank=False, null=False)
	message = models.CharField(verbose_name='Message', max_length=255, blank=False, null=False)
	timestamp =  models.DateTimeField(verbose_name='Time Stamp', auto_now_add=True)

	def username(self):
		user = User.objects.get(id=int(self.user_id)).username
		return user

	 	
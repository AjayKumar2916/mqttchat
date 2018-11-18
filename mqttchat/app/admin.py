# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from app.models import Topic, Subscribe, Message

class TopicAdmin(admin.ModelAdmin):
	list_display = ['id', 'topic_name']

class SubscribeAdmin(admin.ModelAdmin):
	list_display = ['id', 'user_id', 'topic_id']


class MessageAdmin(admin.ModelAdmin):
	list_display = ['id', 'user_id', 'topic_id', 'message', 'timestamp']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Message, MessageAdmin)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
#from django.utils import timezone
from datetime import datetime

# Create your models here.

class gamer(models.Model):
    names = models.CharField(max_length=100)
    phone_number = models.IntegerField(unique=True)
    points = models.IntegerField(default=0)
    time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.names +' '+ str(self.points)

class sessionlevels(models.Model):
    session_id = models.CharField(max_length=1000,unique=True)
    phone_number = models.IntegerField()
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.session_id

class question(models.Model):
    gamer = models.ForeignKey(gamer)
    session = models.CharField(max_length=100)
    question_title = models.CharField(max_length=1000)
    question_subject = models.CharField(max_length=1000)
    question_options = JSONField()
    question_answer = models.CharField(max_length=1)
    time = models.DateTimeField(default=datetime.now)
    won = models.BooleanField(default=False)

    def __unicode__(self):
        return self.question_title

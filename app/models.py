# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class student(models.Model):
    names = models.CharField(max_length=100)
    email = models.CharField(max_length=30)

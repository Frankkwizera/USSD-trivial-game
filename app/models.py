# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class gamer(models.Model):
    names = models.CharField(max_length=100)
    phone_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.names + str(self.phone_number)

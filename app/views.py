# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import IntegrityError
from .models import *
from .utility import *
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        response = ""

        #Throwing back another input text for names
        pattern = "^\d+\*\d{10}$"
        m = re.match(pattern,text)
        if m:
            response = "CON Enter your names "
            return HttpResponse(response)

        #Saving a new user after submitting required fields
        user_details_pattern = "^\d+\*\d{10}\D+\s\D+$"
        p = re.match(user_details_pattern,text)

        if p:
            detailSplit = re.split(r'\*',text)
            #New gamer
            try:
                gamer.objects.create(names = detailSplit[2],phone_number=detailSplit[1])
                response = "END You have been registered successfully dial again to start answering questions"
            except IntegrityError:
                response = "END Phone Number is already registered"
            return HttpResponse(response)

        textSplit = re.split(r'\*',text)
        #finding 99 for terminating trivial game
        n = re.compile("99")
        terminate = filter(n.match,textSplit)

        if terminate:
            response = "END Trivial Game terminated \n You have 0 points"
            return HttpResponse(response)

        if text == "":
            response = "CON Trivial Questions USSD System \n \n"
            response += "1. Start Game \n 2. Register"

        if text == "2":
            response = "CON Your Phone Number \n"

        if text == "1":
            response = "CON Trivial Questions USSD System \n \n"
            response += "1. Mathematics \n 2. Biology \n 3. Physics \n 4. Chemistry \n 99. End this Trivial game"

        elif text == "1*1":
            response = trivial(request,'Mathematics')

        elif text == "1*2":
            response = trivial(request,'Biology')

        elif text == "1*3":
            response = trivial(request,'Physics')

        elif text == "1*4":
            response = trivial(request,'Chemistry')

        return HttpResponse(response)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db import IntegrityError
from datetime import datetime
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

        textSplit = re.split(r'\*',text)

        #initiating a level or processing
        try:
            sessionlevels.objects.create(session_id = session_id, phone_number=phone_number,level=0)
        except IntegrityError:
            current_session = sessionlevels.objects.filter(session_id = session_id).first()

            #if user is at level 4
            if current_session.level == 4:
                r = re.compile("\D")
                charsInText = filter(r.match,textSplit)
                if charsInText:
                    chosenChar = charsInText[len(charsInText)-1]
                    return HttpResponse(checkAnswer(chosenChar,session_id))



        #Saving a new user after submitting required fields
        user_details_pattern = "^\d+\*\d{10}\D+\s\D+$"
        p = re.match(user_details_pattern,text)

        if p:
            detailSplit = re.split(r'\*',text)
            #New gamer
            try:
                gamer.objects.create(names = detailSplit[2],phone_number='25'+str(detailSplit[1]),time=datetime.now())
                response = "END You have been registered successfully dial again to start answering questions"
            except IntegrityError:
                response = "END Phone Number is already registered"
            return HttpResponse(response)

        #Throwing back another input text for names
        pattern = "^\d+\*\d{10}$"
        m = re.match(pattern,text)
        if m:
            response = "CON Enter your names "
            return HttpResponse(response)

        #finding 99 for terminating trivial game
        n = re.compile("99")
        terminate = filter(n.match,textSplit)

        if terminate:
            trivia_gamer = gamer.objects.filter(phone_number=phone_number).first()
            response = "END Trivial Game terminated \n You have "+str(trivia_gamer.points)+" points"
            return HttpResponse(response)
        #End of terminating

        if text == "":
            #checking if user exist
            user = gamer.objects.filter(phone_number= phone_number[1:]).first()
            if user is not None:
                response = "CON Welcome "+str(user.names)+" \n \n"
                response += "1. Start Game"
            else:
                response = "CON Welcome for the first time \n \n"
                response += "2. Register your information "

        if text == "2":
            response = "CON Your Phone Number \n"

        if text == "1":
            response = "CON Trivial Questions USSD System \n \n"
            response += "1. Mathematics \n 2. Biology \n 3. Physics \n 4. Chemistry \n 99. End this Trivial game"

        elif text == "1*1":
            response = trivial('Mathematics',session_id)

        elif text == "1*2":
            response = trivial('Biology',session_id)

        elif text == "1*3":
            response = trivial('Physics',session_id)

        elif text == "1*4":
            response = trivial('Chemistry',session_id)

        return HttpResponse(response)

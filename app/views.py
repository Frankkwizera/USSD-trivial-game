# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.
def trivial(request,subject):

    if request.session.has_key('previousQuestion'):
        print request.session['previousQuestion']
    else:
        print "No session saved under previousQuestion"

    url = 'https://questions.aloc.ng/api/q?subject='+subject
    req = requests.get(url)
    result = req.json()

    #if request.session.has_key('previousQuestion'):
    #    pass
    #else:
    request.session['previousQuestion'] = result
    request.session.save()

    answers = ""
    question = result['data']['question']
    options = result['data']['option']
    rightAnswer = result['data']['answer']

    for i,v in options.iteritems():
        answers += str(i) +". "+str(v)+" \n"

    response = "CON "+ subject + " Question \n "+ question +"\n \n"+ answers +"\n 99. End this Trivial game"

    return response

def checkAnswer(request,chosenChar):
    print request.session['previousQuestion']
    if chosenChar == "a":
        response = trivial(request,'Mathematics')
    return response

@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        response = ""

        textSplit = re.split(r'\*',text)
        r = re.compile("\D")
        charsInText = filter(r.match,textSplit)

        if charsInText:
            chosenChar = charsInText[len(charsInText)-1]
            return HttpResponse(checkAnswer(request,chosenChar))

        if text == "":
            response = "CON Trivial Questions USSD System \n \n"
            response += "1. Mathematics \n 2. Biology \n 3. Physics \n 4. Chemistry \n 99. End this Trivial game"

        elif text == "1":
            response = trivial(request,'Mathematics')

        elif text == "2":
            response = trivial(request,'Biology')

        elif text == "3":
            response = trivial(request,'Physics')

        elif text == "4":
            response = trivial(request,'Chemistry')

        elif text == "99":
            response = "END Trivial Game terminated"

        elif text == "1*99":
            response = "END Trivial Game terminated"

        elif text == "2*99":
            response = "END Trivial Game terminated"

        elif text == "3*99":
            response = "END Trivial Game terminated"

        elif text == "4*99":
            response = "END Trivial Game terminated"

        return HttpResponse(response)

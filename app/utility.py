from __future__ import unicode_literals
import requests
from datetime import datetime
from .models import *


def trivial(subject,session_id):
    url = 'https://questions.aloc.ng/api/q?subject='+subject
    req = requests.get(url)
    result = req.json()

    answers = ""
    trivia_question = result['data']['question']
    options = result['data']['option']
    rightAnswer = result['data']['answer']

    for i,v in options.iteritems():
        answers += str(i) +". "+str(v)+" \n"

    #upgrading session level
    session = sessionlevels.objects.filter(session_id=session_id).first()
    session.level = 4
    session.save()
    #gamer
    trivia_gamer = gamer.objects.filter(phone_number = session.phone_number).first()
    #saving a queston
    question.objects.create(gamer = trivia_gamer,session = session_id,
                            question_title = trivia_question,
                            question_subject = subject,
                            question_options = options,
                            question_answer = rightAnswer,
                            time = datetime.now())


    response = "CON "+ subject + " Question \n "+ trivia_question +"\n \n"+ answers +"\n 99. End this Trivial game"
    return response

def checkAnswer(chosenChar,session_id):
    attempted_queston = question.objects.filter(session=session_id).latest('time')
    trivia_gamer = attempted_queston.gamer
    if chosenChar == attempted_queston.question_answer:
        print "success"
        attempted_queston.won = True
        trivia_gamer.points += 10
        attempted_queston.save()
        trivia_gamer.save()
    else:
        print "loss"
    return trivial(attempted_queston.question_subject,session_id)

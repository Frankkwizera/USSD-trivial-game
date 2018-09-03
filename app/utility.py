import requests

def trivial(request,subject):
    url = 'https://questions.aloc.ng/api/q?subject='+subject
    req = requests.get(url)
    result = req.json()

    answers = ""
    question = result['data']['question']
    options = result['data']['option']
    rightAnswer = result['data']['answer']

    for i,v in options.iteritems():
        answers += str(i) +". "+str(v)+" \n"

    response = "CON "+ subject + " Question \n "+ question +"\n \n"+ answers +"\n 99. End this Trivial game"

    return response

def checkAnswer(request,chosenChar):
    if chosenChar == "a":
        response = trivial(request,'Mathematics')
    return response

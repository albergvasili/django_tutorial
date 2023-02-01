from django.shortcuts import render
from django.http import HttpResponse
from .models import Question


def index(req):
    latest_questions_list = Question.objects.order_by('pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_questions_list])
    return HttpResponse(output)


def detail(req, question_id):
    return HttpResponse(f'You are looking at question {question_id}')


def results(req, question_id):
    res = f'You are looking at results of question {question_id}'
    return HttpResponse(res)


def vote(req, question_id):
    return HttpResponse(f'You are voting on question {question_id}')

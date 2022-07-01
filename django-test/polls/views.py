from django.shortcuts import render,get_object_or_404
from django.db import reset_queries
from django.http import HttpResponse,Http404
from django.template import loader
from .models import Question

def index(request):
    # # -是降序，最新的在前面
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # # 这里拼接setting的TEMPLATES，加载template
    # template = loader.get_template('polls/index.html')
    # # context是一个dict
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return HttpResponse(template.render(context, request))

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question= Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')
    
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
     

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
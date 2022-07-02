from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic 
from django.utils import timezone
from .models import Question,Choice



#  class 写法
#  generic.ListView
class IndexView(generic.ListView):
    # 这里没有提供model，怎么知道什么模型，应该是定义了context_object_name 和 get_querset的原因
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        # return Question.objects.order_by('-pub_date')[:5]

#  generic.DetailView
# 这里指定了model， 所以默认就是使用question
class DetailView(generic.DetailView):
    model = Question
    # 把question_detail.html 改为 detail.html
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    # 把question_detail.html 改为 results.html
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# def index(request):
#     # # -是降序，最新的在前面
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # # 这里拼接setting的TEMPLATES，加载template
#     # template = loader.get_template('polls/index.html')
#     # # context是一个dict
#     # context = {
#     #     'latest_question_list': latest_question_list,
#     # }
#     # return HttpResponse(template.render(context, request))

#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # try:
#     #     question= Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404('Question does not exist')
    
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
     

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/result.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)   
    print('request.POST',request.POST)
    try:
        # 字典要用[],来获取数据
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # 这里的e是 isinstance(e, KeyError)
    except (KeyError, Choice.DoesNotExist) as e:
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # 如果点击了返回或者刷新，只要到polls:vote路由，就会重复提交，
        # 所以不能让其跳转到polls:vote
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
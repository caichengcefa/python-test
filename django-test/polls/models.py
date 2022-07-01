import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    # varchar数据类型？
    question_text = models.CharField(max_length=200)
    # 这第一个参数 用于可读
    pub_date = models.DateTimeField('date published')


    def was_published_rencently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


    def __str__(self):
        return self.question_text


class Choice(models.Model):
    # 绑定quesiton外键
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
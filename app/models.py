from django.db import models
from django.conf import settings
from collections import defaultdict


class Test(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_right = models.BooleanField(default=False)


class QuestionList(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    count_test = models.IntegerField(default=0)
    count_ok = models.IntegerField(default=0)
    count_total = models.IntegerField(default=0)
    que_id = defaultdict(int)
    count_corr = defaultdict(int)

    def __str__(self):
        return self.user.username

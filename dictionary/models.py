from django.db import models
from django.forms import CharField
from django.utils import timezone
from django.contrib.auth.models import User



# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # ユーザープロフィールに特有のフィールドを追加可能
#     # 例：プロフィール写真、誕生日など


    
class Word(models.Model):
    #英単語
    word_name = models.CharField(max_length = 255)


class UserWord(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    correct_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)
    response_times = models.JSONField(default=list)
    last_answer_time = models.DateTimeField(null=True)
    


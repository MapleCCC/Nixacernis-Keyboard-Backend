from django.db import models


class BaseDict(models.Model):
    chinese_word = models.CharField(
        max_length=25, primary_key=True, unique=True)
    pinyin = models.CharField(max_length=50)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.chinese_word


class UserDict(BaseDict):
    pass

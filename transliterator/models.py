from django.db import models

# Unfortunately, Django currently doesn't support multi-column primary key.
# A workaround is to add an aditional 'id' column as primary key,
# and add a UNIQUE constraint.


class AbstrDict(models.Model):
    chinese_word = models.CharField(max_length=100)
    pinyin = models.CharField(max_length=250)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.chinese_word

    class Meta:
        abstract = True
        unique_together = ['chinese_word', 'pinyin']
        ordering = ["pinyin", "-count"]


# class BaseDict(AbstrDict):
#     class Meta(AbstrDict.Meta):
#         db_table = "base_dict"

# class SingleCharDict(AbstrDict):
#     class Meta(AbstrDict.Meta):
#         db_table = "single_char_dict"


class UserDict(AbstrDict):
    class Meta(AbstrDict.Meta):
        db_table = "user_dict"

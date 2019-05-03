from django.shortcuts import render
from django.http import HttpResponse
from .models import UserDict

from .utils.helper import *


def index(request):
    return HttpResponse("Hello, world. You're at the transliterator index.")


def detail(request, chinese_word):
    result = UserDict.objects.filter(chinese_word=chinese_word)
    if result.count() == 0:
        return HttpResponse("No information about %s can be found", chinese_word)
    else:
        context = {'result': result}
        return render(request, 'transliterator/detail.html', context)


# IN: request object and a string representing raw_key_list
# OUT: HTTPResponse object containing the candidate word list
def transliterate(request, raw_key_list):
    # Input preprocessing
    key_list = preprocess(raw_key_list)
    possible_pinyin_list = translate(key_list)
    # eg. possible_pinyin_list = [['ri','re','ni','ne], ['wa','za']]

    num_of_pinyin = len(possible_pinyin_list)

    # Now look up for candidate words
    candidate_word_list = []

    for i in range(num_of_pinyin):
        candidate_word_list = query(
            possible_pinyin_list[:i + 1]) + candidate_word_list

    context = {'candidate_word_list': candidate_word_list, }

    return render(request, 'transliterator/transliterate.html', context)


# FIXME
def increment(request, chosen_chinese_word):
    try:
        entry = UserDict.objects.get(pk=chosen_chinese_word)
    except BaseException:
        new_entry = UserDict(
            chinese_word=chosen_chinese_word, pinyin="", count=1)
        new_entry.save()
    else:
        entry.count += 1

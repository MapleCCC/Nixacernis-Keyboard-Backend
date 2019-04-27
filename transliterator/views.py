from django.shortcuts import render
from django.http import HttpResponse
from .models import BaseDict, UserDict

from .utils.nixacernis_keyboard import key_initials_bidict, key_finals_bidict


def index(request):
    return HttpResponse("Hello, world. You're at the transliterator index.")


# IN: request object and a string representing raw_key_list
# OUT: HTTPResponse object containing xxx
def transliterate(request, raw_key_list):
    # Input preprocessing
    # Example: raw_key_list = "1-13-4-8"
    key_list = map(lambda x: int(x), raw_key_list.split("-"))
    # Example: key_list = [1, 13, 4, 8]

    # TODO: Check input validity

    pinyin_list = []
    for index, key in enumerate(key_list):
        if index % 2 == 0:
            pinyin_list.append(key_initials_bidict[key][0])
        else:
            pinyin_list[-1] += key_finals_bidict[key][0]
    # Example: pinyin_list = ["wa", "wi"]

    # TODO: Check pinyin validity

    most_likely_sentence = sentence_match_query(pinyin_list)

    return HttpResponse(most_likely_sentence)


# IN: A list of string. e.g. ["wa", "hua"]
# OUT: QuerySet of the longest first n elements of the list, such that it yields non-zero QuerySet.
# Or just an empty QuerySet and an empty list, if no desired target can be found.
def suffix_match_query(pinyin_list):
    query_set = BaseDict.objects.filter(pinyin="".join(pinyin_list))
    if len(pinyin_list) == 0:
        return query_set, pinyin_list  # empty set and empty list
    elif len(query_set) == 0:
        return suffix_match_query(pinyin_list[:-1])
    else:
        return query_set, pinyin_list


def sentence_match_query(pinyin_list):
    if len(pinyin_list) == 0:
        return ""
    query_set, suffix = suffix_match_query(pinyin_list)
    if len(query_set) == 0:
        return ""
    return query_set.order_by('count')[0].chinese_word + sentence_match_query(pinyin_list[len(suffix):])


def query_helper(pinyin_list):
    # e.g. pinyin_list = ["h", "ua", "en"]

    # First part
    # Find exact match to the whole key sequence
    # QuerySet1 = UserDict.objects.filter(pinyin="ni,hao").order_by('count')

    # Second part
    # Find exact match to the first two characters
    # QuerySet2 = UserDict.objects.filter(pinyin="ni,hao")

    # Third part
    # Find exact match to the first character
    first_pinyin = pinyin_list[0] + pinyin_list[1]
    queryset3 = UserDict.objects.filter(pinyin__startswith=first_pinyin)

    # return (QuerySet1 | QuerySet2 | QuerySet3).distinct()
    return queryset3


def increment(request, chosen_chinese_word):
    try:
        entry = UserDict.objects.get(pk=chosen_chinese_word)
    except:
        new_entry = UserDict(
            chinese_word=chosen_chinese_word, pinyin="", count=1)
        new_entry.save()
    else:
        entry.count += 1

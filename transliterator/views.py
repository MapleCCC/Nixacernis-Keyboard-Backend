from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import UserDict

import re

from .utils.transliterate_helper import transliterate_helper
from .utils.pinyin import word_to_pinyin
from .utils.nixacernis_keyboard import number_of_key


def index(request):
    return HttpResponse("Hello, world. You're at the transliterator index.")


def detail(request, chinese_word):
    result = UserDict.objects.filter(chinese_word=chinese_word)
    if result.count() == 0:
        return HttpResponse("No information about %s can be found" % chinese_word)
    else:
        context = {'result': result}
        return render(request, 'transliterator/detail.html', context)


# TODO: 测试一下加入cache mechanism之后的query速度是否加快了

# IN: request object and a string representing raw_key_list
# OUT: HTTPResponse object containing the candidate word list
def transliterate_request_handler(request, raw_key_list):
    if raw_key_list == '':
        return HttpResponse('')

    if not input_is_valid(raw_key_list):
        raise Http404("Input is not valid.")

    # Input preprocessing
    # Example: raw_key_list = "7-4-1-3"
    key_list = preprocess(raw_key_list)
    # Example: key_list = [7, 4, 1, 3]

    candidate_word_list = transliterate_helper(key_list)
    # Example: candidate_word_list = ['你好', '日抛', '你', '腻', '泥']

    return HttpResponse(",".join(candidate_word_list))


def demo(request, raw_key_list):
    response = transliterate_request_handler(request, raw_key_list)
    candidate_word_list = response.content.decode('utf-8').split(',')
    context = {'candidate_word_list': candidate_word_list, }

    return render(request, 'transliterator/demo.html', context)


def increment(request, chinese_word):
    result = UserDict.objects.filter(chinese_word=chinese_word)
    if result.count() == 0:
        for pinyin in word_to_pinyin(chinese_word):
            new_record = UserDict(
                chinese_word=chinese_word, pinyin=pinyin, count=1)
            new_record.save()
        return HttpResponse("Cannot find the chinese word %s in database. Created new record for it instead." % chinese_word)
    else:
        for record in result:
            record.count = record.count + 1
            record.save()
        return HttpResponse("Increment succeeded. Word priority has been incremented From %d to %d" % (record.count-1, record.count))


# TODO: Change regex from hardcode to format via number_of_pinyin
def input_is_valid(raw_key_list):
    # regex = '^[1-%(number_of_key)d](-[1-%(number_of_key)d])*$' % {
    #     'number_of_key': number_of_key}
    regex = '^([1-9]|1[0-8])(-([1-9]|1[0-8]))*$'
    if re.match(regex, raw_key_list) == None:
        return False
    else:
        return True


# IN: "7-4-1-3"
# OUT: [7, 4, 1, 3]
def preprocess(raw_key_list):
    # Tokenize and transform from 1-indexed to 0-indexed
    # Example: raw_key_list = "7-4-1-3"
    key_list = [int(key)-1 for key in raw_key_list.split("-")]
    # Example: key_list = [6, 3, 0, 2]

    # TODO: Check input validity, boundedness

    # normalize pinyin_list, remove dangling initials
    if len(key_list) % 2 != 0:
        key_list = key_list[:-1]

    return key_list

from django.shortcuts import render
from django.http import HttpResponse
from .models import UserDict

from .utils.helper import preprocess, translate, query
from .utils.pinyin import word_to_pinyin


def index(request):
    return HttpResponse("Hello, world. You're at the transliterator index.")


def detail(request, chinese_word):
    result = UserDict.objects.filter(chinese_word=chinese_word)
    if result.count() == 0:
        return HttpResponse("No information about %s can be found" % chinese_word)
    else:
        context = {'result': result}
        return render(request, 'transliterator/detail.html', context)


# IN: request object and a string representing raw_key_list
# OUT: HTTPResponse object containing the candidate word list
def transliterate(request, raw_key_list):
    # Input preprocessing
    # Example: raw_key_list = "7-4-1-3"
    key_list = preprocess(raw_key_list)
    # Example: key_list = [7, 4, 1, 3]

    possible_pinyin_list = translate(key_list)
    # eg. possible_pinyin_list = [['ri','re','ni','ne], ['wa','za']]

    num_of_pinyin = len(possible_pinyin_list)

    # Now look up for candidate words
    # Lookup from small string to larger string, for better utilizing Django's database lookup cache feature
    candidate_word_list = []
    for i in range(num_of_pinyin):
        candidate_word_list = query(
            possible_pinyin_list[:i + 1]) + candidate_word_list
    # Example: candidate_word_list = ['你好', '日抛', '你', '腻', '泥']

    context = {'candidate_word_list': candidate_word_list, }

    return render(request, 'transliterator/transliterate.html', context)


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

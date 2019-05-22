__all__ = ['transliterate_helper']

from itertools import product
from functools import reduce

from django.db.models import Q
from ..models import UserDict

from .nixacernis_keyboard import translate
from .pinyin import pinyin_is_valid
from .transliterate_cache import TransliterateCache


# The maximum payload restriction for performance.
CANDIDATES_PAYLOAD = 20

# TODO: Does Python have any reserved keywords for declaring global varibales? To prevent multiple inclusion.
transliterate_cache = TransliterateCache()


def transliterate_helper(key_list, offset=0):
    candidate_word_list = transliterate(key_list)
    transliterate_cache.store(key_list, candidate_word_list)

    return candidate_word_list[offset:offset+CANDIDATES_PAYLOAD]


# IN: A list of keys.
#   eg, [5, 16, 1, 8]
# OUT: A list of candidate words.
#   eg, ['你好','日抛','你','日','匿','泥']
def transliterate(key_list):
    if key_list == []:
        return []

    result = transliterate_cache.query(key_list)
    if result != None:
        return result

    possible_pinyin_list = translate(key_list)
    # eg. possible_pinyin_list = [['ri', 'ni'], ['hao','pao']]
    candidate_word_list = query(
        possible_pinyin_list) + transliterate(key_list[:-2])

    return candidate_word_list


# IN: A list of possible pinyins.
#   eg, [['ri','ni'], ['hao','pao']]
# OUT: A list of candidate words.
#   eg, ['你好','日抛','你','日','匿','泥']
def query(possible_pinyin_list):
    Q_objects = [Q(pinyin=",".join(py_list))
                 for py_list in product(*possible_pinyin_list)]
    # eg py_list = ["ni", "hao", "ma"]
    merged_Q = reduce(lambda x, y: x | y, Q_objects)
    queryset = UserDict.objects.filter(merged_Q).order_by('-count')

    return [user_dict.chinese_word for user_dict in queryset]

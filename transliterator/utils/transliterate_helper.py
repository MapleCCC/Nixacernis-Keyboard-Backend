__all__ = ['transliterate']

from itertools import product
from functools import reduce, lru_cache

from django.db.models import Q
from ..models import UserDict

from .nixacernis_keyboard import translate
from .pinyin import pinyin_is_valid


# IN: A list of keys.
#   eg, [5, 16, 1, 8]
# OUT: A list of candidate words.
#   eg, ['你好','日抛','你','日','匿','泥']
#
# lru_cache decorator caches recently function calls and results, to accerlerate future query.
# According to document, setting maxsize to power of 2 is most efficient.
# Also note that lru_cache decorator requires the function parameters to be hashable.
# So we should use tuple instead of list.
@lru_cache(maxsize=256)
def transliterate(keys):
    if len(keys) == 0:
        return []

    possible_pinyin_list = translate(keys)
    # eg. possible_pinyin_list = [['ri', 'ni'], ['hao','pao']]
    candidate_word_list = query(
        possible_pinyin_list) + transliterate(keys[:-2])

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

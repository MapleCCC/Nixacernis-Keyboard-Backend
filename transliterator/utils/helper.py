__all__ = ['preprocess', 'translate', 'query']

from itertools import product
from functools import reduce

from django.db.models import Q
from ..models import UserDict

from .nixacernis_keyboard import key_initials_dict, key_finals_dict
from .pinyin import pinyin_is_valid


def preprocess(raw_key_list):
    # Example: raw_key_list = "7-4-1-3"
    key_list = [int(key)-1 for key in raw_key_list.split("-")]
    # Example: key_list = [7, 4, 1, 3]

    # TODO: Check input validity

    # normalize pinyin_list, remove dangling initials
    if len(key_list) % 2 != 0:
        key_list = key_list[:-1]

    return key_list


def translate(key_list):
    if len(key_list) == 0:
        return []
    possible_initial = key_initials_dict[key_list[0]]
    possible_final = key_finals_dict[key_list[1]]
    possible_first_pinyin = [
        x[0]+x[1] for x in product(possible_initial, possible_final) if pinyin_is_valid(x[0]+x[1])]
    # Example: possible_first_pinyin = ["wa", "wi"]
    return [possible_first_pinyin] + translate(key_list[2:])


def query(possible_pinyin_list):
    Q_objects = [Q(pinyin=",".join(py_list))
                 for py_list in product(*possible_pinyin_list)]
    # eg py_list = ["ni", "hao", "ma"]
    total_Q = reduce(lambda x, y: x | y, Q_objects)
    total_queryset = UserDict.objects.filter(total_Q).order_by('-count')
    return [user_dict.chinese_word for user_dict in total_queryset]

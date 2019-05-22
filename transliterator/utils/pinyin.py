# -*- coding:utf-8 -*-#
__all__ = ['pinyin_is_valid', 'word_to_pinyin']

import os
from enum import Enum
from itertools import product


all_pinyin = ()
all_pinyin_file_path = os.path.join(
    os.path.dirname(__file__), 'data', 'all_pinyin.txt')
with open(all_pinyin_file_path, 'r', encoding="utf-8") as f:
    for line in f.readlines():
        all_pinyin += (line[:-1],)


def pinyin_is_valid(string):
    return string in all_pinyin


# IN: A chinese character
# OUT: A set of possible pinyins for the chinese character
char_to_pinyin = {}
char_to_pinyin_file_path = os.path.join(
    os.path.dirname(__file__), 'data', 'Chara.txt')
with open(char_to_pinyin_file_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        tokens = line.split(' ')
        chinese_word = tokens[0]
        # remove the trailing linefeed character
        tokens[-1] = tokens[-1][:-1]
        # remove tone mark
        pinyins = [token[:-1] for token in tokens[1:]]
        # convert to set to drop duplicates
        char_to_pinyin[chinese_word] = set(pinyins)


# IN: A chinese word
# OUT: A list of possible pinyins for the chinese word
def word_to_pinyin(chinese_word):
    py = []
    for char in chinese_word:
        if char in char_to_pinyin:
            py.append(char_to_pinyin[char])
        else:
            continue
    return [','.join(x) for x in product(*py)]


def remove_non_dict_char(chinese_word):
    new_word = chinese_word
    for char in chinese_word:
        if char not in char_to_pinyin:
            new_word = new_word.replace(char, "")
    return new_word

# class Initial(Enum):
#     b = "b"
#     p = "p"
#     m = "m"
#     f 	 d  t  n  l 	 g  k  h 	 j  q  x 	 zh  ch  sh  r 	 z  c  s


# class Final(Enum):


# class Pinyin:
#     def __init__(self, initial=Initial(""), final=Final("a")):
#         self.initial = initial
#         self.final = final

#     def is_valid(self):

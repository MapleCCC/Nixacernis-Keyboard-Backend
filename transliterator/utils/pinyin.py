# -*- coding:utf-8 -*-#
__all__ = ['pinyin_is_valid']

from enum import Enum
import os


all_pinyin = ()
file_path = os.path.join(os.path.dirname(__file__), 'all_pinyin.txt')
with open(file_path, 'r') as f:
    for line in f.readlines():
        all_pinyin += (line[:-1],)


def pinyin_is_valid(string):
    return string in all_pinyin

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

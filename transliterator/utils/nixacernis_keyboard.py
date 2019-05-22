# limit exported objects to only the two dicts, for better information hiding and inter-module decoupling.
__all__ = ['number_of_key', 'translate']

from itertools import product
from bidict import bidict
from .pinyin import pinyin_is_valid

# Use tuple instead of list, for immutability.
# Otherwise the bidict constructor won't accept.
ordered_initials_list = (("v", "x"), ("h", "p"), ("d"), ("w", "z"), ("t"), ("r", "n")) + \
    (("c"), ("l"), ("b"), ("y"), ("sh"), ("ch")) + \
    (("f"), ("q", ""), ("zh"), ("g"), ("j", "k"), ("m", "s"))
ordered_finals_list = (("uan", "uai", "o"), ("a", "ua"), ("u"), ("e"), ("er", "ong"), ("an")) + \
    (("iu", "ou"), ("ai", "ue"), ("ao", "iong"), ("ing", "eng"), ("en", "in"), ("iang", "ui")) + \
    (("ia", "uo"), ("ian", "uang"), ("ang", "iao"), ("ei", "un"), ("i"), ("ie"))

number_of_key = len(ordered_initials_list)

key_initials_dict = {k: v for k, v in enumerate(ordered_initials_list)}
key_finals_dict = {k: v for k, v in enumerate(ordered_finals_list)}

key_initials_bidict = bidict(key_initials_dict)
key_finals_bidict = bidict(key_finals_dict)

initials_key_dict = key_initials_bidict.inverse
finals_key_dict = key_finals_bidict.inverse

# "5,16" yields ['ri', 'ni']
translation_lookup_table = {}
for i in range(18):
    for j in range(18):
        index = "%d,%d" % (i, j)
        possible_initial = key_initials_dict[i]
        possible_final = key_finals_dict[j]
        possible_pinyins = [
            x[0]+x[1] for x in product(possible_initial, possible_final) if pinyin_is_valid(x[0]+x[1])]
        # Example: possible_first_pinyin = ["wa", "wi"]
        translation_lookup_table[index] = possible_pinyins


# IN: A list of keys.
#   eg, [5, 16, 1, 8]
# OUT: A list of possible pinyins.
#   eg, [['ri','ni'], ['hao','pao']]
def translate(key_list):
    if len(key_list) == 0:
        return []
    if len(key_list) == 1:
        # raise ValueError("Input is invalid.")
        return []

    key_for_initial = key_list[0]
    key_for_final = key_list[1]

    index = str(key_for_initial) + ',' + str(key_for_final)

    possible_first_pinyin = translation_lookup_table[index]

    return [possible_first_pinyin] + translate(key_list[2:])

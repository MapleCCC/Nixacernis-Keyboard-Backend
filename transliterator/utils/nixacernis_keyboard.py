# limit exported objects to only the two dicts, for better information hiding and inter-module decoupling.
__all__ = ['number_of_key', 'translate']

from bidict import bidict
from .pinyin import pinyin_is_valid
from itertools import product

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


# IN: A list of keys.
#   eg, [7, 4, 1, 3]
# OUT: A list of possible pinyins.
#   eg, [['ri','re','ni','ne], ['wa','za']]
def translate(key_list):
    if len(key_list) == 0:
        return []
    if len(key_list) == 1:
        # raise ValueError()
        return []

    key_for_initial = key_list[0]
    key_for_final = key_list[1]

    # check input validity

    possible_initial = key_initials_dict[key_for_initial]
    possible_final = key_finals_dict[key_for_final]
    possible_first_pinyin = [
        x[0]+x[1] for x in product(possible_initial, possible_final) if pinyin_is_valid(x[0]+x[1])]
    # Example: possible_first_pinyin = ["wa", "wi"]

    return [possible_first_pinyin] + translate(key_list[2:])

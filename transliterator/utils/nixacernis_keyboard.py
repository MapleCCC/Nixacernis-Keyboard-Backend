from bidict import bidict

# Use tuple instead of list, for immutability.
# Otherwise the bidict constructor won't accept.
ordered_initials_list = (("v", "x"), ("h", "p"), ("d"), ("w", "z"), ("t"), ("r", "n")) + \
    (("c"), ("l"), ("b"), ("y"), ("sh"), ("ch")) + \
    (("f"), ("q", ""), ("zh"), ("g"), ("j", "k"), ("m", "s"))
ordered_finals_list = (("uan", "uai", "o"), ("a", "ua"), ("u"), ("e"), ("er", "ong"), ("an")) + \
    (("iu", "ou"), ("ai", "ue"), ("ao", "iong"), ("ing", "eng"), ("en", "in"), ("iang", "ui")) + \
    (("ia", "uo"), ("ian", "uang"), ("ang", "iao"), ("ei", "un"), ("i"), ("ie"))

key_initials_dict = {k: v for k, v in enumerate(ordered_initials_list)}
key_finals_dict = {k: v for k, v in enumerate(ordered_finals_list)}

key_initials_bidict = bidict(key_initials_dict)
key_finals_bidict = bidict(key_finals_dict)

initials_key_dict = key_initials_bidict.inverse
finals_key_dict = key_finals_bidict.inverse

# limit exported objects to only the two dicts, for better information hiding and inter-module decoupling.
__all__ = ['key_initials_dict', 'key_finals_dict']

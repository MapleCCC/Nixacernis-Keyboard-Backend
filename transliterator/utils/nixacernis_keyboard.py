from bidict import bidict

# Use tuple instead of list, for immutability.
# Otherwise the bidict constructor won't accept.
ordered_initials_list = (("t"), ("w", "z"), ("zh"), ("h", "p"), ("m", "s"), ("b")) + \
    (("c"), ("r", "n"), ("sh"), ("x"), ("q"), ("k", "j")) + \
    (("ch"), ("g"), ("l"), ("f"), ("d", ""), ("y"))
ordered_finals_list = (("ong", "er"), ("e"), ("ang, iao"), ("a", "ua"), ("ie"), ("ao", "iong")) + \
    (("iu", "ou"), ("an"), ("en", "in"), ("uan", "uai", "o", "v"), ("ian", "uang"), ("i")) + \
    (("iang", "ui"), ("ei", "un"), ("ai", "ue"),
     ("ia", "uo"), ("u"), ("ing", "eng"))

key_initials_dict = {k: v for k, v in enumerate(ordered_initials_list)}
key_finals_dict = {k: v for k, v in enumerate(ordered_finals_list)}

key_initials_bidict = bidict(key_initials_dict)
key_finals_bidict = bidict(key_finals_dict)

initials_key_dict = key_initials_bidict.inverse
finals_key_dict = key_finals_bidict.inverse

# limit exported objects to only the two dicts, for better information hiding and inter-module decoupling.
__all__ = ['key_initials_dict', 'key_finals_dict']

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__     = 'MIT'
__author__      = 'Alberto Pettarin (alberto albertopettarin.it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto albertopettarin.it)'
__version__     = 'v2.0.0'
__date__        = '2014-06-30'
__description__ = 'Parse the given definition list for penelope.py'


import collections, re
### BEGIN parse ###
# parse(data, type_sequence, ignore_case)
# parse the given list of pairs
# data = [ [word, definition] ]
# with type_sequence and ignore_case options,
# and outputs the following list:
# parsed = [ word, include, synonyms, substitutions, definition ]
#
# where:
#        word is the sorting key
#        include is a boolean saying whether the word should be included
#        synonyms is a list of alternative strings for word
#        substitutions is a list of pairs [ word_to_replace, replacement ]
#        definition is the definition of word

# regular expressions
raw_regs = [
    ['(\w+)ves$', '\g<1>f'],     # leaves -> leaf
    ['(\w+)ves$', '\g<1>fe'],     # knives -> knife

    ['(\w+)s$', '\g<1>'],        # asks -> ask  & rocks -> rock
    ['(\w+)ies$', '\g<1>y'],     # tries -> try
    ['(\w+)ing$', '\g<1>'],      # working -> work
    ['(\w+)ing$', '\g<1>e'],     # baking -> bake
    ['(\w+)ed$', '\g<1>'],      # asked -> ask
    ['(\w+e)d$', '\g<1>'],      # baked -> bake
    ['(\w+)ied$', '\g<1>y']     # worried -> worry
]


# default implementation, just copy the content of the stardict dictionary
def parse(data, type_sequence, ignore_case):
    # prepare regular expressions
    regs = []
    for [reg, repl] in raw_regs:
        reg_obj = re.compile(reg)
        regs.append([reg_obj, repl])

    # initial dictionary fill
    parsed_data = collections.defaultdict()
    for [key, definition] in data:
        parsed_data[key] = [ key, True, [], [], definition ]

    for d in data:
        key = d[0]
        # print(key + ":")
        for [reg_obj, repl] in regs:
            # match word forms in order
            if reg_obj.search(key) == None:
                continue
            # try a word form
            wordForm = reg_obj.sub(repl, key)
            # if the word form exist (i.e. included into the dictionary)
            # add it to the list on synonyms
            if wordForm in parsed_data:
                print(wordForm + " -> " + key)
                change_tuple = parsed_data[wordForm]
                change_tuple[2].append(key)
                parsed_data[wordForm] = change_tuple

    return list(parsed_data.values())
### END parse ###


#FLM Check Anchors
# -*- coding: utf-8 -*-

# Version 1.0

# Description:
# Compares font anchors to latest Bravura metadata file # (published at
# https://github.com/steinbergmedia/bravura) to find missing or # superfluous
# glyph anchors according to the SMuFL standard. Script will print # any
# findings and mark glyphs with discrepancies unless colour value is set to 0.

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.

import os
import json
from urllib2 import urlopen

f = fl.font


def get_json(url):
    ''''gets json source files from repository url.'''
    raw = urlopen(url)
    source = raw.read()
    data = json.loads(source)
    return data


def compare_anchors(dict_a, dict_b, colour):
    '''compares font vs. metadata anchors, and marks glyphs with discrepancies'''
    seen = set()
    for name, anchors in dict_a.iteritems():
        if name in dict_b:
            for anchor in anchors:
                if anchor not in dict_b[name]:
                    # Get conventional glyph names.
                    aglname = name_dict[name]
                    # Delete nested loop duplicates of name.
                    if aglname not in seen:
                        seen.add(aglname)
                        if colour > 0:
                            g.mark = colour
                        print('\n{} / {}:'.format(aglname, name))
                    print(anchor)


# Get raw data.
b = get_json('https://raw.githubusercontent.com/steinbergmedia/bravura/master/redist/bravura_metadata.json')

f_dict = {}
name_dict = {}
b_dict = {}

# Build dicts of font anchors and conventional glyph names.
for g in f.glyphs:
    name_dict[g.note] = g.name
    f_dict[g.note] = [a.name]
    for a in g.anchors:
        if g.note in f_dict and a.name not in f_dict[g.note]:
            f_dict[g.note].append(a.name)


# Build dict of Bravura anchors.
for name, anchors in b['glyphsWithAnchors'].iteritems():
    if name in f_dict:
        b_dict[name] = anchors.keys()

# Compare Bravura anchors to font anchors to get missing font anchors.
print('Missing anchors:'),
compare_anchors(b_dict, f_dict, 250)  # 250 = red
print('\n' + '-' * 30 + '\n')

# Compare font anchors to Bravura anchors to get superfluous anchors.
print('Superfluous anchors:'),
compare_anchors(f_dict, b_dict, 250)  # 250 = red
print('All done!')
fl.UpdateFont()

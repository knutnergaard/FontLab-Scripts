#FLM:Set SMuFL Names

# Description:
# This script retrieves discriptive SMuFL names from the latest published glyphnames.json metadata
# file published at https://github.com/w3c/smufl, and adds them to the Note field of the glyphs at
# the corresponding codepoint.

# Note:
# This is a modified version of Ben Timms's  'Annotate glyphs with SMuFL names', Available at the
# SMuFL GitHub repository (https://github.com/w3c/smufl).

# (c) 2021 by Knut Nergaard
# (c) 2015 by Ben Timms, Steinberg Media Technologies GmbH.
# Use, modify and distribute as desired.


import json
import os
from urllib2 import urlopen


def get_json(url):
    ''''gets json source files from repository url.'''
    raw = urlopen(url)
    source = raw.read()
    data = json.loads(source)
    return data


def set_glyph_note_to_smufl_name(glyph):
    for codepoint in glyph.unicodes:
        if codepoint in glyphnames_for_codepoint:
            print 'Setting Note for codepoint {} to "{}".'.format(hex(codepoint), glyphnames_for_codepoint[codepoint])
            glyph.note = str(glyphnames_for_codepoint[codepoint])
        return
    print 'Unable to lookup SMuFL name for glyph {}.'.format(glyph.name)


if fl.font is None:
    raise Exception('Please open a font first!')

glyphnames_data = get_json('https://raw.githubusercontent.com/w3c/smufl/gh-pages/metadata/glyphnames.json')

glyphnames_for_codepoint = {}

# Build a map of glyph names indexed on codepoint
for glyphname, glyphdata in glyphnames_data.iteritems():
    glyphnames_for_codepoint[int(glyphdata['codepoint'][2:], 16)] = glyphname

for glyph in fl.font.glyphs:
    set_glyph_note_to_smufl_name(glyph)

fl.UpdateFont()

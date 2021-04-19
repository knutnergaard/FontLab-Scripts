#FLM: Set Optional Descriptions

# Description:
# Retrieves glyph descriptions for optional glyphs from the latest bravura metadata JSON file
# published at https://github.com/steinbergmedia/bravura, and appends them to the Note field of
# glyphs at the corresponding codepoints, along with the value separator of your choice.

# Note:
# This script is intended as preparation for metadata file generation, and should be run AFTER
# setting the descriptive smufl_names. The chosen value separator (carriage return (\r) by default)
# should be the same as in the metadata generator.

# (c) 2021 by Knut Nergaard
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


def set_description(glyph):
    ''' Appends description to glyph note with chosen value separator. '''
    if glyph.unicode >= 0xF400:
        if glyph.note == 0:
            print('Skipping glyph with empty note: {}'.format(glyph.name))
        elif glyph.note > 0 and VALUE_SEPARATOR in glyph.note:
            print('Skipping glyph with preexisting value separator: {}'.format(glyph.name))
        elif glyph.note not in descriptions:
            print('Unable to lookup SMuFl name for glyph: {}'.format(glyph.name))
        else:
            print('Setting description for {}: "{}".'.format(glyph.name, descriptions[glyph.note]))
            glyph.note += str(VALUE_SEPARATOR + descriptions[glyph.note])
        return


VALUE_SEPARATOR = '\r'

if fl.font is None:
    raise Exception('Please open a font first!')

metadata = get_json('https://raw.githubusercontent.com/steinbergmedia/bravura/master/redist/bravura_metadata.json')

descriptions = {}

# Build dictionary of smufl names : descriptions.
for structure, smufl_names in metadata.iteritems():
    if structure in ['ligatures', 'optionalGlyphs', 'sets']:
        for smufl_name, values in smufl_names.iteritems():
            if values.has_key('description'):
                descriptions[smufl_name] = values['description']

for g in fl.font.glyphs:
    set_description(g)

fl.UpdateFont()
print('All done!')

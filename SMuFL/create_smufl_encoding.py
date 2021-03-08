# Create SMuFL Encoding

# Version 1.0

# Description:
# Generates FontLab encoding file (.enc) for the SMuFL PUA range,
# based on latest metadata release @ https://github.com/w3c/smufl.

# Naming Scheme:
# By default, glyph names are formatted uniXXXX (UV with 'uni' prefix),
# according to the AGL specification (https://github.com/adobe-type-tools/agl-specification).

# If you prefer to encode SMuFLs descriptive glyph names, comment/uncomment lines 93/94.

# Beware:
# Please be sure to specify unique encoding vector index under Settings below
# when using several encoding versions at the same time.

# If chosen file path already exists, existing file will be overwritten.
# The script must be run using Python 3 in the command line.

# Please refer to the FontLab manual for more information about custom encoding tables.

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.


import os
import json
from urllib.request import urlopen
from datetime import date


def get_json(url):
    ''''gets json source files from repository url.'''
    with urlopen(url) as raw:
        source = raw.read()
    data = json.loads(source)
    return data


# converts ranges.json to sorted list.
r = get_json('https://raw.githubusercontent.com/w3c/smufl/gh-pages/metadata/ranges.json')
r_list = []

for key, value in r.items():
    values = value['range_start'], value['range_end'], value['description']
    r_list.append(values)

r_sorted = sorted(r_list)

# converts glyphnames.json to sorted list.
g = get_json('https://raw.githubusercontent.com/w3c/smufl/gh-pages/metadata/glyphnames.json')
g_list = []

for key, value in g.items():
    if type(value) is dict:
        values = value['codepoint'], value['description'], key
        g_list.append(values)

g_sorted = sorted(g_list)


# SETTINGS:
#---------------------
date = date.today()     # defaults to today's date.
enc_vector = '10001'    # must be unique to encoding file!
enc_name = 'SMuFL Complete OT Encoding'  # name in FontLab encoding menu.
smufl_version = '1.3'
file_path = '/Users/user_name/Library/Application Support/FontLab/Studio 5/Encoding/SMuFL.enc'
# path and name of encoding file, e.g.:
# /Users/User_name/Library/Application Support/FontLab/Studio 5/Encoding/SMuFL.enc
#---------------------

try:
    # opens encoding file.
    with open(file_path, 'w') as f:

        # formats and writes preamble.
        f.write('%%FONTLAB ENCODING: {}; {}\n%%GROUP:SMuFL\n'
                '%Date: {}\n%SMuFL Version: {}\n\n'.format(enc_vector, enc_name, date, smufl_version))

        # formats and writes spaces range and glyphs.
        f.write('--Spaces--\nspace\n.notdef\nCR\nNULL')

        # formats and writes SMuFL ranges and glyphs.
        for r_start, r_end, r_name in r_sorted:
            ranges = '\n\n--{}_({}-{})--'.format(r_name.replace(' ', '_'), r_start, r_end)
            f.write(ranges)
            for codepoint, g_description, g_name in g_sorted:
                agl_names = '\nuni{} % {}: {}'.format(codepoint[2:], codepoint, g_description)
                smufl_names = '\n{} % {}: {}'.format(g_name, codepoint, g_description)
                if codepoint >= r_start and codepoint <= r_end:

                    # Comment/uncomment following lines to choose different naming scheme.
                    f.write(agl_names)
                    # f.write(smufl_names)

                else:
                    continue

        f.write('\n\n--Optional_glyphs_(U+F400-U+F8FF)--')
except FileNotFoundError:
    print('Please choose a valid path for encoding file.')
else:
    print('All done!')

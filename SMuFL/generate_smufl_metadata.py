#FLM:Generate SMuFL Metadata

# Version 1.0

# Description:
# Generates JSON metadata file for SMuFL fonts.

# Features currently supported:
# - engraving defaults
# - glyph advanced widths
# - glyph bounding boxes
# - glyphs with alternates
# - glyphs with anchors
# - ligatures
# - optional glyphs
# - sets

# Note:
# This script requires all glyphs to be named according to SMuFL guidelines, with recommended
# characters adopting the 'uni' + Unicode value scheme. Ligatures, stylistic alternates and sets
# should follow the descriptive scheme, with ligature names comprised of component names,
# separated by underscore ('_'), and alternates and stylistic adopting the names of their
# recommended counterparts, suffixed by .salt and .ss (plus index number) respectively.

# Full support for glyph descriptions in optional glyphs and sets require additional string,
# separated from descriptive name by an optional character, in the Note fields of appropriate
# glyphs. As a starting point, Bravura's glyph descriptions can be imported using the script Set
# Optional Descriptions. String must be set manually for any unique glyphs.

# By default the metadata file is saved to Desktop. Filepath can be set in OUTPUT_DIR below.
# VALUE_SEPARATOR (carriage return (\r) by default) should be the same as in Notes and as specified
# in Set Optional Descriptions.

# This script is built upon Ben Timms's metadata generator for SMuFL fonts, which is available at
# the SMuFL repository on GitHub (https://github.com/w3c/smufl).

# (c) 2021 by Knut Nergaard.
# (c) 2015 by Ben Timms, Steinberg Media Technologies GmbH.
# Use, modify and distribute as desired.


import json
import os
from time import localtime, strftime
from urllib2 import urlopen
from FL import *
f = fl.font

OUTPUT_DIR = os.path.join(os.path.expanduser('~'), 'Desktop')
VALUE_SEPARATOR = '\r'
FILENAME = os.path.join(OUTPUT_DIR, '{}_metadata_{}.json'.format(f.font_name,
                                                                 strftime("%Y%m%d_%H%M%S", localtime())))
# Striftime adds date and time file

if f is None:
    raise Exception('Please open a font first!')

# Edit the following dictionaries manually as needed.
FONT_METADATA = {
    "fontName": f.font_name,
    "fontVersion": 1.12,
    "engravingDefaults": {
        "arrowShaftThickness": 0.16,
        "barlineSeparation": 0.4,
        "beamSpacing": 0.25,
        "beamThickness": 0.5,
        "bracketThickness": 0.5,
        "dashedBarlineDashLength": 0.5,
        "dashedBarlineGapLength": 0.25,
        "dashedBarlineThickness": 0.16,
        "hairpinThickness": 0.16,
        "legerLineExtension": 0.4,
        "legerLineThickness": 0.16,
        "lyricLineThickness": 0.16,
        "octaveLineThickness": 0.16,
        "pedalLineThickness": 0.16,
        "repeatBarlineDotSeparation": 0.16,
        "repeatEndingLineThickness": 0.16,
        "slurEndpointThickness": 0.1,
        "slurMidpointThickness": 0.22,
        "staffLineThickness": 0.13,
        "stemThickness": 0.12,
        "subBracketThickness": 0.16,
        "textFontFamily": [
            "Academico",
            "Century Schoolbook",
            "Edwin",
            "serif"
        ],
        "textEnclosureThickness": 0.16,
        "thickBarlineThickness": 0.5,
        "thinBarlineThickness": 0.16,
        "tieEndpointThickness": 0.1,
        "tieMidpointThickness": 0.22,
        "tupletBracketThickness": 0.16
    },
    "glyphAdvanceWidths": {},
    "glyphBBoxes": {},
    "glyphsWithAlternates": {},
    "glyphsWithAnchors": {},
    "ligatures": {},
    "optionalGlyphs": {},
    "sets": {},
}

SET_INFO = {
    "ss01": {
        "description": "Smaller optical size for small staves",
        "type": "opticalVariantsSmall"
    },
    "ss02": {
        "description": "Short flags (to avoid augmentation dots)",
        "type": "flagsShort"
    },
    "ss03": {
        "description": "Straight flags",
        "type": "flagsStraight"
    },
    "ss04": {
        "description": "Large time signatures",
        "type": "timeSigsLarge"
    },
    "ss05": {
        "description": "Noteheads at larger optical size",
        "type": "noteheadsLarge"
    },
    "ss06": {
        "description": "Tuplet numbers at a lighter weight",
        "type": "tupletsLight"
    },
    "ss07": {
        "description": "Smaller optical size for subscript and superscript placement",
        "type": "chordSymbolsOpticalVariants"
    },
    "ss08": {
        "description": "Oversized slash noteheads",
        "type": "slashesOversized"
    },
    "ss09": {
        "description": "Large, narrow time signatures",
        "type": "timeSigsLargeNarrow"
    },
    "ss10": {
        "description": "Accidentals for figured bass with longer stems",
        "type": "figbassAccidentalsLongerStems"
    }
}


def to_cartesian(val):
    ''' Converts font units to staff spaces based on font UPM. '''
    space = f.upm / 4
    return round(float(val) / space, 3)


def format_codepoint(val):
    ''' Converts unicode decimal to codepoint. '''
    return "U+{}".format(hex(val).upper()[2:])


def get_smufl_name(note):
    '''Parses name and description in note field and returns name. '''
    if VALUE_SEPARATOR in note:
        name = note.split(VALUE_SEPARATOR)[0]
    else:
        name = note
    return name


def get_alt_description(note):
    '''Parses name and description in note field and returns description. '''
    if VALUE_SEPARATOR in note:
        description = note.split(VALUE_SEPARATOR)[1]
    else:
        description = None
    return description


def note_for_name(glyphname):
    ''' Returns note for specified glyph by name. '''
    index = f.FindGlyph(glyphname)
    return f.glyphs[index].note


def get_json(url):
    ''''gets json source files from repository url.'''
    raw = urlopen(url)
    source = raw.read()
    data = json.loads(source)
    return data


# progaram:
print('Starting ...')

# Build dict of classes from classes.json and map keys to alternates.
class_dict = {}
classes_data = get_json('https://raw.githubusercontent.com/w3c/smufl/gh-pages/metadata/classes.json')
for classes, smufl_names in classes_data.iteritems():
    for name in smufl_names:
        class_dict.setdefault(name, []).append(classes)

# Build dict of alternates
alt_dict = {}
for g in f.glyphs:
    if '.salt' in g.name or '.ss' in g.name:
        alt_dict.setdefault(g.name[:7], []).append(g.name)

set_glyphs = []

# Build file.
print('Building metadata ...')
for g in f.glyphs:

    # Validate glyphs.
    if g.note is None or len(g.note) == 0:
        print 'Skipping glyph with empty note: {}'.format(g.name)
        continue

    if g.nodes_number == 0 and len(g.components) == 0:
        print 'Skipping glyph with no nodes: {}'.format(g.name)
        continue

    smufl_name = get_smufl_name(g.note)
    alt_description = get_alt_description(g.note)

    # Set glyph advace widths.
    advance_wdth = float(g.width)
    FONT_METADATA["glyphAdvanceWidths"][smufl_name] = \
        to_cartesian(advance_wdth)

    # Set glyph bounding boxes.
    bounding_box = g.GetBoundingRect()
    FONT_METADATA["glyphBBoxes"][smufl_name] = \
        {"bBoxSW":
         [to_cartesian(bounding_box.ll.x),
          to_cartesian(bounding_box.ll.y)],
         "bBoxNE":
         [to_cartesian(bounding_box.ur.x),
          to_cartesian(bounding_box.ur.y)]}

    # Set glyphs with alternates.
    if g.name in alt_dict:
        FONT_METADATA["glyphsWithAlternates"][smufl_name] = {}
        FONT_METADATA["glyphsWithAlternates"][smufl_name]["alternates"] = []

        for alternate in alt_dict[g.name]:
            alt_note = note_for_name(alternate)
            FONT_METADATA["glyphsWithAlternates"][smufl_name]["alternates"].append({
                "codepoint": "U+{}".format(alternate[3:7]),
                "name": get_smufl_name(alt_note)})

    # Set glyphs with anchors.
    if len(g.anchors) > 0:
        FONT_METADATA["glyphsWithAnchors"][smufl_name] = {}

        for anchor in g.anchors:
            FONT_METADATA["glyphsWithAnchors"][smufl_name][anchor.name] = \
                [to_cartesian(anchor.x), to_cartesian(anchor.y)]

    # Set ligatures.
    if g.unicode >= 0xF400:
        if g.name.count('uni') >= 2 and '_' in g.name:
            FONT_METADATA["ligatures"][smufl_name] = {}
            FONT_METADATA["ligatures"][smufl_name]["codepoint"] = format_codepoint(g.unicode)
            FONT_METADATA["ligatures"][smufl_name]["description"] = alt_description

            # Get component names from ligature names.
            component_names = g.name.split('_')
            component_notes = []

            for c_name in component_names:
                c_note = note_for_name(c_name)
                component_notes.append(c_note)
                FONT_METADATA["ligatures"][smufl_name]["componentGlyphs"] = component_notes

        # Set optional glyphs.
        FONT_METADATA["optionalGlyphs"][smufl_name] = {"classes": []}
        FONT_METADATA["optionalGlyphs"][smufl_name]["codepoint"] = format_codepoint(g.unicode)
        if g.name.endswith(('.salt', '.ss'), 7, -2):
            alt_name = g.name[:7]
            smufl_alt = note_for_name(alt_name)
            if smufl_alt in class_dict:
                FONT_METADATA["optionalGlyphs"][smufl_name] = {}
                FONT_METADATA["optionalGlyphs"][smufl_name]["classes"] = []
                for value in class_dict[smufl_alt]:
                    FONT_METADATA["optionalGlyphs"][smufl_name]["classes"].append(value)
                
        # Set sets.
        if g.name.endswith('.ss', 7, -2):
            FONT_METADATA["sets"] = SET_INFO
            glyph_info = {
                "alternateFor": smufl_alt,
                "codepoint": format_codepoint(g.unicode),
                "description": get_alt_description(g.note),
                "name": smufl_name}
            suffix = g.name[8:]
            if suffix in FONT_METADATA["sets"]:
                set_glyphs.append(glyph_info)
                FONT_METADATA["sets"][suffix]["glyphs"] = set_glyphs

# Write to file.
print 'Writing metadata to: {}'.format(FILENAME)
with open(FILENAME, 'w') as outfile:
    json.dump(FONT_METADATA, outfile, indent=4, sort_keys=True)

print 'All done!'

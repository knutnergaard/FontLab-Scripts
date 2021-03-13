#FLM: Build Barlines

# Version 0.1

# Description:
# Builds composite glyphs in SMuFLs Barlines range from single barline glyphs.
# For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.


from FL import *

engraving_dflts = {
    # Values in staff spaces.
    'barlineSeparation': 0.34,
}


gen_dict = {
    # target : sources
    'uniE031': ('uniE030', 'uniE030'),
    'uniE032': ('uniE030', 'uniE034'),
    'uniE033': ('uniE034', 'uniE030'),
    'uniE035': ('uniE034', 'uniE034'),
}


def check_sources(glyph):
    ''' Checks for missing source glyphs and decomposes any precsisting components. '''
    if not f.has_key(glyph):
        print glyph + ' is missing'
    for g in f.glyphs:
        comp_num = len(g.components)
        if g.name == glyph and comp_num > 0:
            g.Decompose()
            print 'Decomposing: ' + g.name


def handle_preexisting(glyph_name):
    ''' Changes name and unicode of any preexisting glyphs. '''
    if f.has_key(glyph_name):
        t_indx = f.FindGlyph(glyph_name)
        old_glyph = f.glyphs[t_indx]
        old_glyph.name = old_glyph.name + '_001'
        old_glyph.unicode = 0


def make_glyph(glyph_name):
    ''' Appends new glyphs with chosen mark colour (stylistic alt. unicode = 0). '''
    try:
        new_glyph.unicode = int(glyph_name[3:], 16)
    except ValueError:
        new_glyph.unicode = 0
    # Sets your favorite mark colour.
    new_glyph.mark = 120
    # Appends new glyphs to font.
    f.glyphs.append(new_glyph)
    print('Appending: ' + glyph_name)


# Program:
f = fl.font
print 'Starting ...'
for target, sources in gen_dict.iteritems():
    bbox_wdths = []
    separations = []
    components = []

    for i, source in enumerate(sources):
        new_glyph = Glyph()
        new_glyph.name = target
        s_indx = f.FindGlyph(source)
        source_glyph = f.glyphs[s_indx]
        space = f.upm / 4
        check_sources(source)

        bbox_wdth = int(source_glyph.GetBoundingRect().width)
        separation = int(space * engraving_dflts['barlineSeparation'])
        bbox_wdths.append(bbox_wdth)
        if i == 0:
            separation = 0
        separations.append(separation)
        offset = sum(bbox_wdths[:-1] + separations)
        x, y = offset, 0
        components.append(Component(s_indx, Point(x, y)))

    for item in components:
        new_wdth = sum(bbox_wdths + separations)
        metrics = Point(new_wdth, 0)
        new_glyph.SetMetrics(metrics)
        new_glyph.components.append(item)

    handle_preexisting(target)
    make_glyph(target)


fl.UpdateFont(fl.ifont)
print('All done!')

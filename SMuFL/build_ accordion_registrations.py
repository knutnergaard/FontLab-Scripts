#FLM: Build Accordion Registrations

# Version 0.1

# Description:
# Builds composites from the combining rank and dot glyphs in SMuFLs Accordion ramge.

# Note:
# The script assigns grid values to the bounding box of each combining rank glyph, and places dots
# accordingly. To ensure accurate placements, all glyphs must be registered according to SMuFL
# guidelines, with the bottom left corner at the origin point, and with zero - width side bearings.

# Please specify any overshoot below the baseline for round rank glyphs below (in font units).

# For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.


from FL import *

# OVERSHOOT FOR ROUND RANK GLYPHS:

overshoot = -0

#---------------------------------

gen_dict = {
    # target : (rank glyph, dot placement codes)
    'uniE8A0': ('uniE8C6', 'stop4'),
    'uniE8A1': ('uniE8C6', 'stop8'),
    'uniE8A2': ('uniE8C6', 'upper8'),
    'uniE8A3': ('uniE8C6', 'lower8'),
    'uniE8A4': ('uniE8C6', 'stop16'),
    'uniE8A5': ('uniE8C6', 'stop4', 'stop8'),
    'uniE8A6': ('uniE8C6', 'stop8', 'upper8'),
    'uniE8A7': ('uniE8C6', 'stop4', 'stop8', 'upper8'),
    'uniE8A8': ('uniE8C6', 'lower8', 'stop8', 'upper8'),
    'uniE8A9': ('uniE8C6', 'stop4', 'stop16'),
    'uniE8AA': ('uniE8C6', 'stop4', 'stop8', 'stop16'),
    'uniE8AB': ('uniE8C6', 'stop8', 'stop16'),
    'uniE8AC': ('uniE8C6', 'stop8', 'upper8', 'stop16'),
    'uniE8AD': ('uniE8C6', 'stop4', 'lower8', 'upper8' 'stop16'),
    'uniE8AE': ('uniE8C6', 'lower8', 'upper8'),
    'uniE8AF': ('uniE8C6', 'lower8', 'upper8', 'stop16'),
    'uniE8B0': ('uniE8C6', 'stop4', 'lower8', 'upper8'),
    'uniE8B1': ('uniE8C6', 'lower8', 'stop8', 'upper8', 'stop16'),
    'uniE8B2': ('uniE8C6', 'stop4', 'lower8', 'stop8', 'upper8'),
    'uniE8B3': ('uniE8C6', 'stop4', 'lower8', 'stop8', 'upper8' 'stop16'),
    'uniE8B4': ('uniE8C7', 'soprano'),
    'uniE8B5': ('uniE8C7', 'soprano', 'alto'),
    'uniE8B6': ('uniE8C7', 'soprano', 'alto', 'tenor'),
    'uniE8B7': ('uniE8C7', 'soprano', 'alto', 'tenor', 'bass', 'master'),
    'uniE8B8': ('uniE8C7', 'tenor', 'bass', 'master'),
    'uniE8B9': ('uniE8C7', 'alto', 'tenor'),
    'uniE8BA': ('uniE8C7', 'soprano', 'alto', 'bass'),
    'uniE8BB': ('uniE8C8', 'stop8_2'),
    'uniE8BC': ('uniE8C8', 'stop16_2'),
    'uniE8BD': ('uniE8C8', 'stop8_2', 'stop16_2'),
    'uniE8BE': ('uniE8C8', 'master'),
    'uniE8BF': ('uniE8C8', 'stop16_2', 'master'),
    'uniE8C0': ('uniE8C8', '8stop_2', 'stop16_2', 'master'),
    'uniE8C1': ('uniE8C9', 'stop8_3'),
    'uniE8C2': ('uniE8C9', 'stop2'),
    'uniE8C3': ('uniE8C9', 'double8stop'),
    'uniE8C4': ('uniE8C9', 'stop2' 'stop8_3'),
    'uniE8C5': ('uniE8C9', 'stop2', 'left8stop', 'right8stop'),
}

dot = 'uniE8CA'


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
    ''' Appends new glyphs with chosen mark colour (stylistic alto. unicode = 0). '''
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
for target, values in gen_dict.iteritems():
    components = []
    source = values[0]
    placement = values[1:]
    new_glyph = Glyph()
    new_glyph.name = target
    s_indx = f.FindGlyph(source)
    d_indx = f.FindGlyph(dot)
    source_glyph = f.glyphs[s_indx]
    dot_glyph = f.glyphs[d_indx]
    for i, value in enumerate(placement):
        check_sources(source)

        source_bbox_wdth = (source_glyph.GetBoundingRect().width)
        source_bbox_hght = (source_glyph.GetBoundingRect().height)
        dot_bbox_wdth = (dot_glyph.GetBoundingRect().width)
        dot_bbox_hght = (dot_glyph.GetBoundingRect().height)

        # Reference values provided in comments below.
        x, y = source_bbox_wdth / 2, source_bbox_hght / 2
        if value == 'stop4':
            y = source_bbox_hght / 1.219  # stop4 = top of round rank 3 (780/640)
        elif value == 'upper8' or value == 'master':
            x = source_bbox_wdth / 1.3  # upper8/master = mid right of round rank 2/3/4 (780/600)
        elif value == 'lower8':
            x = source_bbox_wdth / 4.333  # lower8 = mid left of round rank 3 (780/180)
        elif value == 'stop16':
            y = source_bbox_hght / 5.571  # stop16 = bottom of round rank 3 (780/140)
        elif value == 'soprano':
            y = source_bbox_hght / 1.1624  # soprano = top of rank 4 (780/671)
        elif value == 'alto':
            y = source_bbox_hght / 1.612  # alto = upper mid of rank 4 (780/484)
        elif value == 'tenor':
            y = source_bbox_hght / 2.635  # tenor = lower mid of rank 4 (780/296)
        elif value == 'bass':
            y = source_bbox_hght / 7.156  # bass = bottom of rank 4 (780/109)
        elif value == 'stop8_2':
            y = source_bbox_hght / 1.352  # stop8_2 = top of rank 2 (780/577)
        elif value == 'stop16_2':
            y = source_bbox_hght / 3.842  # stop16_2 = bottom of rank 2 (780/203)
        elif value == 'stop8_3' or value == 'left8stop' or value == 'right8stop':
            y = source_bbox_hght / 5.555  # stop8_3 = bottom of square rank 3 (750/135)
        elif value == 'stop2':
            y = source_bbox_hght / 1.22  # stop2 = top of square rank 3 (750/615)
        elif value == 'left8stop':
            x = source_bbox_wdth / 3.079  # left8stop = bottom left half of square rank 3 (625/203)
        # (x = source_bbox_wdth / 3 with 3% compensation <-->)
        elif value == 'right8stop':
            x = source_bbox_wdth / 1.481  # right8stop = bottom right half of square rank 3 (625/422)
        # (x = source_bbox_wdth / 3 with 3% compensation <-->)

        x -= dot_bbox_wdth / 2
        y -= dot_bbox_hght / 2
        if source != 'uniE8C9':
            y += overshoot

        if i == 0:
            components.append(Component(s_indx, Point(0, 0)))
        components.append(Component(d_indx, Point(x, y)))

    for item in components:
        metrics = source_glyph.GetMetrics()
        new_glyph.SetMetrics(metrics)
        new_glyph.components.append(item)

    handle_preexisting(target)
    make_glyph(target)


fl.UpdateFont(fl.ifont)
print('All done!')

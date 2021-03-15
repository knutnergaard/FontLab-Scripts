# FLM: Build Staves
# pylint: disable=invalid-name

# Version 0.2

# Description:
# Builds composite glyphs in SMuFLs Staves range from single staff line glyphs. Script will draw
# primitives in place of non-existent source glyphs, according to engraving default settings below.

# Note:
# For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.
# Any preexisting components in the source glyphs will be decomposed.

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.


from FL import *

# Engraving default settings in staff spaces:
engraving_defaults = {'legerLineExtension': 0.3,
                      'legerLineThickness': 0.16,
                      'staffLineThickness': 0.13}


# Advance width settings for leger lines in staff spaces:
leger_wdths = {'uniE022': 1.328,  # legerLine
               'uniE023': 2.128,  # legerLineWide
               'uniE024': 0.528}  # legerLineNarrow


# Glyphs to generate:
staves = {
    # source : (target_1,  target_2,  target_3,  target_4,  target_5)
    'uniE010': ('uniE011', 'uniE012', 'uniE013', 'uniE014', 'uniE015'),  # staffLine
    'uniE016': ('uniE017', 'uniE018', 'uniE019', 'uniE01A', 'uniE01B'),  # staffLineWide
    'uniE01C': ('uniE01D', 'uniE01E', 'uniE01F', 'uniE020', 'uniE021'),  # staffLineNarrow
    'uniE022': None,  # legerLine
    'uniE023': None,  # legerLineWide
    'uniE024': None   # legerLineNarrow
}

mark_colour = 120  # 0 = None


def draw_primitive(glyph, pt, lngth, hght):
    ''' Draws primitive of assigned length and width. '''
    node = Node(17, Point(pt.x, pt.y + hght))  # 17 = Move
    node.alignment = 0  # 0 = Sharp
    glyph.Add(node)

    node.type = 1  # 1 = Line
    node.points = [Point(pt.x, pt.y - hght)]
    glyph.Add(node)

    node.points = [Point(pt.x + lngth, pt.y - hght)]
    glyph.Add(node)

    node.points = [Point(pt.x + lngth, pt.y + hght)]
    glyph.Add(node)


def decompose_components(glyph_name):
    ''' Decomposes preexisting components in source glyphs. '''
    for g in f.glyphs:
        comp_num = len(g.components)
        if g.name == glyph_name and comp_num > 0:
            g.Decompose()
            print('Decomposing: ' + g.name)


def check_sources(glyph_name):
    ''' Checks for missing source glyphs, draws if non-existent, according to
        type and above settings and append glyphs to font. '''
    if not f.has_key(glyph_name):
        print('\nSource glyph {} is missing!'.format(glyph_name))
        glyph = Glyph()
        glyph.name = glyph_name
        glyph.unicode = int(glyph_name[3:], 16)
        glyph.mark = mark_colour

        # Define parameters for staff lines.
        x, y = 0, space * 2
        wdth = space * 2
        thk = engraving_defaults['staffLineThickness'] * space / 2
        if glyph_name == 'uniE016':
            wdth = space * 3
        elif glyph_name == 'uniE01C':
            wdth = space
        metrics = Point(wdth, 0)

        # Define parameters for leger lines.
        if staves[glyph_name] is None:
            x = -engraving_defaults['legerLineExtension'] * space
            y = 0
            ext = engraving_defaults['legerLineExtension'] * 2
            thk = engraving_defaults['legerLineThickness'] * space / 2
            if glyph_name == 'uniE022':
                wdth = (leger_wdths['uniE022'] + ext) * space
            elif glyph_name == 'uniE023':
                wdth = (leger_wdths['uniE023'] + ext) * space
            else:
                wdth = (leger_wdths['uniE024'] + ext) * space
            neg_sb = wdth - ext * space
            metrics = Point(neg_sb, 0)

        # Draw glyphs, set metrics and append to font.
        reg = Point(x, y)
        print('Adding glyph')
        draw_primitive(glyph, reg, wdth, thk)
        glyph.SetMetrics(metrics)
        f.glyphs.append(glyph)


def make_shifts(start, end, inc):
    ''' Generates delta shift values for components. '''
    current = start
    while current < end:
        yield current
        current += inc


# Program:
f = fl.font
space = fl.font.upm / 4
print('Starting ...')

for source, targets in staves.iteritems():
    # Prepare source glyphs.
    check_sources(source)
    decompose_components(source)

    if targets is not None:
        for target in targets:
            # Get index of source.
            g_indx = f.FindGlyph(source)
            source_glyph = f.glyphs[g_indx]

            # Change name and unicode of any preexisting glyph.
            if f.has_key(target):
                s_indx = f.FindGlyph(target)
                old_glyph = f.glyphs[s_indx]
                old_glyph.name = old_glyph.name + '_001'
                old_glyph.unicode = 0

            # Set parameters for new glyphs.
            new_glyph = Glyph()
            new_glyph.name = target
            new_glyph.unicode = int(target[3:], 16)
            new_glyph.mark = mark_colour  # Sets your favorite mark colour.

            # Determine base y values for initial components
            # in glyphs with odd/even number of lines.
            line_num = targets.index(target) + 2
            if line_num % 2 == 0:
                baseline = space / 2
            else:
                baseline = 0
            glyph_height = space * line_num / 2

            # Generate shift values for subsequent components.
            shifts = make_shifts(baseline, glyph_height, space)

            # Append with + and - shift values.
            for shift in shifts:
                if shift > 0:
                    new_glyph.components.append(Component(g_indx, Point(0, shift)))
                new_glyph.components.append(Component(g_indx, Point(0, -shift)))

            # Get/set metrics for composite glyphs.
            metrics = source_glyph.GetMetrics()
            new_glyph.SetMetrics(metrics)

            # Append new glyphs to font.
            f.glyphs.append(new_glyph)
            print('Appending composite glyph {}'.format(new_glyph.name))


fl.UpdateFont(fl.ifont)
print('\nAll done!')

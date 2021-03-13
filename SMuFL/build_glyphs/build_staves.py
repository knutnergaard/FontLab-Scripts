#FLM: Build Staves

# Version 0.1

# Description:
# Builds composite glyphs in SMuFLs Staves range from single staff line glyphs.

# Note:
# For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.


from FL import *

gen_list = {
    # source : (target_1,  target_2,  target_3,  target_4,  target_5)
    'uniE010': ('uniE011', 'uniE012', 'uniE013', 'uniE014', 'uniE015'),  # staffLine
    'uniE016': ('uniE017', 'uniE018', 'uniE019', 'uniE01A', 'uniE01B'),  # staffLineWide
    'uniE01C': ('uniE01D', 'uniE01E', 'uniE01F', 'uniE020', 'uniE021')}  # staffLineNarrow


f = fl.font


def make_offsets(start, end, inc):
    ''' Generates y offset values for components based on baseline,
        staff hight and staff space values. '''
    current = start
    while current < end:
        yield current
        current += inc


def check_sources(glyph):
    ''' Checks for missing source glyphs and decomposes any precsisting components. '''
    if not f.has_key(glyph):
        print glyph + ' is missing'
    for g in f.glyphs:
        comp_num = len(g.components)
        if g.name == glyph and comp_num > 0:
            g.Decompose()
            print 'Decomposing: ' + g.name


print 'Creating new glyphs ...'
for source, targets in gen_list.iteritems():
    check_sources(source)
    for target in targets:
        # Finds source glyph.
        g_indx = f.FindGlyph(source)
        source_glyph = f.glyphs[g_indx]

        # Changes name and unicode of any preexisting glyph.
        if f.has_key(target):
            s_indx = f.FindGlyph(target)
            old_glyph = f.glyphs[s_indx]
            old_glyph.name = old_glyph.name + '_001'
            old_glyph.unicode = 0

        # Sets parameters for new glyphs.
        new_glyph = Glyph()
        new_glyph.name = target
        new_glyph.unicode = int(target[3:], 16)
        new_glyph.mark = 120  # Sets your favorite mark colour.

        # Determines base offset values for components
        # in glyphs with odd/even number of copies.
        space = fl.font.upm / 4
        line_num = targets.index(target) + 2
        if line_num % 2 == 0:
            baseline = space / 2
        else:
            baseline = 0
        glyph_height = space * line_num / 2

        # Generates offset values for staff lines.
        offsets = make_offsets(baseline, glyph_height, space)
        # Appends components with + and - offset values.
        for offset in offsets:
            if offset > 0:
                new_glyph.components.append(Component(g_indx, Point(0, offset)))
            new_glyph.components.append(Component(g_indx, Point(0, -offset)))

        # Copies and sets metrics.
        metrics = source_glyph.GetMetrics()
        new_glyph.SetMetrics(metrics)

        # Appends new glyphs to font.
        f.glyphs.append(new_glyph)
        print('Appending: ' + new_glyph.name)


fl.UpdateFont(fl.ifont)
print('All done!')

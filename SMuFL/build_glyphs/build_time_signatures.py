#FLM:Build Time Signatures

# Version 0.1

# Description:
# Builds composite glyphs in the Time Signatures, Time signatures supplement, Turned time signatures
# and Reversed time signatures ranges. Current version supports the following glyph types:

# - fractions,
# - cut time glyphs
# - turned glyphs
# - reversed glyphs
# - ligatures

# Support for stylistic sets is planned.

# Note:
# Script requires the presence of basic Time signature numerals (U+E080 - U+E089), common time symbol
# (U+E08A) and fraction slash (U+E08E).

# Additionally, cut time symbols build requires a vertical stroke glyph to be used as component in
# those glyphs. This does not need to be encoded, but must be named according to the variable
# Stroke below. By default name is set to 'timeSigVerticalStroke'.


# (c) 2021 by Knut Nergaard.
# Use, modify and distribute as desired.

f = fl.font
space = f.upm / 4

#              target:  (numerator,   slash,  denominator)
fractions = {'uniE097': ('uniE081', 'uniE08E', 'uniE084'),
             'uniE098': ('uniE081', 'uniE08E', 'uniE082'),
             'uniE099': ('uniE083', 'uniE08E', 'uniE084'),
             'uniE09A': ('uniE081', 'uniE08E', 'uniE083'),
             'uniE09B': ('uniE082', 'uniE08E', 'uniE083')}


component_spacing = 20  # spacing adjustment between components
glyph_spacing = 10      # sidebearing adjustment
serif_space = 20        # extra space for serif of numerator 1
four_space = -40        # extra space for slanted top of denominator four


stroke = 'timeSigVerticalStroke'
# Assigned glyphname of vertical stroke glyph for cut time characters.

cut_dict = {'uniE082': 'uniEC85', 'uniE083': 'uniEC86', 'uniE08A': 'uniE08B'}

turned_dict = {'uniE080': 'uniECE0', 'uniE081': 'uniECE1', 'uniE082': 'uniECE2',
               'uniE083': 'uniECE3', 'uniE084': 'uniECE4', 'uniE085': 'uniECE5',
               'uniE086': 'uniECE6', 'uniE087': 'uniECE7', 'uniE088': 'uniECE8',
               'uniE089': 'uniECE9', 'uniE08A': 'uniECEA', 'uniE08B': 'uniECEB'}

reversed_dict = {'uniE080': 'uniECF0', 'uniE081': 'uniECF1', 'uniE082': 'uniECF2',
                 'uniE083': 'uniECF3', 'uniE084': 'uniECF4', 'uniE085': 'uniECF5',
                 'uniE086': 'uniECF6', 'uniE087': 'uniECF7', 'uniE088': 'uniECF8',
                 'uniE089': 'uniECF9', 'uniE08A': 'uniECFA', 'uniE08B': 'uniECFB'}

ligatures = (
    'uniE09F_uniE080', 'uniE09E_uniE080', 'uniE09F_uniE081', 'uniE09E_uniE081',
    'uniE09F_uniE082', 'uniE09E_uniE082', 'uniE09F_uniE083', 'uniE09E_uniE083',
    'uniE09F_uniE084', 'uniE09E_uniE084', 'uniE09F_uniE085', 'uniE09E_uniE085',
    'uniE09F_uniE086', 'uniE09E_uniE086', 'uniE09F_uniE087', 'uniE09E_uniE087',
    'uniE09F_uniE088', 'uniE09E_uniE088', 'uniE09F_uniE089', 'uniE09E_uniE089',
    'uniE09E_uniE082_uniE09F_uniE084', 'uniE09E_uniE082_uniE09F_uniE082',
    'uniE09E_uniE083_uniE09F_uniE082', 'uniE09E_uniE083_uniE09F_uniE084',
    'uniE09E_uniE083_uniE09F_uniE088', 'uniE09E_uniE084_uniE09F_uniE084',
    'uniE09E_uniE085_uniE09F_uniE084', 'uniE09E_uniE085_uniE09F_uniE088',
    'uniE09E_uniE086_uniE09F_uniE084', 'uniE09E_uniE086_uniE09F_uniE088',
    'uniE09E_uniE087_uniE09F_uniE088', 'uniE09E_uniE089_uniE09F_uniE088',
    'uniE09E_uniE081_uniE09E_uniE082_uniE09F_uniE088',
)

ctrl_char = ('uniE09E', 'uniE09F')


def check_sources(glyph):
    if not f.has_key(glyph):
        print glyph + ' is missing'


def decompose_components(glyph):
    for g in f.glyphs:
        comp_num = len(g.components)
        if g.name == glyph and g.name != 'uniE08B' and comp_num > 0:
            g.Decompose()
            print 'Decomposing: ' + g.name


def append_component_of_component(parent, target):
    ''' Append components inc. any component's component in source 'timeSigCutCommon'
        to new glyph and adjust vertical position of 'timeSigVerticalStroke'. '''
    if parent.name == 'uniE08B' and parent.components:
        vs_indx = f.FindGlyph(stroke)
        stroke_glyph = f.glyphs[vs_indx]
        stroke_wdth = stroke_glyph.width
        stroke_wdth = stroke_glyph.height
        sx, sy = -1, -1  # scale to turn/reverse.
        dx, dy = parent.width, parent.height
        for c in parent.components:
            if c.index == vs_indx:
                dx = (parent.width + stroke_wdth) * 0.5
            target.components.append(Component(c.index, Point(dx, dy), Point(sx, sy)))


def handle_preexisting(glyph_name):
    ''' Changes name and unicode of any preexisting glyphs. '''
    while f.has_key(glyph_name):
        t_indx = f.FindGlyph(glyph_name)
        old_glyph = f.glyphs[t_indx]
        counter = 01
        old_glyph.name = '{}_{}'.format(old_glyph.name, counter)
        old_glyph.unicode = 0
        counter += 1
    # return old_glyph.name


def make_glyph(glyph, glyph_name):
    ''' Appends new glyphs with chosen mark colour (stylistic alto. unicode = 0). '''
    try:
        glyph.unicode = int(glyph_name[3:], 16)
    except ValueError:
        glyph.unicode = 0
    # Sets your favorite mark colour.
    glyph.mark = 120
    # Appends new glyphs to font.
    f.glyphs.append(glyph)
    print('Appending: ' + glyph_name)


def build_fractions():
    for target, sources in fractions.iteritems():
        source_wdths = []
        #components = []
        new_glyph = Glyph()
        new_glyph.name = target

        for i, source in enumerate(sources):
            check_sources(source)
            decompose_components(source)
            s_indx = f.FindGlyph(source)
            source_glyph = f.glyphs[s_indx]
            source_wdth = source_glyph.width
            scale_x, scale_y = 1.0, 1.0    # 1 = 100% (x, y)
            shift_x, shift_y = 0, 0
            num_factor = 0.5
            if i != 1:
                source_wdth = source_wdth * num_factor + glyph_spacing
                scale_x, scale_y = scale_x * num_factor, scale_y * num_factor
            if i == 0:
                shift_x, shift_y = glyph_spacing, space / 2
                if source == 'uniE081':
                    source_wdth += serif_space
            if i == 1:
                shift_x = source_wdths[i - 1] - source_wdth / 2 + component_spacing
            if i == 2:
                shift_x = source_wdths[0] + component_spacing * 2
                shift_y = -space / 2
                if source == 'uniE084':
                    shift_x += four_space
                    source_wdth += four_space

            source_wdths.append(source_wdth)
            new_glyph.components.append(Component(s_indx, Point(shift_x, shift_y), Point(scale_x, scale_y)))

        # for item in components:
        #     new_glyph.components.append(item)

        adv_wdth = source_wdths[0] + source_wdths[2] + component_spacing * 2
        metrics = Point(adv_wdth, 0)
        new_glyph.SetMetrics(metrics)
        handle_preexisting(target)
        make_glyph(new_glyph, target)


def build_cut_time():
    for source, target in cut_dict.iteritems():
        check_sources(source)
        check_sources(stroke)
        decompose_components(source)
        new_glyph = Glyph()
        new_glyph.name = target
        s_indx = f.FindGlyph(source)
        vs_indx = f.FindGlyph(stroke)
        source_glyph = f.glyphs[s_indx]
        source_center = source_glyph.width / 2
        stroke_glyph = f.glyphs[vs_indx]

        dx, dy = 0, 0
        new_glyph.components.append(Component(s_indx, Point(dx, dy)))
        dx, dy = source_center, 0
        new_glyph.components.append(Component(vs_indx, Point(dx, dy)))

        metrics = source_glyph.GetMetrics()
        new_glyph.SetMetrics(metrics)
        handle_preexisting(target)
        make_glyph(new_glyph, target)


def build_turned_time():
    ''' Builds Turned time signatures range. '''
    for source, target in turned_dict.iteritems():
        check_sources(source)
        decompose_components(source)
        new_glyph = Glyph()
        new_glyph.name = target
        s_indx = f.FindGlyph(source)
        source_glyph = f.glyphs[s_indx]
        source_wdth = source_glyph.width
        source_hght = source_glyph.height
        sx, sy = -1, -1  # scale to turn/reverse.
        dx, dy = source_wdth, source_hght

        new_glyph.components.append(Component(s_indx, Point(dx, dy), Point(sx, sy)))
        append_component_of_component(source_glyph, new_glyph)

        metrics = source_glyph.GetMetrics()
        new_glyph.SetMetrics(metrics)
        handle_preexisting(target)
        make_glyph(new_glyph, target)


def build_reversed_time():
    ''' Builds Reversed time signatures range. '''
    for source, target in reversed_dict.iteritems():
        check_sources(source)
        decompose_components(source)
        new_glyph = Glyph()
        new_glyph.name = target
        s_indx = f.FindGlyph(source)
        source_glyph = f.glyphs[s_indx]
        source_wdth = source_glyph.width
        sx, sy = -1, 1
        dx, dy = source_wdth, 0

        new_glyph.components.append(Component(s_indx, Point(dx, dy), Point(sx, sy)))
        append_component_of_component(source_glyph, new_glyph)

        metrics = source_glyph.GetMetrics()
        new_glyph.SetMetrics(metrics)
        handle_preexisting(target)
        make_glyph(new_glyph, target)


def build_ligatures():
    for target in ligatures:
        components = []
        shifts = []
        space = f.upm / 4
        denom = space
        numer = space * 3
        new_glyph = Glyph()
        new_glyph.name = target
        sources = target.split('_')

        for i, source in enumerate(sources):
            check_sources(source)
            decompose_components(source)
            s_indx = f.FindGlyph(source)
            source_glyph = f.glyphs[s_indx]
            source_wdth = source_glyph.width
            if source not in ctrl_char:
                x, y = 0, 0
                if sources[i - 1] == 'uniE09F':
                    y = denom
                else:
                    y = numer
                if len(sources) > 4:
                    shifts.append(source_wdth)
                    if i == 3:
                        x = shifts[0]
                    elif i == 5:
                        glyph_wdth = sum(shifts[:2])
                        glyph_center = source_wdth / 2
                        x = glyph_wdth / 2 - glyph_center

                components.append(Component(s_indx, Point(x, y)))

        for item in components:
            metrics = source_glyph.GetMetrics()
            if len(sources) > 4:
                metrics = Point(glyph_wdth, 0)
            new_glyph.SetMetrics(metrics)
            new_glyph.components.append(item)
        metrics = source_glyph.GetMetrics()
        if len(sources) > 4:
            metrics = Point(glyph_wdth, 0)
        new_glyph.SetMetrics(metrics)
        handle_preexisting(target)
        make_glyph(new_glyph, target)

    # Program:
print 'Starting ...'
build_fractions()
build_turned_time()
build_reversed_time()
build_cut_time()
build_ligatures()
fl.UpdateFont(fl.ifont)
print('All done!')

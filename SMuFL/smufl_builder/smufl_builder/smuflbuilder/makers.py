# (c) 2021 by Knut Nergaard.

from ConfigParser import SafeConfigParser
from FL import *

from smuflbuilder import data
from smuflbuilder import tools
from smuflbuilder import helpers
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)

SPACE = f.upm / 4


def barline_parents(name):
    '''Makes missing parent barline glyphs in Barlines and Repeats ranges.'''
    def draw_dashed_barline(glyph, registration, height):
        '''Draws dashed barline by superimposing reversed gap sized squares separated by dash length
        over thin barline and removing overlap. Indexes in loop are understood as 1/4 increments,
        since square's origin point is midpoint.
        '''
        width = helpers.configfloat('Barlines', 'dashed barline thickness')
        dash, gap = helpers.configfloat('Barlines', 'dashed barline dash length'), \
            helpers.configfloat('Barlines', 'dashed barline gap length')

        # Draw normal barline for dashes.
        tools.draw_square(glyph, registration, width, height)

        # Draw gaps and remove overlap.
        unit, stop = dash + gap, height * 2 - dash
        for quarter, _ in enumerate(helpers.generate_shifts(0, stop, unit)):
            diff = dash - gap
            init = quarter * 4
            start_height = init + 3
            gap_height = gap / 2
            x, y = 0, start_height * gap_height + diff * (quarter + 1)
            registration = Point(x, y)
            tools.draw_square(glyph, registration, width, -gap_height)  # -gap_height == rev. contour.
            glyph.RemoveOverlap()

    def draw_dotted_barline(glyph, registration, height):
        '''Draw dotted barline, rounding gap values to fit staff hight (4 spaces).'''
        radius = x = y = helpers.configfloat('Barlines', 'dotted barline dot radius')
        dot = width = radius * 2
        gap = dot + helpers.configfloat('Barlines', 'dotted barline gap length')
        unit, height = dot + gap, height * 2
        for num, _ in enumerate(helpers.generate_shifts(0, height, unit)):
            num_of_units = height / unit
            num_of_gaps = gap * num_of_units
            num_of_dots = dot * (num_of_units + 1)
            diff = (num_of_gaps + num_of_dots - height) / num_of_units
            x = y = radius
            registration = Point(x, y + (unit - diff) * num)
            tools.draw_circle(glyph, registration, radius)

    # Define and draw barline and dot elements acc. to spec.
    x, y = 0, SPACE * 2
    height = y
    width = helpers.configfloat('Barlines', 'thin barline thickness')
    if name == 'uniE034':  # barlineHeavy
        width = helpers.configfloat('Barlines', 'thick barline thickness')
    elif name == 'uniE038':  # barlineShort
        y = SPACE * 3
        height = SPACE
    elif name == 'uniE039':  # barlineTick
        y = SPACE * 4
        height = SPACE * 0.5
    elif name == 'uniE044':  # repeatDot
        x, y = helpers.configfloat('Repeats', 'repeat dot radius'), 0
        width = x * 2
    parent_glyph = Glyph()
    registration = Point(x, y)

    if name == 'uniE036':  # barlineDashed
        draw_dashed_barline(parent_glyph, registration, height)
        width = helpers.configfloat('Barlines', 'dashed barline thickness')
    elif name == 'uniE037':  # barlineDotted
        draw_dotted_barline(parent_glyph, registration, height)
        width = helpers.configfloat('Barlines', 'dotted barline dot radius') * 2
    elif name == 'uniE044':  # repeat dot
        tools.draw_circle(parent_glyph, registration,
                          helpers.configfloat('Repeats', 'repeat dot radius'))
    else:  # everything else
        tools.draw_square(parent_glyph, registration, width, height)
    metrics = Point(width, 0)
    helpers.append_glyph(parent_glyph, name, metrics)


def stave_parents(name, value):
    '''Makes missing parent stave and leger line glyphs in Barlines and Repeats ranges.'''
    # Define staffline dimensions.
    x = 0
    y = width = helpers.configfloat('Staves', 'medium staff line width')
    height = helpers.configfloat('Staves', 'staff line thickness') / 2
    if name == 'uniE016':
        width = helpers.configfloat('Staves', 'wide staff line width')
    elif name == 'uniE01C':
        width = helpers.configfloat('Staves', 'narrow staff line width')
    metrics = Point(width, 0)

    # Define leger line dimensions.
    if value is None:
        leger_extension = helpers.configfloat('Staves', 'leger line extension')
        x, y = -leger_extension, 0
        ext = leger_extension * 2
        height = helpers.configfloat('Staves', 'leger line thickness') / 2
        if name == 'uniE022':
            sidebearing = helpers.configfloat('Staves', 'narrow leger line width')
        elif name == 'uniE023':
            sidebearing = helpers.configfloat('Staves', 'medium leger line width')
        else:
            sidebearing = helpers.configfloat('Staves', 'wide leger line width')
        width = sidebearing + ext
        metrics = Point(sidebearing, 0)

    # Draw lines and append parent glyphs.
    parent_glyph = Glyph()
    registration = Point(x, y)
    tools.draw_square(parent_glyph, registration, width, height)
    helpers.append_glyph(parent_glyph, name, metrics)


def stem(name):
    '''Draws and appends note stem primitives.'''
    long_stem_length = helpers.configfloat('Stems', 'long stem length')
    x, y = 0, long_stem_length / 2
    stem_width = helpers.configfloat('Stems', 'stem thickness')
    stem_height = long_stem_length / 2
    metrics = Point(stem_width / 2, 0)

    # Handle long stem in Beamed groups of notes.
    if name in ('uniE204', 'uniE205'):
        # Get metrics based on noteheadBlack.
        note_index = f.FindGlyph(data.beamed_notes['uniE1F0'][1])
        note_glyph = f.glyphs[note_index]
        glyph_width = note_glyph.width
        x = glyph_width - stem_width
        retraction = helpers.configfloat('Stems', 'stem retraction')
        y += retraction / 2
        stem_height -= retraction / 2
        metrics = Point(glyph_width, 0)

        # Handle short stem in Beamed groups of notes.
        if name == 'uniE204':
            short_stem_length = helpers.configfloat('Stems', 'short stem length')
            diff = (long_stem_length - short_stem_length) / 2
            y -= diff
            stem_height -= diff

    # Draw and append glyph.
    parent_glyph = Glyph()
    regiastration = Point(x, y)
    tools.draw_square(parent_glyph, regiastration, stem_width, stem_height)
    helpers.append_glyph(parent_glyph, name, metrics)


def augmentation_dot(name):
    '''Draws and appends augmentation dot.'''
    radius = helpers.configfloat('Notes', 'augmentation dot radius')
    x, y = radius, 0
    width = radius * 2
    regiastration = Point(x, y)
    glyph = Glyph()
    tools.draw_circle(glyph, regiastration, radius)
    metrics = Point(width, 0)
    helpers.append_glyph(glyph, name, metrics)


def note_beam(name):
    '''Draws and appends beam in Beamed group of notes range.'''
    short_stem_length = helpers.configfloat('Stems', 'short stem length')
    beam_thickness = helpers.configfloat('Beams', 'beam thickness')
    beam_length = helpers.configfloat('Beams', 'beam length')

    x, y = 0, short_stem_length - beam_thickness / 2
    height, width = beam_thickness / 2, beam_length
    metrics = Point(width, 0)

    # Draw lines and append glyph.
    glyph = Glyph()
    registration = Point(x, y)
    tools.draw_square(glyph, registration, width, height)
    helpers.append_glyph(glyph, name, metrics)


def tuplet_bracket(name):
    '''Draws and appends tuplet bracket in Beamed group of notes range.'''
    # Horizontal stroke
    bracket_height = helpers.configfloat('Beams', 'tuplet height')
    hook_length = helpers.configfloat('Beams', 'tuplet bracket hook length')
    bracket_thickness = helpers.configfloat('Beams', 'tuplet bracket thickness')
    beam_length = helpers.configfloat('Beams', 'beam length')

    x, y = 0, bracket_height + hook_length
    horizontal_width = beam_length - bracket_thickness
    height = bracket_thickness / 2
    glyph = Glyph()
    regiastration = Point(x, y)
    tools.draw_square(glyph, regiastration, horizontal_width, height)

    # Vertical stroke
    x, y = 0, bracket_height + hook_length / 2
    vertical_width, height = bracket_thickness, hook_length / 2
    regiastration = Point(x, y)
    tools.draw_square(glyph, regiastration, vertical_width, height)
    glyph.RemoveOverlap()
    metrics = Point(horizontal_width, 0)
    helpers.append_glyph(glyph, name, metrics)


def accordion_rank(name):
    '''Draws and appends children for accordion registration.'''
    def draw_partition(glyph, radius, width, position, thickness):
        '''Draws partition lines in rank glyphs.'''
        diff = thickness / 2 + radius - width / 2
        x, y = diff, position
        height = thickness / 2
        registration = Point(x, y)
        tools.draw_square(glyph, registration, width, height)
        glyph.RemoveOverlap()

    glyph = Glyph()
    thickness = helpers.configfloat('Accordion', 'ranks line thickness')
    if name != 'uniE8C9':
        radius = helpers.configfloat('Accordion', 'round ranks radius')
        overshoot = helpers.configfloat('Accordion', 'round ranks overshoot')
        width = radius * 2
        tools.draw_circle_frame(glyph, radius, thickness, overshoot)
    else:
        width = helpers.configfloat('Accordion', 'square ranks width')
        height = helpers.configfloat('Accordion', 'square ranks height')
        radius = width / 2
        tools.draw_square_frame(glyph, width, height, thickness)

    for position, length in helpers.compile_part_data(name):
        draw_partition(glyph, radius, length, position, thickness)

    metrics = Point(width + thickness, 0)
    helpers.append_glyph(glyph, name, metrics)


def coupler_dot(name):
    '''Makes coupler dot glyph for accordion registrations.'''
    glyph = Glyph()
    radius = helpers.configfloat('Accordion', 'coupler dot radius')
    x = y = radius
    width = radius * 2
    registration = Point(x, y)
    tools.draw_circle(glyph, registration, radius)
    metrics = Point(width, 0)
    helpers.append_glyph(glyph, name, metrics)

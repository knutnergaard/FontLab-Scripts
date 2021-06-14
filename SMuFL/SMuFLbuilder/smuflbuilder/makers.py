"""Drawing module for SMuFLbuilder.

This module contains all functions to draw rudimentary (parent) glyphs.
It is built upon functions in .tools and relies heavily on user defined
values in config to produce particular glyph types, most of which are required
for composite builds. Functions in .helpers are used to append glyphs to
font.

Functions:

barlines() -- draws barlines and repeat dot
staves() -- draws staves and leger lines
stems() -- draws stems
augmentation_dot() -- draws augmentation dot
note_beam() -- draws beam for beamed notes
tuplet_bracket() -- draws tuplet bracket for beamed notes
ranks() -- draws ranks for accordion registration
coupler_dot() -- draws coupler dot for accordion registration
"""


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


def barlines(name):
    """Draws parent barline glyphs for Barlines and Repeats ranges."""
    def dashed_barline(glyph, registration, height):
        """Draws dashed barline.

        Superimposes reversed gap sized squares, separated by dash length,
        over full-length barline and removes overlap.

        Indexes in loop are understood as 1/4 increments, since square's
        origin point is midpoint.
        """
        width = helpers.configvalue('Barlines', 'dashed barline thickness')
        dash = helpers.configvalue('Barlines', 'dashed barline dash length')
        gap = helpers.configvalue('Barlines', 'dashed barline gap length')

        # Draw normal barline for dashes.
        tools.draw_rectangle(glyph, registration, width, height)

        # Draw gaps and remove overlap.
        unit, stop = dash + gap, height * 2 - dash
        for quarter, _ in enumerate(range(0, stop, unit)):
            diff = dash - gap
            init = quarter * 4
            start_height = init + 3
            gap_height = gap / 2
            x, y = 0, start_height * gap_height + diff * (quarter + 1)
            registration = Point(x, y)
            tools.draw_rectangle(glyph, registration, width, -gap_height)
            # -gap_height == rev. contour.
            glyph.RemoveOverlap()

    def dotted_barline(glyph, registration, height):
        """Draws dotted barline.

        Draws dots and spaces according to user specifications.
        Rounds gap values to fit staff hight (4 spaces).
        """
        radius = x = y = helpers.configvalue('Barlines',
                                             'dotted barline dot radius')
        dot = width = radius * 2
        gap = dot + helpers.configvalue('Barlines',
                                        'dotted barline gap length')
        unit, height = dot + gap, height * 2
        for num, _ in enumerate(range(0, height, unit)):
            num_of_units = height / unit
            num_of_gaps = gap * num_of_units
            num_of_dots = dot * (num_of_units + 1)
            diff = (num_of_gaps + num_of_dots - height) / num_of_units
            x = y = radius
            registration = Point(x, y + (unit - diff) * num)
            tools.draw_circle(glyph, registration, radius)

    # Define and draw barline and dot elements acc. to spec.
    print 'drawing ...'
    x, y = 0, SPACE * 2
    height = y
    width = helpers.configvalue('Barlines', 'thin barline thickness')
    if name == 'uniE034':  # barlineHeavy
        width = helpers.configvalue('Barlines', 'thick barline thickness')
    elif name == 'uniE038':  # barlineShort
        y = SPACE * 3
        height = SPACE
    elif name == 'uniE039':  # barlineTick
        y = SPACE * 4
        height = SPACE * 0.5
    elif name == 'uniE044':  # repeatDot
        x, y = helpers.configvalue('Repeats', 'repeat dot radius'), 0
        width = x * 2
    parent_glyph = Glyph()
    registration = Point(x, y)

    if name == 'uniE036':  # barlineDashed
        dashed_barline(parent_glyph, registration, height)
        width = helpers.configvalue('Barlines', 'dashed barline thickness')
    elif name == 'uniE037':  # barlineDotted
        dotted_barline(parent_glyph, registration, height)
        width = helpers.configvalue('Barlines',
                                    'dotted barline dot radius') * 2
    elif name == 'uniE044':  # repeat dot
        tools.draw_circle(parent_glyph, registration,
                          helpers.configvalue('Repeats',
                                              'repeat dot radius'))
    else:  # everything else
        tools.draw_rectangle(parent_glyph, registration, width, height)
    metrics = Point(width, 0)
    helpers.append_glyph(parent_glyph, name, metrics)


def staves(name, value):
    """Draws staff parents and leger line glyphs for Staves range."""
    # Define staffline dimensions.
    print 'drawing ...'
    x = 0
    y = width = helpers.configvalue('Staves', 'medium staff line width')
    height = helpers.configvalue('Staves', 'staff line thickness') / 2
    if name == 'uniE016':
        width = helpers.configvalue('Staves', 'wide staff line width')
    elif name == 'uniE01C':
        width = helpers.configvalue('Staves', 'narrow staff line width')
    metrics = Point(width, 0)

    # Define leger line dimensions.
    if not value:
        leger_extension = helpers.configvalue('Staves', 'leger line extension')
        x, y = -leger_extension, 0
        ext = leger_extension * 2
        height = helpers.configvalue('Staves', 'leger line thickness') / 2
        if name == 'uniE022':
            sidebearing = helpers.configvalue('Staves',
                                              'narrow leger line width')
        elif name == 'uniE023':
            sidebearing = helpers.configvalue('Staves',
                                              'medium leger line width')
        else:
            sidebearing = helpers.configvalue('Staves',
                                              'wide leger line width')
        width = sidebearing + ext
        metrics = Point(sidebearing, 0)

    # Draw lines and append parent glyphs.
    parent_glyph = Glyph()
    registration = Point(x, y)
    tools.draw_rectangle(parent_glyph, registration, width, height)
    helpers.append_glyph(parent_glyph, name, metrics)


def stems(name):
    """Draws note stem primitives for stem and note composites."""
    print 'drawing ...'
    long_stem_length = helpers.configvalue('Stems', 'long stem length')
    x, y = 0, long_stem_length / 2
    stem_width = helpers.configvalue('Stems', 'stem thickness')
    stem_height = long_stem_length / 2
    metrics = Point(stem_width / 2, 0)

    # Handle long stem in Beamed groups of notes.
    if name in {'uniE204', 'uniE205'}:
        # Get metrics based on noteheadBlack.
        note_index = f.FindGlyph(data.beamed_notes['uniE1F0'][1])
        note_glyph = f.glyphs[note_index]
        glyph_width = note_glyph.width
        x = glyph_width - stem_width
        retraction = helpers.configvalue('Stems', 'stem retraction')
        y += retraction / 2
        stem_height -= retraction / 2
        metrics = Point(glyph_width, 0)

        # Handle short stem in Beamed groups of notes.
        if name == 'uniE204':
            short_stem_length = helpers.configvalue('Stems', 'short stem length')
            diff = (long_stem_length - short_stem_length) / 2
            y -= diff
            stem_height -= diff

    # Draw and append glyph.
    parent_glyph = Glyph()
    registration = Point(x, y)
    tools.draw_rectangle(parent_glyph, registration, stem_width, stem_height)
    helpers.append_glyph(parent_glyph, name, metrics)


def augmentation_dot(name):
    """Draws augmentation dot for Individual Notes range."""
    print 'drawing ...'
    radius = helpers.configvalue('Notes', 'augmentation dot radius')
    x, y = radius, 0
    width = radius * 2
    registration = Point(x, y)
    glyph = Glyph()
    tools.draw_circle(glyph, registration, radius)
    metrics = Point(width, 0)
    helpers.append_glyph(glyph, name, metrics)


def note_beam(name):
    """Draws beam for Beamed group of notes range."""
    print 'drawing ...'
    short_stem_length = helpers.configvalue('Stems', 'short stem length')
    beam_thickness = helpers.configvalue('Beams', 'beam thickness')
    beam_length = helpers.configvalue('Beams', 'beam length')

    x, y = 0, short_stem_length - beam_thickness / 2
    height, width = beam_thickness / 2, beam_length
    metrics = Point(width, 0)

    # Draw lines and append glyph.
    glyph = Glyph()
    registration = Point(x, y)
    tools.draw_rectangle(glyph, registration, width, height)
    helpers.append_glyph(glyph, name, metrics)


def tuplet_bracket(name):
    """Draws tuplet bracket for Beamed group of notes range."""
    print 'drawing ...'
    # Horizontal stroke
    bracket_height = helpers.configvalue('Beams', 'tuplet height')
    hook_length = helpers.configvalue('Beams', 'tuplet bracket hook length')
    bracket_thickness = helpers.configvalue('Beams', 'tuplet bracket thickness')
    beam_length = helpers.configvalue('Beams', 'beam length')

    x, y = 0, bracket_height + hook_length
    horizontal_width = beam_length - bracket_thickness
    height = bracket_thickness / 2
    glyph = Glyph()
    registration = Point(x, y)
    tools.draw_rectangle(glyph, registration, horizontal_width, height)

    # Vertical stroke
    x, y = 0, bracket_height + hook_length / 2
    vertical_width, height = bracket_thickness, hook_length / 2
    registration = Point(x, y)
    tools.draw_rectangle(glyph, registration, vertical_width, height)
    glyph.RemoveOverlap()
    metrics = Point(horizontal_width, 0)
    helpers.append_glyph(glyph, name, metrics)


def dynamics(name):
    """Draws dynamic hairpin and niente circle

    Determines vertical registration of hairpin from range x-height,
    in additon to user specs.
    """
    glyph = Glyph()
    if name == 'uniE53E':
        width = helpers.configvalue('Dynamics', 'hairpin length')
        aperture = helpers.configvalue('Dynamics', 'hairpin aperture')
        thickness = helpers.configvalue('Dynamics', 'hairpin line thickness')
        offset = helpers.configvalue('Dynamics', 'hairpin height adjustment')

        # Base x-height/hairpin height on n, m, r, z or s (in that order).
        x_heights = ('uniE526', 'uniE521', 'uniE523', 'uniE525', 'uniE524')
        for item in x_heights:
            if f.has_key(item):
                l_height = helpers.get_bbox(item).height / 2 + offset
                break
            else:
                l_height = SPACE / 2 + offset
        r_height = aperture / 2
        x, y = 0, l_height + offset
        registration = Point(x, y)

        tools.draw_slash(glyph, registration, width, 0, r_height, thickness)
        tools.draw_slash(glyph, registration, width, 0, -r_height, thickness)

    else:
        # Draw niente circle.
        radius = helpers.configvalue('Dynamics', 'niente radius')
        thickness = helpers.configvalue('Dynamics', 'niente line thickness')
        width = radius * 2
        x, y = radius + thickness / 2, 0
        registration = Point(x, y)
        tools.draw_circle_frame(glyph, registration, radius, thickness)

    glyph.RemoveOverlap()
    metrics = Point(width, 0)
    helpers.append_glyph(glyph, name, metrics)


def ranks(name):
    """Draws empty ranks for accordion registration."""
    def partition(glyph, radius, width, position, thickness):
        """Draws partition lines for ranks."""
        diff = thickness / 2 + radius - width / 2
        x, y = diff, position
        height = thickness / 2
        registration = Point(x, y)
        tools.draw_rectangle(glyph, registration, width, height)
        glyph.RemoveOverlap()

    print 'drawing ...'
    glyph = Glyph()
    width = 0
    thickness = helpers.configvalue('Accordion', 'ranks line thickness')
    if name != 'uniE8C9':
        radius = helpers.configvalue('Accordion', 'round ranks radius')
        width = radius * 2
        overshoot = helpers.configvalue('Accordion', 'round ranks overshoot')
        x = radius + thickness / 2
        y = x + overshoot
        registration = Point(x, y)
        tools.draw_circle_frame(glyph, registration, radius, thickness)
    else:
        width = helpers.configvalue('Accordion', 'square ranks width')
        height = helpers.configvalue('Accordion', 'square ranks height')
        x, y = 0, (height + thickness) / 2
        registration = Point(x, y)
        radius = width / 2
        tools.draw_rect_frame(glyph, registration, width, height, thickness)

    for position, length in helpers.compile_part_data(name):
        partition(glyph, radius, length, position, thickness)

    metrics = Point(width + thickness, 0)
    helpers.append_glyph(glyph, name, metrics)


def coupler_dot(name):
    """Draws coupler dot for accordion registrations."""
    print 'drawing ...'
    glyph = Glyph()
    radius = helpers.configvalue('Accordion', 'coupler dot radius')
    x = y = radius
    width = radius * 2
    registration = Point(x, y)
    tools.draw_circle(glyph, registration, radius)
    metrics = Point(width, 0)
    helpers.append_glyph(glyph, name, metrics)

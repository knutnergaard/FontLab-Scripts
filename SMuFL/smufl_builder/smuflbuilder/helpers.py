"""Helper module for SMuFLbuilder.

This module contains various helper functions for SMuFL builder.
They are mainly called by the various type-/range-specific funtions in
.builders and .makers. Many functions rely on user-defined values from
config, and some imports data from .data. Additionally, strftime() and
.math are imported to aid particular functions.

Functions:

configvalue() -- returns config value format, depending on cofig. setting
check_excluded() -- checks config [Excluded] for name and returns boolean
check_complete() -- checks glyph presence in font. Informs and returns boolean
def decompose() -- decomposes preexisting components used in building
get_bbox() -- gets glyph bounding box from glyphname
get_kerning() -- gets kerning value from glyph pair
compile_part_data() -- 'data compiler' for drawing accordion ranks correctly
timestamp() -- creates strftime-friendly timestamp from config
handle_replaced() -- applies timestamp + unicode 0 and/or returns boolean
append_glyph() -- applies name, unicode and mark before appending glyph to font
print_incomplete(name) -- returns print statement for incomplete composites
"""

# (c) 2021 by Knut Nergaard.

from ConfigParser import SafeConfigParser
from time import localtime, strftime
import math
import re

from FL import *

from smuflbuilder import data
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)
checked = set()  # global set to check execution of local processes.

SPACE = f.upm / 4


def configvalue(section, option):
    """Returns config option value as 'staff spaces', font units or str().

    Determines numerical type from [Global][values in staff spaces].
    String is returned if float/int is False.
    Exceptions enclosed in parenthesis are stripped and converted to numbers.

    'staff spaces' is defined as font upm/4', according to SMuFL specification,
    in constant SPACE.
    """
    try:
        if config.getboolean('Global', 'values in staff spaces'):
            return int(config.getfloat(section, option) * SPACE)
        return (config.getint(section, option))
    except ValueError:
        string = config.get(section, option)
        # Regex to earch for numbers or period in parenthesis.
        if not re.search(r'\([0-9]|[0-9][.]\)', string):
            return string
        if config.getboolean('Global', 'values in staff spaces'):
            return int(float(string.strip('()')))
        return int(float(string.strip('()')) * SPACE)


def check_excluded(name):
    """Checks input against list of excluded glyphs in config file.

    Prints message if matched and returns boolean to skip/proceed.
    """
    try:
        if not config.has_option('Exclude', name):
            return False
        elif not config.getboolean('Exclude', name):
            return False
        else:
            print('Skipping excluded glyph: {}'.format(name))
            return True
    except AttributeError:
        return False


def check_complete(name):
    """Checks if glyph in font, informs and returns boolean to skip/proceed.

    Avoids repeated messaging by adding glyphaname to global set checked and
    checking set for name on further iterations.
    """
    global checked
    if f.has_key(name):
        return True
    elif name not in checked:
        print('\nParent glyph {} is missing!'.format(name))
        checked.add(name)
    return False


def decompose(name):
    """Decomposes preexisting components."""
    for g in f.glyphs:
        num_of_comps = len(g.components)
        if g.name in data.do_not_decompose:
            return
        elif g.name == name and num_of_comps > 0:
            g.Decompose()
            print('Decomposing: {}'.format(g.name))


def get_bbox(name):
    """Returns bounding box of specified glyph."""
    if f.has_key(name):
        index = f.FindGlyph(name)
        glyph = f.glyphs[index]
        return glyph.GetBoundingRect()
    return None


def get_kerning(left, right):
    """gets kerning value from left and right (parent and key) names."""
    left_index = f.FindGlyph(left)
    right_index = f.FindGlyph(right)
    kerning = f.glyphs[left_index].kerning
    for pair in kerning:
        if kerning and pair.value and right_index == pair.key:
            return pair.value
    return 0


def compile_part_data(name):
    """Compiles data to correctly draw rank partitions.

    Calculates correct length of partition lines (tangents) and determines
    their vertical position based on frame diameter/width and height.
    """
    radius = configvalue('Accordion', 'round ranks radius')
    overshoot = configvalue('Accordion', 'round ranks overshoot')
    thickness = configvalue('Accordion', 'ranks line thickness')
    width = configvalue('Accordion', 'square ranks width')

    def calculate_tangent(radius, position):
        """Calculates tangent length at given position accross diameter."""
        offset = position - radius - thickness / 2
        exp = (radius ** 2 - offset ** 2)
        return math.sqrt(exp) * 2

    def compile_positions(name):
        """Determines vertical positions to draw rank partitions."""
        height = (radius + overshoot) * 2
        if name == 'uniE8C9':
            height = configvalue('Accordion', 'square ranks height')
        increment = (height / data.accordion_ranks[name])
        start = increment + thickness / 2
        end = start * data.accordion_ranks[name] - thickness * 2
        return range(start, end, increment)

    def compile_lengths(name):
        """Compiles correct lengths of partition lines."""
        if name == 'uniE8C9':
            return [width for position in compile_positions(name)]
        return [calculate_tangent(radius, position)
                for position in compile_positions(name)]

    return zip(compile_positions(name), compile_lengths(name))


def timestamp():
    """Creates strftime-friendly user-specified timestamp.

    Restricts character usage to ensure correct formatting and informs if
    invalid. prepends each character in raw stamp with modulus (%) to make
    readable by strftime.
    """
    raw = config.get('Global', 'timestamp')
    allowed = {'Y', 'm', 'd', 'H', 'M', 'S', '.', ':', '-', '_'}
    stamp_set = {item for item in raw}
    # Raise error if timestamp in config contains invalid characters.
    if not allowed.issuperset(stamp_set):
        raise ValueError('Please choose a valid setting for [Global]'
                         '[timestamp] in file:\n{}!'.format(filepaths.user))
    # Prepend each character with % to make strftime-friendly.
    stampform = '%' + '%'.join(raw)
    return strftime(stampform, localtime())


def handle_replaced(name):
    """Checks for preexisting glyphs and validity of [Global][handle replaced].

    Appends timestamp to name and/or returns boolean to skip or append glyph,
    depending on setting in config.
    """
    option = config.getint('Global', 'handle replaced')
    if option > 2:
        raise ValueError('Please choose a valid setting for [Global]'
                         '[handle replaced] in file:\n{}!'.format(filepaths.user))
    if not f.has_key(name):
        return
    elif option == 0:
        return False
    elif option == 1:
        from time import localtime, strftime
        index = f.FindGlyph(name)
        old_glyph = f.glyphs[index]
        old_glyph.name = '{}_{}'.format(old_glyph.name, timestamp())
        old_glyph.unicode = 0
        return True
    return True


def append_glyph(glyph, name, metrics):
    """Appends new glyphs with mark colour if handle_replaced() is True.

    Prints message if False and sets unicode to 0 for stylistic alternates and
    non-conventional glyphnames.
    """
    if handle_replaced(name) is False:
        print('Skipping preexisting: {}'.format(name))
        return

    glyph.name = name
    try:
        glyph.unicode = int(name[3:], 16)
    # exception to handle names with alt. suffixes
    except ValueError:
        glyph.unicode = 0
    glyph.mark = config.getint('Global', 'mark colour')
    glyph.SetMetrics(metrics)
    f.glyphs.append(glyph)
    print('Appending: {}'.format(name))


def print_incomplete(name):
    """Print statement for incomplete composites in builders."""
    print('Skipping incomplete composite: {}'.format(name))

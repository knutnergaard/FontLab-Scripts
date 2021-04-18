# (c) 2021 by Knut Nergaard.

from ConfigParser import SafeConfigParser
import math

from FL import *

from smuflbuilder import data
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)

SPACE = f.upm / 4


def configfloat(section, name):
    '''Returns config file value in staff spaces (upm / 4) or font units,
    depending on Global setting. Returns string if float is False.
    '''
    try:
        if config.getboolean('Global', 'values in staff spaces') is True:
            return int(config.getfloat(section, name) * SPACE)
        return (config.getint(section, name))
    except ValueError:
        return config.get(section, name)


def check_excluded(name):
    '''Checks input against list of excluded glyphs in config file. Prints message if matched.'''
    try:
        if config.has_option('Exclude', name) and config.getboolean('Exclude', name) is True:
            print('Skipping excluded glyph: {}'.format(name))
            return True
    except AttributeError:
        return False


def decompose(name):
    '''Decomposes preexisting components.'''
    for g in f.glyphs:
        num_of_comps = len(g.components)
        if g.name == name and num_of_comps > 0 and g.name not in data.do_not_decompose:
            g.Decompose()
            print('Decomposing: {}'.format(g.name))


def generate_shifts(start, end, increment):
    '''Generates delta shift values for components.'''
    current = start
    while current < end:
        yield current
        current += increment


def compile_part_data(name):
    '''Compiles data to correctly draw rank partitions.'''
    radius = configfloat('Accordion', 'round ranks radius')
    overshoot = configfloat('Accordion', 'round ranks overshoot')
    thickness = configfloat('Accordion', 'ranks line thickness')
    width = configfloat('Accordion', 'square ranks width')

    def calculate_tangent(radius, position):
        '''Calculates length of tangent at given position accross cricle diameter.'''
        offset = position - radius - thickness / 2
        exp = (radius ** 2 - offset ** 2)
        return math.sqrt(exp) * 2

    def compile_positions(name):
        '''Compiles vertical positions to draw rank partitions.'''
        height = (radius + overshoot) * 2
        if name == 'uniE8C9':
            height = configfloat('Accordion', 'square ranks height')
        increment = (height / data.accordion_ranks[name])
        start = increment + thickness / 2
        end = start * data.accordion_ranks[name] - thickness * 2
        return generate_shifts(start, end, increment)

    def compile_lengths(name):
        '''Compiles correct lengths of partition lines.'''
        if name == 'uniE8C9':
            return [width for position in compile_positions(name)]
        return [calculate_tangent(radius, position) for position in compile_positions(name)]
    return zip(compile_positions(name), compile_lengths(name))


def move_preexisting(name):
    '''Changes name and unicode of any preexisting glyphs.
    Potentially find a way to add 1 to number at end of string automatically.
    '''
    if f.has_key(name):
        index = f.FindGlyph(name)
        old_glyph = f.glyphs[index]
        init = 1
        old_glyph.name = '{}_{}'.format(old_glyph.name, init)


def append_glyph(glyph, name, metrics):
    '''Appends new glyphs with chosen mark colour (stylistic alt. unicode = 0).'''
    glyph.name = name
    try:
        glyph.unicode = int(name[3:], 16)
    except ValueError:
        glyph.unicode = 0
    glyph.mark = config.getint('Global', 'mark colour')
    glyph.SetMetrics(metrics)
    f.glyphs.append(glyph)
    print('Appending: {}'.format(name))

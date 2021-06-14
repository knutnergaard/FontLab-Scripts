#FLM: SMuFLbuilder

"""Top level script for SMuFLbuilder.

This script contains main and alternate builder executions, as well as
functions to compile alternte datasets.

Functions:

compile_dataset() -- adds suffixes etc. to compile dataset for alts
exe_altbuilder() -- executes all alternate builders
exe_builder() -- executes all main range builders
main() -- executes script
"""

# (c) 2021 by Knut Nergaard.

from ConfigParser import SafeConfigParser
from FL import *

if not fl.font:
    raise Exception('Please open a font!')

from smuflbuilder import data
from smuflbuilder import builders
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)


def compile_dataset(sfx, glyphdata):
    """Compiles new dataset for stylistic sets.

    builds new names from defaults and suffix in config."""
    new_data = {k + sfx: [i + sfx for i in v] for k, v in glyphdata.iteritems()}
    if sfx.endswith(config.get('Set Suffixes', 'short flags')):
        # Pair dflt base flags uniE242 and uniE242 with short int. flags.
        new_data = {k + '.' + sfx: [i + sfx if i == 'uniE242' or i == 'uniE243'
                                    else i for i in v] for k, v in
                    data.flags.iteritems()}

    elif sfx.endswith(config.get('Set Suffixes', 'straight flags')):
        new_data = {k + sfx: ['uniE240' + sfx if i == 'uniE250' or i == 'uniE242'
                              else 'uniE241' + sfx for i in v] for k, v in
                    glyphdata.iteritems()}
        # Add keys for flag16thUpStraight and flag16thDownStraight.
        new_data['uniE242' + sfx] = ['uniE240' + sfx]
        new_data['uniE243' + sfx] = ['uniE241' + sfx]
        # Add straight 8th flag (up/down) to each
        # key to build from single character.
        for k, v in new_data.iteritems():
            v.append(('uniE240' + sfx) if 'uniE240' + sfx in v
                     else v.append('uniE241' + sfx))
    return new_data


def exe_altbuilder(glyphrange):
    """Executes builders for add. datasets, alts, sets and ligas."""
    if glyphrange == data.ranges['repeats']:
        if config.getboolean('Include', 'alternates'):
            builders.barlines(data.repeat_barlines_alt)

    elif glyphrange == data.ranges['time']:
        if config.getboolean('Include', 'ligatures'):
            builders.time_ligatures(data.time_ligatures)

        stylesets = ('large time signatures', 'large narrow time signatures')
        for styleset in stylesets:
            if config.getboolean('Include', styleset):
                suffix = '.' + config.get('Set Suffixes', styleset)
                builders.cut_time(compile_dataset(suffix,
                                                  data.cut_time_common))
                builders.fraction_time(compile_dataset(suffix,
                                                       data.time_fractions))

    elif glyphrange == data.ranges['time sup']:
        stylesets = ('large time signatures', 'large narrow time signatures')
        for styleset in stylesets:
            if config.getboolean('Include', styleset):
                suffix = '.' + config.get('Set Suffixes', styleset)
                builders.cut_time(compile_dataset(suffix,
                                                  data.cut_time_common))
                builders.fraction_time(compile_dataset(suffix,
                                                       data.time_fractions))

    elif glyphrange == data.ranges['flags']:
        stylesets = ('small staff', 'short flags', 'straight flags')
        for styleset in stylesets:
            if config.getboolean('Include', styleset):
                suffix = '.' + config.get('Set Suffixes', styleset)
                builders.flags(compile_dataset(suffix, data.flags))

    elif glyphrange == data.ranges['indv notes']:
        if config.getboolean('Include', 'alternates'):
            builders.indv_notes(data.indv_notes_alt)

    elif glyphrange == data.ranges['octaves']:
        if config.getboolean('Include', 'alternates'):
            builders.indv_notes(data.octaves_alt)


def exe_builder(glyphrange, builder, dataset):
    """Executes main range builders.

    Calls altbuilder if range in alternates.
    """
    if not config.getboolean('Include', glyphrange):
        return
    print('\nGenerating {} ...'.format(glyphrange))
    if config.getboolean('Include', 'characters'):
        builder(dataset)
        # Execute extra builder (fractions) for Time Signatures.
        if glyphrange == data.ranges['time']:
            builders.fraction_time(data.time_fractions)
    else:
        print('Skipping recommended characters ...')

    # Call altbuilder if allternates, print message if not.
    has_alternates = {'repeats', 'time', 'flags', 'indv notes', 'octaves'}
    if glyphrange not in {data.ranges[key] for key in has_alternates}:
        print('\nNo supported alternates in included range(s).')
    else:
        alttypes = ('alternates', 'ligatures', 'small staff',
                    'short flags', 'straight flags')
        altbools = {config.getboolean('Include', alttype)
                    for alttype in alttypes}
        if any(altbools):
            exe_altbuilder(glyphrange)
        else:
            print('Skipping alternate glyphs ...')

    return False


def main():
    """Creates list of booleans in config('Include').

    Executes script if settings found and anything is True.
    Informs if not.
    """
    if not config.has_section('Include'):
        print('Unable to read settings: {}'.format(filepaths.user))
        return

    booleans = [config.getboolean('Include', boolean)
                for boolean in config.options('Include')]

    if not any(booleans):
        print('Please select a range to build in \n{} '
              '\nand try again!'.format(filepaths.user))
        return

    print('Starting ...')
    exe_builder(data.ranges['staves'], builders.staves, data.staves)
    exe_builder(data.ranges['barlines'], builders.barlines, data.barlines)
    exe_builder(data.ranges['repeats'],
                builders.barlines, data.repeat_barlines)
    exe_builder(data.ranges['time'],
                builders.cut_time, data.cut_time_common)
    exe_builder(data.ranges['time sup'],
                builders.cut_time, data.cut_time_sup)
    exe_builder(data.ranges['turned time'],
                builders.mirror_time, data.turned_time)
    exe_builder(data.ranges['reversed time'],
                builders.mirror_time, data.reversed_time)
    exe_builder(data.ranges['stems'], builders.stems, data.stems)
    exe_builder(data.ranges['tremolos'], builders.tremolos, data.tremolos)
    exe_builder(data.ranges['indv notes'],
                builders.indv_notes, data.indv_notes)
    exe_builder(data.ranges['beamed notes'],
                builders.beamed_notes, data.beamed_notes)
    exe_builder(data.ranges['flags'], builders.flags, data.flags)
    exe_builder(data.ranges['octaves'], builders.octaves, data.octaves)
    exe_builder(data.ranges['octaves sup'],
                builders.octaves, data.octaves_sup)
    exe_builder(data.ranges['dynamics'], builders.dynamics, data.dynamics)
    exe_builder(data.ranges['accordion'], builders.accordion_reg,
                (data.accordion_ranks, data.accordion_reg))

    fl.UpdateFont(fl.ifont)
    print('\nAll done!')


main()

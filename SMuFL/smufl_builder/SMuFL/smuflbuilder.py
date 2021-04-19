#FLM: SMuFL Builder

# (c) 2021 by Knut Nergaard.
# Use, modify and distribute as desired.

from ConfigParser import SafeConfigParser
from FL import *

from smuflbuilder import data
from smuflbuilder import builders
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)

SPACE = f.upm / 4

if f is None:
    raise Exception('Please open a font first!')


def build_setdata(sfx, glyphdata):
    '''Builds new dataset for stylistic sets from default data and suffix.'''
    new_data = {k + sfx: [i + sfx for i in v] for k, v in glyphdata.iteritems()}
    if sfx.endswith(config.get('Set Suffixes', 'short flags')):
        # Pair default base flags uniE242 and uniE242 with dedicated short internal flags.
        new_data = {k + '.' + sfx: [i + sfx if i == 'uniE242' or i == 'uniE243' else
                                    i for i in v] for k, v in data.flags.iteritems()}

    elif sfx.endswith(config.get('Set Suffixes', 'straight flags')):
        new_data = {k + sfx: ['uniE240' + sfx if i == 'uniE250' or i == 'uniE242' else
                              'uniE241' + sfx for i in v] for k, v in glyphdata.iteritems()}
        # Add keys for flag16thUpStraight and flag16thDownStraight.
        new_data['uniE242' + sfx] = ['uniE240' + sfx]
        new_data['uniE243' + sfx] = ['uniE241' + sfx]
        # Add straight 8th flag (up/down) to each key to build from single character.
        for k, v in new_data.iteritems():
            v.append('uniE240' + sfx) if 'uniE240' + sfx in v else v.append('uniE241' + sfx)

    return new_data


def exe_altbuilder(glyphrange):
    '''Executes builders for additional datasets, alternates, sets and ligatures.'''
    if glyphrange == data.ranges['repeats']:
        if config.getboolean('Include', 'alternates') is True:
            builders.barlines(data.repeat_barlines_alt)

    elif glyphrange == data.ranges['time']:
        builders.fraction_time(data.time_fractions)
        if config.getboolean('Include', 'ligatures') is True:
            builders.time_ligatures(data.time_ligatures)

    elif glyphrange == data.ranges['flags']:
        stylesets = ('small staff', 'short flags', 'straight flags')
        for styleset in stylesets:
            if config.getboolean('Include', styleset) is True:
                suffix = '.' + config.get('Set Suffixes', styleset)
                builders.flags(build_setdata(suffix, data.flags))


def exe_builder(glyphrange, builder, dataset):
    '''Executes main range builder and calls alternate builder if range in alternates.'''
    if config.getboolean('Include', glyphrange) is True:
        print('\nGenerating {} ...'.format(glyphrange))
        if config.getboolean('Include', 'characters') is True:
            builder(dataset)
        else:
            print('Skipping recommended characters ...')

        has_alternates = (data.ranges['repeats'], data.ranges['time'], data.ranges['flags'])
        if glyphrange in has_alternates:
            alttypes = ('alternates', 'ligatures', 'small staff', 'short flags', 'straight flags')
            altbools = [config.getboolean('Include', alttype) for alttype in alttypes]

            if any(altbools):
                exe_altbuilder(glyphrange)
            else:
                print('Skipping alternate glyphs ...')
        else:
            print('\nNo supported alternates in included range(s).')
    return False


# Program: -----------------------------------------------------------------

def main():
    '''Creates list of booleans in config('Include'). Executes script if anything is True.
    Prints message to enable range if not.
    '''
    booleans = [config.getboolean('Include', boolean) for boolean in config.options('Include')]

    if any(booleans):
        print('Starting ...')
        exe_builder(data.ranges['staves'], builders.staves, data.staves)
        exe_builder(data.ranges['barlines'], builders.barlines, data.barlines)
        exe_builder(data.ranges['repeats'], builders.barlines, data.repeat_barlines)
        exe_builder(data.ranges['time'], builders.cut_time, data.cut_time_common)
        exe_builder(data.ranges['time sup'], builders.cut_time, data.cut_time_sup)
        exe_builder(data.ranges['turned time'], builders.mirror_time, data.turned_time)
        exe_builder(data.ranges['reversed time'], builders.mirror_time, data.reversed_time)
        exe_builder(data.ranges['stems'], builders.stems, data.stems)
        exe_builder(data.ranges['tremolos'], builders.tremolos, data.tremolos)
        exe_builder(data.ranges['indv notes'], builders.indv_notes, data.indv_notes)
        exe_builder(data.ranges['beamed notes'], builders.beamed_notes, data.beamed_notes)
        exe_builder(data.ranges['flags'], builders.flags, data.flags)
        exe_builder(data.ranges['accordion'], builders.accordion_reg,
                    (data.accordion_ranks, data.accordion_reg))

        fl.UpdateFont(fl.ifont)
        print('\nAll done!')

    else:
        print 'Please include a range in {} and try again!'.format(filepaths.user)


main()

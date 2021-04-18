# (c) 2021 by Knut Nergaard.


from ConfigParser import SafeConfigParser
from FL import *

from smuflbuilder import data
from smuflbuilder import tools
from smuflbuilder import helpers
from smuflbuilder import makers
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)

SPACE = f.upm / 4


def barlines(glyphdata):
    '''Draws non-existent parent glyphs (except uniE037),
    cand builds omposites in Barline and Repeat ranges.
    '''
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        bbox_widths = []
        separations = []
        components = []

        for i, parent in enumerate(parents):
            if not f.has_key(parent):
                print('\nSource glyph {} is missing!'.format(parent))
                makers.barline_parents(parent)
            helpers.decompose(parents)

            # Get bounding boxes.
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            bbox_width = parent_glyph.GetBoundingRect().width
            bbox_widths.append(bbox_width)

            # Set separation parameters.
            separation = helpers.configfloat('Barlines', 'barline separation')
            if parents[i] == 'uniE044' or parents[i - 1] == 'uniE044':
                separation = helpers.configfloat('Repeats', 'repeat barline dot separation')

            if parent == 'uniE044':
                if i in (1, 3, 6) or i == len(parents) - 1:
                    separation = -bbox_width

            if i == 0:
                separation = 0
            separations.append(separation)

            # Set shifts for repeat dots.
            dx, dy = sum(bbox_widths[:-1] + separations), 0
            if parent == 'uniE044':
                dy = SPACE * 1.5 if i % 2 == 1 else SPACE * 2.5

            # Append components.
            new_glyph = Glyph()
            components.append(Component(parent_index, Point(dx, dy)))

        for item in components:
            new_glyph.components.append(item)

        # Append glyphs unless child is None.
        if child is not None:
            new_width = sum(bbox_widths + separations)
            metrics = Point(new_width, 0)
            helpers.move_preexisting(child)
            helpers.append_glyph(new_glyph, child, metrics)


def staves(glyphdata):
    '''Draws non-existent parent glyphs and builds composite glyphs in Staves range.'''
    for parent, children in glyphdata.iteritems():
        if not f.has_key(parent):
            print('\nSource glyph {} is missing!'.format(parent))
            makers.stave_parents(parent, children)
        helpers.decompose(parent)

        if children:
            for child in children:
                if helpers.check_excluded(child) is True:
                    continue

                # Determine base y values for initial components
                # in glyphs with odd vs. even number of lines.
                num_of_lines = children.index(child) + 2
                baseline = SPACE / 2 if num_of_lines % 2 == 0 else 0
                glyph_height = SPACE * num_of_lines / 2

                # Generate shift values for subsequent components.
                shifts = helpers.generate_shifts(baseline, glyph_height, SPACE)
                new_glyph = Glyph()
                parent_index = f.FindGlyph(parent)
                parent_glyph = f.glyphs[parent_index]

                # Append components with + and - shift values to new glyph.
                dx, dy = 0, 0
                for dy in shifts:
                    new_glyph.components.append(Component(parent_index, Point(dx, dy)))
                    if dy > 0:
                        new_glyph.components.append(Component(parent_index, Point(dx, -dy)))

                # Append new glyph to font.
                metrics = parent_glyph.GetMetrics()
                helpers.move_preexisting(child)
                helpers.append_glyph(new_glyph, child, metrics)


def cut_time(glyphdata):
    '''Builds cut time composites in Time signatures supplement range.'''
    for parent, child in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        if not f.has_key(parent):
            print('Skipping missing parent glyph: {}'.format(parent))
            continue

        stroke = helpers.configfloat('Time Signatures', 'cut time stroke')
        if not f.has_key(stroke):
            print('Skipping missing parent glyph: {}'.format(stroke))
            continue
        helpers.decompose(parent)

        new_glyph = Glyph()
        parent_index = f.FindGlyph(parent)
        parent_glyph = f.glyphs[parent_index]
        dx, dy = 0, 0
        new_glyph.components.append(Component(parent_index, Point(dx, dy)))

        # Get index of cut time stroke glyph, and center in main parent glyph.
        stroke_index = f.FindGlyph(stroke)
        parent_width = parent_glyph.GetBoundingRect().width
        parent_center = parent_width / 2
        dx, dy = parent_center, 0
        new_glyph.components.append(Component(stroke_index, Point(dx, dy)))

        metrics = parent_glyph.GetMetrics()
        helpers.move_preexisting(child)
        helpers.append_glyph(new_glyph, child, metrics)


def fraction_time(glyphdata):
    '''Builds Time signature fraction composites.'''
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        parent_widths = []

        new_glyph = Glyph()
        for i, parent in enumerate(parents):
            if not f.has_key(parent):
                print('Skipping missing parent glyph: {}'.format(parent))
                continue
            helpers.decompose(parent)

            # Define scale, shift, spacing and kerning for fraction glyphs acc. to spec.
            sidebearings = helpers.configfloat('Time Signatures', 'fraction sidebearings')
            spacing = helpers.configfloat('Time Signatures', 'fraction spacing')
            one_kern = helpers.configfloat('Time Signatures', 'fraction one kern')
            four_kern = helpers.configfloat('Time Signatures', 'fraction four kern')
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            parent_width = parent_glyph.width
            sx = sy = 1  # 1 = 100% (x, y)
            dx = dy = 0
            num_factor = 0.5  # reflects current scaling factor of slash vs. numerals in Bravura
            if i != 1:
                parent_width = parent_glyph.width * num_factor + sidebearings
                sx, sy = sx * num_factor, sy * num_factor
                if i == 0:
                    dx, dy = sidebearings, SPACE / 2
                    if parent == 'uniE081':
                        parent_width += one_kern
                else:
                    dx, dy = parent_widths[0] + spacing * 2, -SPACE / 2
                    if parent == 'uniE084':
                        dx += four_kern
                        parent_width += four_kern
            else:
                dx = parent_widths[i - 1] - parent_width / 2 + spacing

            parent_widths.append(parent_width)
            new_glyph.components.append(Component(parent_index, Point(dx, dy),
                                                  Point(sx, sy)))

        new_width = parent_widths[0] + parent_widths[2] + spacing * 2
        metrics = Point(new_width, 0)
        helpers.move_preexisting(child)
        helpers.append_glyph(new_glyph, child, metrics)


def mirror_time(glyphdata):
    '''Builds composites in Turned/Reversed time signatures ranges,
    retaining cutTimeCommon composite.
    '''
    for parent, child in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        if not f.has_key(parent):
            print('Skipping missing parent glyph: {}'.format(parent))
            continue
        stroke = helpers.configfloat('Time Signatures', 'cut time stroke')
        if not f.has_key(stroke):
            print('Skipping missing parent glyph: {}'.format(stroke))
            continue
        helpers.decompose(parent)

        new_glyph = Glyph()
        parent_index = f.FindGlyph(parent)
        parent_glyph = f.glyphs[parent_index]
        dx, dy, sx, sy = parent_glyph.width, parent_glyph.height, -1, -1  # turn
        if glyphdata == data.reversed_time:
            dx, dy, sx, sy = parent_glyph.width, 0, -1, 1  # reverse
        new_glyph.components.append(Component(parent_index, Point(dx, dy), Point(sx, sy)))

        # Append component if cut time is component.
        if parent == 'uniE08B' and parent_glyph.components:
            stroke_index = f.FindGlyph(stroke)
            stroke_glyph = f.glyphs[stroke_index]

            for c in parent_glyph.components:
                if c.index == stroke_index:
                    dx = (parent_glyph.width + stroke_glyph.width) * 0.5
                new_glyph.components.append(Component(c.index, Point(dx, dy), Point(sx, sy)))

        metrics = parent_glyph.GetMetrics()
        helpers.move_preexisting(child)
        helpers.append_glyph(new_glyph, child, metrics)


def time_ligatures(glyphdata):
    '''Builds recommended ligatures in Time Signatures range. Target name and numerator/
    denominator is determined by ligature name (underscore and ctrl character).
    '''
    for child in glyphdata:
        if helpers.check_excluded(child) is True:
            continue

        components = []
        shifts = []

        parents = child.split('_')
        for i, parent in enumerate(parents):
            if not f.has_key(parent):
                print('Skipping missing parent glyph: {}'.format(parent))
                continue
            helpers.decompose(parent)

            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]

            # Define parameters for Time Signature ligatures.
            if glyphdata == data.time_ligatures:
                dx, dy = 0, 0
                if parent not in data.ctrl_char:
                    # Set vertical shift values for denominator and numerator.
                    dy = SPACE if parents[i - 1] == 'uniE09F' else SPACE * 3
                    # Set horizontal shifts and spacing for ligatures with double digit numerator.
                    if len(parents) > 4:
                        shifts.append(parent_glyph.width)
                        if i == 3:
                            dx = shifts[0]
                        elif i == 5:
                            glyph_width = sum(shifts[:2])
                            glyph_center = parent_glyph.width / 2
                            dx = glyph_width / 2 - glyph_center

                components.append(Component(parent_index, Point(dx, dy)))

        new_glyph = Glyph()
        for item in components:
            new_glyph.components.append(item)

        metrics = parent_glyph.GetMetrics()
        if len(parents) > 4:
            metrics = Point(glyph_width, 0)
        helpers.move_preexisting(child)
        helpers.append_glyph(new_glyph, child, metrics)


def stems(glyphdata):
    ''' Builds rudimentary base glyph and composites in Stems range. '''
    for child, parent in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        if not f.has_key(parent):
            print('\nSource glyph {} is missing!'.format(parent))
            if parent == 'uniE210':
                makers.stem(parent)
        helpers.decompose(parent)

        stem_index = f.FindGlyph(glyphdata[None])
        parent_index = f.FindGlyph(parent)
        parent_glyph = f.glyphs[parent_index]
        new_glyph = Glyph()
        dx, dy = 0, 0
        new_glyph.components.append(Component(stem_index, Point(dx, dy)))
        dx, dy = helpers.configfloat('Stems', 'stem thickness') / 2, SPACE * 2
        if parent == 'uniE263':
            dx -= parent_glyph.width / 2
        new_glyph.components.append(Component(parent_index, Point(dx, dy)))

        stem_glyph = f.glyphs[stem_index]
        metrics = stem_glyph.GetMetrics()
        if child:
            helpers.move_preexisting(child)
            helpers.append_glyph(new_glyph, child, metrics)


def tremolos(glyphdata):
    ''' Builds composites in Tremolos range. '''
    for parent, children in glyphdata.iteritems():
        if not f.has_key(parent):
            print('\nSource glyph {} is missing!'.format(parent))
            continue
        helpers.decompose(parent)

        for child in children:
            if helpers.check_excluded(child) is True:
                continue

            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            bbox = parent_glyph.GetBoundingRect()
            dot_spacing = helpers.configfloat('Tremolos', 'divisi dot spacing')
            num_of_comps = children.index(child) + 2
            # Set up tremoloDivisiDots6 for double two rows of 3 dots.
            if child == 'uniE231':
                num_of_comps += -2

            if parent != 'uniE4A2':
                # Define base y values for initial comps with odd/even number of trem slashes.
                baseline = bbox.height / 2 if num_of_comps % 2 == 0 else 0
                spacing = helpers.configfloat('Tremolos', 'tremolo slash spacing')
                separation = bbox.height + spacing
                glyph_span = separation * num_of_comps / 2
                if parent == 'uniE225':
                    spacing = helpers.configfloat('Tremolos', 'fingered tremolo spacing')
                    separation = bbox.height + spacing
            else:
                baseline = 0
                separation = bbox.height + dot_spacing
                glyph_span = separation * num_of_comps

            # Generate shift values
            shifts = helpers.generate_shifts(baseline, glyph_span, separation)
            new_glyph = Glyph()
            for shift in shifts:
                # Append trem slash comps with + and - shift values to.
                if parent != 'uniE4A2':
                    dx, dy = 0, shift
                    new_glyph.components.append(Component(parent_index, Point(dx, dy)))
                    if shift > 0:
                        new_glyph.components.append(Component(parent_index, Point(dx, -dy)))
                    metrics = parent_glyph.GetMetrics()

                # Append divisi dot components with 2x3 for 'uniE231'.
                else:
                    dx, dy = shift, 0
                    if child != 'uniE231':
                        new_glyph.components.append(Component(parent_index, Point(dx, dy)))
                    else:
                        new_glyph.components.append(Component(parent_index, Point(dx, dy)))
                        dy = dot_spacing + bbox.height
                        new_glyph.components.append(Component(parent_index, Point(dx, dy)))
                    metrics = Point(glyph_span - dot_spacing, 0)

            # Append new glyph to font.
            helpers.move_preexisting(child)
            helpers.append_glyph(new_glyph, child, metrics)


def flags(glyphdata):
    ''' Builds composite glyphs in Flags range. '''
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        components = []

        for i, parent in enumerate(parents):
            if not f.has_key(parent):
                print('\nSource glyph {} is missing!'.format(parent))
            helpers.decompose(parent)

            spacing = helpers.configfloat('Flags', 'internal flag spacing')
            suffix = helpers.configfloat('Set Suffixes', 'straight flags')
            if helpers.configfloat('Include', 'straight flags') is True:
                if parent.endswith(suffix):
                    spacing = helpers.configfloat('Flags', 'straight flag spacing')
            shifts = helpers.generate_shifts(-spacing, spacing * len(parents), spacing)
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            dx, dy = 0, 0
            for n, dy in enumerate(shifts):
                if 'uniE251' in parent or parent == 'uniE241' + '.' + suffix:
                    dy = -dy
                if i == n:
                    components.append(Component(parent_index, Point(dx, dy)))

        new_glyph = Glyph()
        for item in components:
            new_glyph.components.append(item)

        metrics = parent_glyph.GetMetrics()
        helpers.move_preexisting(child)
        helpers.append_glyph(new_glyph, child, metrics)


def indv_notes(glyphdata):
    ''' Builds rudimentary base glyphs and composites in Individual notes range. '''
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        components = []

        for i, parent in enumerate(parents):
            long_stem_length = helpers.configfloat('Stems', 'long stem length')
            if not f.has_key(parent):
                print('\nSource glyph {} is missing!'.format(parent))

                # Draw/append stem according to spec.
                if parent == 'uniE210':
                    makers.stem(parent)
                # Draw/append augmentation dot according to spec.
                if parent == 'uniE1E7':
                    makers.augmentation_dot(parent)
            helpers.decompose(parent)

            # Define parameters for notehead.
            if parent in ('uniE0A0', 'uniE0A1', 'uniE0A2', 'uniE0A3', 'uniE0A4'):
                note_index = f.FindGlyph(parent)
                note_glyph = f.glyphs[note_index]
                metrics = Point(note_glyph.width, 0)
                dx, dy = 0, 0
                components.append(Component(note_index, Point(dx, dy)))

            # Define parameters for stem.
            if parent == 'uniE210':
                note_bbox = note_glyph.GetBoundingRect()
                stem_index = f.FindGlyph('uniE210')
                stem_glyph = f.glyphs[stem_index]
                stem_bbox = stem_glyph.GetBoundingRect()
                dx, dy = note_glyph.width - stem_glyph.width, 0

                # Handle downstem notes.
                if child in ('uniE1D4', 'uniE1D6', 'uniE1D8', 'uniE1DA', 'uniE1DC',
                             'uniE1DE', 'uniE1E0', 'uniE1E2', 'uniE1E4', 'uniE1E6'):
                    dx, dy = stem_glyph.width, -long_stem_length
                components.append(Component(stem_index, Point(dx, dy)))

            # Define parameters for flags.
            if parent in ('uniE240', 'uniE241', 'uniE250', 'uniE242', 'uniE243', 'uniE251'):
                flag_spacing = helpers.configfloat('Flags', 'internal flag spacing')
                flag_index = f.FindGlyph(parent)
                flag_glyph = f.glyphs[flag_index]
                glyph_width = note_glyph.width + flag_glyph.width - stem_glyph.width * 2
                metrics = Point(glyph_width, 0)
                dx, dy = note_glyph.width - stem_glyph.width * 2, long_stem_length - flag_spacing * 2
                shifts = helpers.generate_shifts(dy, dy + flag_spacing * len(parents), flag_spacing)
                for n, dy in enumerate(shifts):
                    if parent in ('uniE241', 'uniE243', 'uniE251'):
                        dx, dy = 0, -dy
                        metrics = Point(note_glyph.width, 0)
                    if i == n:
                        components.append(Component(flag_index, Point(dx, dy)))

        if child:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)
            helpers.move_preexisting(child)
            helpers.append_glyph(new_glyph, child, metrics)


def beamed_notes(glyphdata):
    ''' Builds rudimentary base glyphs and composites in Beamed groups of notes range. '''
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child) is True:
            continue

        components = []

        for i, parent in enumerate(parents):
            if parent:
                if not f.has_key(parent):
                    print('\nSource glyph {} is missing!'.format(parent))
                    # Draw/append stem according to spec.
                    if parent in ('uniE204', 'uniE205'):
                        makers.stem(parent)
                    elif parent == 'uniE1E7':
                        makers.augmentation_dot(parent)
                    elif parent == 'uniE1F7':
                        makers.note_beam(parent)
                    elif parent == 'uniE1FE':
                        makers.tuplet_bracket(parent)
                helpers.decompose(parent)

                # Initialize components at origin and 100% scale.
                parent_index = f.FindGlyph(parent)
                parent_glyph = f.glyphs[parent_index]
                parent_bbox = parent_glyph.GetBoundingRect()
                dx, dy, sx, sy = 0, 0, 1, 1

                # Scale tuplet nums to 72% and move in line
                # with parent bracket and move tall version up.
                long_stem_length = helpers.configfloat('Stems', 'long stem length')
                short_stem_length = helpers.configfloat('Stems', 'short stem length')
                tuplet_height = helpers.configfloat('Beams', 'tuplet height')
                hook_length = helpers.configfloat('Beams', 'tuplet bracket hook length')
                diff = long_stem_length - short_stem_length
                if child in ('uniE1FF', 'uniE202'):
                    bbox_center = parent_bbox.height / 2
                    sx = sy = 0.72
                    dy = tuplet_height + hook_length - (bbox_center * 0.72)

                # Reverse tuplet brackets horizontally.
                elif child in ('uniE200', 'uniE203'):
                    dx, sx, sy = parent_glyph.width, -1, 1
                # Move bracket and number for long stem up according to separation.
                if child in ('uniE201', 'uniE202', 'uniE203'):
                    dy += diff

                # Define parameters for beams.
                if parent == 'uniE1F7':
                    beam_index = f.FindGlyph(parent)
                    beam_glyph = f.glyphs[beam_index]
                    beam_thickness = helpers.configfloat('Beams', 'beam thickness')
                    beam_spacing = helpers.configfloat('Beams', 'beam spacing')
                    separation = beam_thickness + beam_spacing

                    # Set vertical shift for long short stem and different number of beams.
                    if 'uniE205' in parents or child in ('uniE1F8', 'uniE1FA', 'uniE1FB'):
                        if parents.count('uniE1F7') == 1:
                            dy = separation
                        elif parents.count('uniE1F7') == 3:
                            dy = -separation
                    else:
                        if parents.count('uniE1F7') == 2:
                            dy = -separation

                    shifts = helpers.generate_shifts(dy, dy + (separation *
                                                               parents.count('uniE1F7')), separation)
                    for n, dy in enumerate(shifts):
                        if i - 2 == n:
                            components.append(Component(beam_index, Point(dx, dy), Point(sx, sy)))
                elif 'uniE1F7' in parents and 'uniE204' in parents or 'uniE1F7' in parents and \
                        'uniE205' in parents:
                    diff = beam_glyph.width - parent_glyph.width
                    dx = diff
                    components.append(Component(parent_index, Point(dx, dy), Point(sx, sy)))
                else:
                    components.append(Component(parent_index, Point(dx, dy), Point(sx, sy)))

        new_glyph = Glyph()
        for item in components:
            new_glyph.components.append(item)
        helpers.move_preexisting(child)
        metrics = parent_glyph.GetMetrics()
        if 'uniE883' in parents:
            metrics = Point(parent_bbox.width * 0.72, 0)
        helpers.append_glyph(new_glyph, child, metrics)


def accordion_reg(glyphdata):
    '''Builds registration composite glyphs in Accordion range.'''
    # for parent_data, child_data in glyphdata:
    for parent, value in glyphdata[0].iteritems():

        if not f.has_key(parent):
            print('\nSource glyph {} is missing!'.format(parent))
            if parent == 'uniE8CA':
                makers.coupler_dot(parent)
            else:
                makers.accordion_rank(parent)
        helpers.decompose(parent)

    for child, values in glyphdata[1].iteritems():
        if helpers.check_excluded(child) is True:
            continue

        components = []
        parent = values[0]
        placement = values[1:]

        for i, value in enumerate(placement):
            # Calculates offsets for dot placement from reference values.
            # Reference values provided in comments.
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            parent_bbox = parent_glyph.GetBoundingRect()

            dot_index = f.FindGlyph('uniE8CA')
            dot_glyph = f.glyphs[dot_index]
            dot_bbox = dot_glyph.GetBoundingRect()

            x, y = parent_bbox.width / 2, parent_bbox.height / 2
            if value == 'stop4':
                y = parent_bbox.height / 1.219  # 'stop4' = top of round ranks 3 (780/640)
            elif value in ('upper8', 'master'):
                x = parent_bbox.width / 1.3  # 'upper8'/'master' = mid right of round ranks 2/3/4 (780/600)
            elif value == 'lower8':
                x = parent_bbox.width / 4.333  # 'lower8' = mid left of round ranks 3 (780/180)
            elif value == 'stop16':
                y = parent_bbox.height / 5.571  # 'stop16' = bottom of round ranks 3 (780/140)
            elif value == 'soprano':
                y = parent_bbox.height / 1.1624  # 'soprano' = top of ranks 4 (780/671)
            elif value == 'alto':
                y = parent_bbox.height / 1.612  # 'alto' = upper mid of ranks 4 (780/484)
            elif value == 'tenor':
                y = parent_bbox.height / 2.635  # 'tenor' = lower mid of ranks 4 (780/296)
            elif value == 'bass':
                y = parent_bbox.height / 7.156  # 'bass' = bottom of ranks 4 (780/109)
            elif value == 'stop8b':
                y = parent_bbox.height / 1.352  # 'stop8b' = top of ranks 2 (780/577)
            elif value == 'stop16b':
                y = parent_bbox.height / 3.842  # 'stop16b' = bottom of ranks 2 (780/203)
            elif value in ('stop8c', 'left8stop', 'right8stop'):
                y = parent_bbox.height / 5.555  # 'stop8c' = bottom of square ranks 3 (750/135)
            elif value == 'stop2':
                y = parent_bbox.height / 1.22  # 'stop2' = top of square ranks 3 (750/615)
            elif value == 'left8stop':
                x = parent_bbox.width / 3.079  # 'left8stop' = bottom left half of square ranks 3 (625/203)
            # (x = parent_bbox.width / 3 with 3% compensation <--> for 'left8stop' and 'right8stop')
            elif value == 'right8stop':
                x = parent_bbox.width / 1.481  # 'right8stop' = bottom right half of square ranks 3 (625/422)

            # Adjust to dot center base and overshoot of round ranks glyphs.
            x -= dot_bbox.width / 2
            y -= dot_bbox.height / 2
            if parent != 'uniE8C9':
                y += helpers.configfloat('Accordion', 'round ranks overshoot')

            components.append(Component(dot_index, Point(x, y)))
            if i == 0:
                components.append(Component(parent_index, Point(0, 0)))

        new_glyph = Glyph()
        for item in components:
            new_glyph.components.append(item)

        metrics = parent_glyph.GetMetrics()
        if child:
            helpers.move_preexisting(child)
            helpers.append_glyph(new_glyph, child, metrics)

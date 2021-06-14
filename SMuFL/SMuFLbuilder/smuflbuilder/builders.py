"""Builder module for SMuFLbuilder.

This module contains all main functionality to build composites from glyph
components. Each function is as well the hub to all other functionality
involved in drawing and appending glyphs to font.

The functions herein are grouped by SMuFL range or glyph type, depending on
practicality. Getting their external functionality from modules .makers and
.helpers and user defined values from config, they all follow more or less
the same process:

1. Check .data in argument against font for missing parents.
2. Call applicable function in .makers if not.
3. Define component delta shift and scale.
4. Define composite metrics.
5. Build composites from components.
6. Append glyphs to font.

Most horizontal placement and spacing presently rely on Glyph().width rather
than bounding boxes. This is more straightforward, but may not be ideal in all
cases.

Functions:

staves() -- builds composites of stafflines
barlines() -- builds barline and repeat barline composites
cut_time() -- builds time signature cut time symbols
fraction_time() -- builds time signature fraction composites
mirror_time() -- builds reversed and turned time signature glyphs
time_ligatures() -- builds time signature ligatures
indv_notes() -- builds individual notes composites
beamed_notes() -- builds beamed notes composites
stems() -- builds stem composites
tremolos() -- builds tremolo and division dot composites
flags() -- builds flag composites
octaves() -- builds octave composites
dynamics() -- builds dynamics composites
accordion_reg() -- builds accordion registration composites
"""

# (c) 2021 by Knut Nergaard.


from ConfigParser import SafeConfigParser
from FL import *

from smuflbuilder import data
from smuflbuilder import helpers
from smuflbuilder import makers
from smuflbuilder import filepaths

f = fl.font
config = SafeConfigParser()
config.read(filepaths.defaults)
config.read(filepaths.user)

SPACE = f.upm / 4


def staves(glyphdata):
    """builds composites in Staves range.

    Determines baseline from number of components required.
    """
    for parent, children in glyphdata.iteritems():
        complete = helpers.check_complete(parent)
        if not complete and config.getboolean('Global', 'draw missing'):
            makers.staves(parent, children)
            complete = True
        helpers.decompose(parent)

        if not children:
            continue
        for child in children:
            if helpers.check_excluded(child) or not complete:
                helpers.print_incomplete(child)
                continue

            # Determine base y values for initial components
            # in glyphs with odd vs. even number of lines.
            num_of_lines = children.index(child) + 2
            baseline = SPACE / 2 if num_of_lines % 2 == 0 else 0
            glyph_height = SPACE * num_of_lines / 2

            # Generate shift values for subsequent components.
            shifts = range(baseline, glyph_height, SPACE)
            new_glyph = Glyph()
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]

            # Append components with + and - shift values to new glyph.
            dx, dy = 0, 0
            for dy in shifts:
                new_glyph.components.append(Component(
                    parent_index, Point(dx, dy)))
                if dy > 0:
                    new_glyph.components.append(Component(
                        parent_index, Point(dx, -dy)))

            metrics = parent_glyph.GetMetrics()
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def barlines(glyphdata):
    """builds composites in Barlines and Repeats ranges.

    Special spacing parameters are required to build composites involving
    repeat dots."""
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        bbox_widths = []
        separations = []
        components = []

        for i, parent in enumerate(parents):
            complete = helpers.check_complete(parent)
            if not complete:
                if not config.getboolean('Global', 'draw missing'):
                    helpers.print_incomplete(child)
                    break
                makers.barlines(parent)
                complete = True

            # Get bounding boxes.
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            bbox_width = parent_glyph.GetBoundingRect().width
            bbox_widths.append(bbox_width)

            # Set separation parameters.
            separation = helpers.configvalue('Barlines', 'barline separation')
            if parents[i] == 'uniE044' or parents[i - 1] == 'uniE044':
                separation = helpers.configvalue(
                    'Repeats', 'repeat barline dot separation')

            if parent == 'uniE044':
                if i in {1, 3, 6} or i == len(parents) - 1:
                    separation = -bbox_width

            if i == 0:
                separation = 0
            separations.append(separation)

            # Set shifts for repeat dots.
            dx, dy = sum(bbox_widths[:-1] + separations), 0
            if parent == 'uniE044':
                dy = SPACE * 1.5 if i % 2 == 1 else SPACE * 2.5

            # Append components.
            components.append(Component(parent_index, Point(dx, dy)))

            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)

        if child and complete:
            new_width = sum(bbox_widths + separations)
            metrics = Point(new_width, 0)
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def cut_time(glyphdata):
    """Builds cut time composites in Time signature related ranges.

    Covers both Time signature and Time signatures supplement ranges.
    Requires unencoded timeSigVerticalStroke component.
    """
    for parent, child in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        stroke = helpers.configvalue(
            'Time Signatures', 'cut time stroke')
        l_suffix = helpers.configvalue(
            'Set Suffixes', 'large time signatures')
        n_suffix = helpers.configvalue(
            'Set Suffixes', 'large narrow time signatures')
        if parent.endswith(l_suffix):
            stroke += l_suffix
        elif parent.endswith(n_suffix):
            stroke += n_suffix

        complete = helpers.check_complete(parent)
        if complete:
            complete = helpers.check_complete(stroke)

        if not complete:
            helpers.print_incomplete(child)
        else:
            new_glyph = Glyph()
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            dx, dy = 0, 0
            new_glyph.components.append(Component(parent_index, Point(dx, dy)))

            # Get index of cut time stroke glyph,
            # and center in main parent glyph.
            stroke_index = f.FindGlyph(stroke)
            parent_width = parent_glyph.GetBoundingRect().width
            parent_center = parent_width / 2
            dx, dy = parent_center, 0
            new_glyph.components.append(Component(
                stroke_index, Point(dx, dy)))

            metrics = parent_glyph.GetMetrics()
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def fraction_time(glyphdata):
    """Builds Time signature fraction composites.

    Scales regular numerals to 50%.
    Fraction slash is kept at 100%, according to Bravura scaling factor.
    Option to build from dedicated numerals should perhaps be implemented.
    """
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        parent_widths = []

        new_glyph = Glyph()
        for i, parent in enumerate(parents):
            complete = helpers.check_complete(parent)
            if not complete:
                break
            helpers.decompose(parent)

            # Define scale, shift, spacing and
            # kerning for fraction glyphs acc. to spec.
            sidebearings = helpers.configvalue(
                'Time Signatures', 'fraction sidebearings')
            spacing = helpers.configvalue(
                'Time Signatures', 'fraction spacing')
            one_kern = helpers.configvalue(
                'Time Signatures', 'fraction one kern')
            four_kern = helpers.configvalue(
                'Time Signatures', 'fraction four kern')
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            parent_width = parent_glyph.width
            sx = sy = 1  # 1 = 100% (x, y)
            dx = dy = 0
            num_factor = 0.5
            # num_factor reflects current scaling factor
            # of slash vs. numerals in Bravura.
            if i == 1:
                dx = parent_widths[i - 1] - parent_width / 2 + spacing
            else:
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

            parent_widths.append(parent_width)
            new_glyph.components.append(Component(
                parent_index, Point(dx, dy), Point(sx, sy)))
        if not complete:
            helpers.print_incomplete(child)
        else:
            new_width = parent_widths[0] + parent_widths[2] + spacing * 2
            metrics = Point(new_width, 0)
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def mirror_time(glyphdata):
    """Builds composites in Turned and Reversed time signatures ranges.

    Requires unencoded timeSigVerticalStroke component to retain cutTimeCommon
    as composite.
    """
    for parent, child in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        stroke = helpers.configvalue('Time Signatures', 'cut time stroke')
        complete = helpers.check_complete(parent)
        if complete and parent == 'uniE08B':
            complete = helpers.check_complete(stroke)
        helpers.decompose(parent)

        if not complete:
            helpers.print_incomplete(child)
        else:
            new_glyph = Glyph()
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            # Turn.
            dx, dy, sx, sy = parent_glyph.width, parent_glyph.height, -1, -1
            if glyphdata == data.reversed_time:
                # Reverse.
                dx, dy, sx, sy = parent_glyph.width, 0, -1, 1
            new_glyph.components.append(Component(
                parent_index, Point(dx, dy), Point(sx, sy)))

            # Append component if cut time is component.
            if parent == 'uniE08B' and parent_glyph.components:
                stroke_index = f.FindGlyph(stroke)
                stroke_glyph = f.glyphs[stroke_index]

                for c in parent_glyph.components:
                    if c.index == stroke_index:
                        dx = (parent_glyph.width + stroke_glyph.width) * 0.5
                    new_glyph.components.append(Component(
                        c.index, Point(dx, dy), Point(sx, sy)))

            metrics = parent_glyph.GetMetrics()
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def time_ligatures(glyphdata):
    """Builds recommended ligatures in Time Signatures range.

    Target name and numerator/denominator is determined by ligature name
    (underscore and ctrl character).
    """
    for child in glyphdata:
        if helpers.check_excluded(child):
            continue

        components = []
        shifts = []

        parents = child.split('_')
        complete = True
        for i, parent in enumerate(parents):
            complete = helpers.check_complete(parent)
            if not complete:
                break
            helpers.decompose(parent)

            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            dx, dy = 0, 0
            if parent in data.ctrl_char:
                continue
            # Set vertical shift values for denominator and numerator.
            dy = SPACE if parents[i - 1] == 'uniE09F' else SPACE * 3
            if len(parents) <= 4:
                continue
            # Set horizontal shifts and spacing for ligatures
            # with double digit numerator.
            shifts.append(parent_glyph.width)
            if i == 3:
                dx = shifts[0]
            elif i == 5:
                glyph_width = sum(shifts[:2])
                glyph_center = parent_glyph.width / 2
                dx = glyph_width / 2 - glyph_center

                components.append(Component(parent_index, Point(dx, dy)))

        if not complete:
            helpers.print_incomplete(child)
        else:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)

            metrics = parent_glyph.GetMetrics()
            if len(parents) > 4:
                metrics = Point(glyph_width, 0)
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def indv_notes(glyphdata):
    """Builds composites in Individual notes range.

    Duplicates functionality of flags() which is not ideal, but difficult to
    avoid when parameters are different.
    """
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        components = []

        complete = True
        for i, parent in enumerate(parents):
            long_stem_length = helpers.configvalue('Stems', 'long stem length')
            complete = helpers.check_complete(parent)
            if not complete:
                if not config.getboolean('Global', 'draw missing'):
                    break
                if parent not in {'uniE210', 'uniE1E7'}:
                    continue
                # Draw/append stem according to spec.
                elif parent == 'uniE210':
                    makers.stems(parent)
                # Draw/append augmentation dot according to spec.
                else:
                    makers.augmentation_dot(parent)
                complete = True

            if not complete:
                continue
            helpers.decompose(parent)

            # Define parameters for notehead and append to list.
            if parent in {'uniE0A0', 'uniE0A1', 'uniE0A2', 'uniE0A3', 'uniE0A4'}:
                note_index = f.FindGlyph(parent)
                note_glyph = f.glyphs[note_index]
                metrics = Point(note_glyph.width, 0)
                dx, dy = 0, 0
                components.append(Component(note_index, Point(dx, dy)))

            # Define parameters for stem.
            elif parent == 'uniE210':
                note_bbox = note_glyph.GetBoundingRect()
                stem_index = f.FindGlyph('uniE210')
                stem_glyph = f.glyphs[stem_index]
                stem_bbox = stem_glyph.GetBoundingRect()
                dx, dy = note_glyph.width - stem_glyph.width, 0

                # Handle downstem notes and append to list.
                if child in {'uniE1D4', 'uniE1D6', 'uniE1D8', 'uniE1DA', 'uniE1DC',
                             'uniE1DE', 'uniE1E0', 'uniE1E2', 'uniE1E4', 'uniE1E6'}:
                    dx, dy = stem_glyph.width, -long_stem_length
                components.append(Component(stem_index, Point(dx, dy)))

            # Define parameters for flags.
            elif parent in {'uniE240', 'uniE241', 'uniE250',
                            'uniE242', 'uniE243', 'uniE251'}:
                flag_spacing = helpers.configvalue(
                    'Flags', 'internal flag spacing')
                flag_index = f.FindGlyph(parent)
                flag_glyph = f.glyphs[flag_index]
                glyph_width = (note_glyph.width + flag_glyph.width -
                               stem_glyph.width * 2)
                metrics = Point(glyph_width, 0)
                dx, dy = (note_glyph.width - stem_glyph.width * 2,
                          long_stem_length - flag_spacing * 2)
                shifts = range(dy, dy + flag_spacing * len(parents), flag_spacing)

                # Generate vertical shifts and append to list.
                for n, dy in enumerate(shifts):
                    if parent in {'uniE241', 'uniE243', 'uniE251'}:
                        dx, dy = 0, -dy
                        metrics = Point(note_glyph.width, 0)
                    if i == n:
                        components.append(Component(flag_index, Point(dx, dy)))

        if not complete:
            helpers.print_incomplete(child)
        elif child:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def beamed_notes(glyphdata):
    """Builds composites in Beamed groups of notes range.

    Scales number in Tuplets range to 70%.
    Mirrors tuplet bracket.
    """
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        components = []

        complete = True
        for i, parent in enumerate(parents):
            if not parent:
                continue
            complete = helpers.check_complete(parent)
            if not complete:
                if not config.getboolean('Global', 'draw missing'):
                    break
                elif parent in {'uniE204', 'uniE205', 'uniE1E7', 'uniE1F7', 'uniE1FE'}:
                    # Draw/append stem according to spec.
                    if parent in {'uniE204', 'uniE205'}:
                        makers.stems(parent)
                    elif parent == 'uniE1E7':
                        makers.augmentation_dot(parent)
                    elif parent == 'uniE1F7':
                        makers.note_beam(parent)
                    elif parent == 'uniE1FE':
                        makers.tuplet_bracket(parent)
                    complete = True

            if not complete:
                continue
            helpers.decompose(parent)
            # Initialize components at origin and 100% scale.
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            parent_bbox = parent_glyph.GetBoundingRect()
            dx, dy, sx, sy = 0, 0, 1, 1

            # Scale tuplet nums to 72% and move in line
            # with parent bracket and move tall version up.
            long_stem_length = helpers.configvalue('Stems', 'long stem length')
            short_stem_length = helpers.configvalue('Stems', 'short stem length')
            tuplet_height = helpers.configvalue('Beams', 'tuplet height')
            hook_length = helpers.configvalue('Beams', 'tuplet bracket hook length')
            diff = long_stem_length - short_stem_length
            if child in {'uniE1FF', 'uniE202'}:
                bbox_center = parent_bbox.height / 2
                sx = sy = 0.72
                dy = tuplet_height + hook_length - (bbox_center * 0.72)

            # Reverse tuplet brackets horizontally.
            elif child in {'uniE200', 'uniE203'}:
                dx, sx, sy = parent_glyph.width, -1, 1

            # Move bracket and number for long stem
            # up according to separation.
            if child in {'uniE201', 'uniE202', 'uniE203'}:
                dy += diff

            # Define parameters for beams.
            if parent == 'uniE1F7':
                beam_index = f.FindGlyph(parent)
                beam_glyph = f.glyphs[beam_index]
                beam_thickness = helpers.configvalue('Beams', 'beam thickness')
                beam_spacing = helpers.configvalue('Beams', 'beam spacing')
                separation = beam_thickness + beam_spacing

                # Set vertical shift for long short stem
                # and different number of beams.
                if 'uniE205' in parents or child in {'uniE1F8', 'uniE1FA', 'uniE1FB'}:
                    if parents.count('uniE1F7') == 1:
                        dy = separation
                    elif parents.count('uniE1F7') == 3:
                        dy = -separation
                elif parents.count('uniE1F7') == 2:
                    dy = -separation

                # Generate shifts and append to list.
                number_of_beams = parents.count('uniE1F7')
                shifts = range(dy, dy + separation * number_of_beams, separation)
                for n, dy in enumerate(shifts):
                    if i - 2 == n:
                        components.append(Component(beam_index, Point(dx, dy)))

            # Define parameters for beamed notes and append to list.
            elif ('uniE1F7' in parents and 'uniE204' in parents or
                  'uniE1F7' in parents and 'uniE205' in parents):
                diff = beam_glyph.width - parent_glyph.width
                dx = diff
                components.append(Component(parent_index, Point(dx, dy)))

            # Append the rest.
            else:
                components.append(Component(parent_index,
                                            Point(dx, dy), Point(sx, sy)))

        if not complete:
            helpers.print_incomplete(child)
        else:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)
            helpers.handle_replaced(child)
            metrics = parent_glyph.GetMetrics()
            if 'uniE883' in parents:
                metrics = Point(parent_bbox.width * 0.72, 0)
            helpers.append_glyph(new_glyph, child, metrics)


def stems(glyphdata):
    """Builds composites in Stems range.

    Dedicated technique components are found in Tremolos and various
    instrument-specific ranges.
    """
    for child, parent in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        complete = helpers.check_complete(parent)
        if not complete:
            if (config.getboolean('Global', 'draw missing')
                    and parent == 'uniE210'):
                makers.stems(parent)
                complete = True
            elif child:
                helpers.print_incomplete(child)
            else:
                helpers.print_incomplete(parent)
            break
        else:
            helpers.decompose(parent)
            stem_index = f.FindGlyph(glyphdata[None])
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            new_glyph = Glyph()
            dx, dy = 0, 0
            # append stem component.
            new_glyph.components.append(Component(stem_index, Point(dx, dy)))

            # Set parameters for symbols and append.
            dx = helpers.configvalue('Stems', 'stem thickness') / 2
            dy = SPACE * 2
            # Centre double sharp on left sidebearing.
            if parent == 'uniE263':
                dx -= parent_glyph.width / 2
            new_glyph.components.append(Component(parent_index, Point(dx, dy)))

            stem_glyph = f.glyphs[stem_index]
            metrics = stem_glyph.GetMetrics()
            if child:
                helpers.handle_replaced(child)
                helpers.append_glyph(new_glyph, child, metrics)


def tremolos(glyphdata):
    """Builds slash and separation dot composites in Tremolos range.

    Determines baseline of slash composites based on number of components
    required, and builds from there.
    Special spcing parameters are used for tremoloDivisiDots6 to split dots
    into to two rows of three.

    Drawing of parents is not yet implemented in [makers].
    """
    for parent, children in glyphdata.iteritems():
        complete = helpers.check_complete(parent)
        helpers.decompose(parent)
        if not children:
            continue

        for child in children:
            if helpers.check_excluded(child):
                continue

            if not complete:
                helpers.print_incomplete(child)
                continue

            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            bbox = parent_glyph.GetBoundingRect()
            dot_spacing = helpers.configvalue('Tremolos', 'divisi dot spacing')
            num_of_comps = children.index(child) + 2

            # Define base values for divisi dots.
            if parent == 'uniE4A2':
                baseline = 0
                separation = bbox.height + dot_spacing
                glyph_span = separation * num_of_comps
                # Set up tremoloDivisiDots6 for double two rows of 3 dots.
                if child == 'uniE231':
                    num_of_comps += -2

            # Define base y values for initial comps with
            # odd/even number of trem slashes.
            else:
                baseline = bbox.height / 2 if num_of_comps % 2 == 0 else 0
                spacing = helpers.configvalue('Tremolos',
                                              'tremolo slash spacing')
                separation = bbox.height + spacing
                glyph_span = separation * num_of_comps / 2

                if parent == 'uniE225':
                    spacing = helpers.configvalue('Tremolos',
                                                  'fingered tremolo spacing')
                    separation = bbox.height + spacing

            shifts = range(baseline, glyph_span, separation)
            new_glyph = Glyph()
            for shift in shifts:

                # Append trem slash comps with + and - shift values.
                if parent != 'uniE4A2':
                    dx, dy = 0, shift
                    new_glyph.components.append(Component(parent_index,
                                                          Point(dx, dy)))
                    if shift > 0:
                        new_glyph.components.append(Component(parent_index,
                                                              Point(dx, -dy)))
                    metrics = parent_glyph.GetMetrics()

                # Append divisi dot components with 2x3 for 'uniE231'.
                else:
                    dx, dy = shift, 0
                    if child != 'uniE231':
                        new_glyph.components.append(Component(parent_index,
                                                              Point(dx, dy)))
                    else:
                        new_glyph.components.append(Component(parent_index,
                                                              Point(dx, dy)))
                        dy = dot_spacing + bbox.height
                        new_glyph.components.append(Component(parent_index,
                                                              Point(dx, dy)))
                    metrics = Point(glyph_span - dot_spacing, 0)

            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def flags(glyphdata):
    """Builds composite glyphs in Flags range.

    Additionally builds straight flags, as well as short flag and small flags
    (for small staff) stylistic sets.
    """
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        components = []

        complete = True
        for i, parent in enumerate(parents):
            complete = helpers.check_complete(parent)
            if not complete:
                continue
            helpers.decompose(parent)

            spacing = helpers.configvalue('Flags', 'internal flag spacing')
            suffix = helpers.configvalue('Set Suffixes', 'straight flags')
            if helpers.configvalue('Include', 'straight flags'):
                if parent.endswith(suffix):
                    spacing = helpers.configvalue('Flags', 'straight flag spacing')
            shifts = range(-spacing, spacing * len(parents), spacing)
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            dx, dy = 0, 0
            for n, dy in enumerate(shifts):
                if 'uniE251' in parent or parent == 'uniE241' + '.' + suffix:
                    dy = -dy
                if i == n:
                    components.append(Component(parent_index, Point(dx, dy)))

        if not complete:
            helpers.print_incomplete(child)
        else:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)
            metrics = parent_glyph.GetMetrics()
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def octaves(glyphdata):
    """Builds composite glyphs in Octaves and Octaves supplement ranges.

    Requires additional (unencoded) letters to build 'loco' and 'bassa' glyphs.
    """
    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        complete = True
        parent_widths = []
        components = []

        for i, parent in enumerate(parents):
            # Define names of unencoded letters according to spec.
            if parent == 'octaveC':
                parent = helpers.configvalue('Octaves', 'c')
            elif parent == 'octaveL':
                parent = helpers.configvalue('Octaves', 'l')
            elif parent == 'octaveO':
                parent = helpers.configvalue('Octaves', 'o')
            elif parent == 'octaveS':
                parent = helpers.configvalue('Octaves', 's')

            complete = helpers.check_complete(parent)
            if not complete:
                break
            helpers.decompose(parent)

            # Define shift, spacing and kerning for fraction glyphs acc. to spec.
            spacing = helpers.configvalue('Octaves', 'component spacing')
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]

            # Define horizontal shifts.
            dx = dy = 0
            parent_widths.append(parent_glyph.width + spacing)
            dx = sum(parent_widths[:-1])
            new_width = sum(parent_widths)

            # Define vertical shift for superscript.
            number_bbox = helpers.get_bbox('uniE510')
            letter_bbox = helpers.get_bbox('uniEC91')
            super_height = (number_bbox.ur.y - letter_bbox.ur.y +
                            number_bbox.ll.y + helpers.configvalue(
                                'Octaves', 'superscript height adjustment'))
            super_kern = helpers.configvalue('Octaves', 'superscript kern')

            if child in {'uniE511', 'uniE515', 'uniE518', 'uniEC92',
                         'uniEC94', 'uniEC96', 'uniEC98'}:
                if parent in {'uniEC91', 'uniEC93', 'uniEC95', 'uniEC97'}:
                    dx += super_kern
                    dy = super_height
                    new_width += super_kern

            components.append(Component(parent_index, Point(dx, dy)))

        if complete:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)

            metrics = Point(new_width, 0)
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)
        else:
            helpers.print_incomplete(child)


def dynamics(glyphdata):
    """Builds composites in Dynamics range.

    Uses sidebearings and any kerning pairs to space components.
    A global spacing setting for entire range is also available in config.
    """

    for child, parents in glyphdata.iteritems():
        if helpers.check_excluded(child):
            continue

        complete = True
        parent_widths = []
        components = []

        for i, parent in enumerate(parents):
            complete = helpers.check_complete(parent)
            if not complete:
                if not config.getboolean('Global', 'draw missing'):
                    helpers.print_incomplete(parent)
                    break
                elif parent in {'uniE53E', 'uniE541'}:
                    makers.dynamics(parent)
                    complete = True
                else:
                    helpers.print_incomplete(child)
                    break

            helpers.decompose(parent)
            parent_index = f.FindGlyph(parent)
            parent_glyph = f.glyphs[parent_index]
            width = parent_glyph.width
            dx = dy = 0

            # Define shifts for letters based on width, spacing and kerning.
            if 'uniE53E' not in parents:
                spacing = helpers.configvalue('Dynamics', 'component spacing')
                left = parents[i - 1]
                right = parents[i]
                # Exclude kerning for leftmost component
                kerning = 0 if i == 0 else helpers.get_kerning(left, right)
                parent_widths.append(width + spacing + kerning)

                dx = sum(parent_widths[:-1]) + kerning
                # Exclude spacing for rightmost component
                width = sum(parent_widths) - spacing
                components.append(Component(parent_index, Point(dx, dy)))

            elif child == 'uniE53F':
                dx, sx, sy = width, -1, 1
                components.append(Component(parent_index, Point(dx, dy),
                                            Point(sx, sy)))
            elif i == 0:
                components.append(Component(parent_index, Point(dx, dy)))
            else:
                spacing = helpers.configvalue('Dynamics', 'hairpin spacing')
                width = width * 2 + spacing
                dx, sx, sy = width, -1, 1
                components.append(Component(parent_index, Point(dx, dy),
                                            Point(sx, sy)))

        if child and complete:
            new_glyph = Glyph()
            for item in components:
                new_glyph.components.append(item)
            metrics = Point(width, 0)
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)


def accordion_reg(glyphdata):
    """Builds registration composites in Accordion range.

    Placement schemes are defined by 'codes' derived from descriptions in
    SMuFL documentation. Reference values are given in comments below.
    """

    # for parent_data, child_data in glyphdata:
    for parent, value in glyphdata[0].iteritems():
        complete = helpers.check_complete(parent)
        if not complete:
            if not config.getboolean('Global', 'draw missing'):
                continue
            if parent == 'uniE8CA':
                makers.coupler_dot(parent)
            else:
                makers.ranks(parent)
            complete = True
        helpers.decompose(parent)

    for child, values in glyphdata[1].iteritems():
        if helpers.check_excluded(child):
            continue

        components = []
        parent = values[0]
        placement = values[1:]

        if not complete:
            helpers.print_incomplete(child)
            continue

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
                y = parent_bbox.height / 1.219
                # 'stop4' = top of round ranks 3 (780/640)
            elif value in {'upper8', 'master'}:
                x = parent_bbox.width / 1.3
                # 'upper8'/'master' = mid right of round ranks 2/3/4 (780/600)
            elif value == 'lower8':
                x = parent_bbox.width / 4.333
                # 'lower8' = mid left of round ranks 3 (780/180)
            elif value == 'stop16':
                y = parent_bbox.height / 5.571
                # 'stop16' = bottom of round ranks 3 (780/140)
            elif value == 'soprano':
                y = parent_bbox.height / 1.1624
                # 'soprano' = top of ranks 4 (780/671)
            elif value == 'alto':
                y = parent_bbox.height / 1.612
                # 'alto' = upper mid of ranks 4 (780/484)
            elif value == 'tenor':
                y = parent_bbox.height / 2.635
                # 'tenor' = lower mid of ranks 4 (780/296)
            elif value == 'bass':
                y = parent_bbox.height / 7.156
                # 'bass' = bottom of ranks 4 (780/109)
            elif value == 'stop8b':
                y = parent_bbox.height / 1.352
                # 'stop8b' = top of ranks 2 (780/577)
            elif value == 'stop16b':
                y = parent_bbox.height / 3.842
                # 'stop16b' = bottom of ranks 2 (780/203)
            elif value in {'stop8c', 'left8stop', 'right8stop'}:
                y = parent_bbox.height / 5.555
                # 'stop8c' = bottom of square ranks 3 (750/135)
            elif value == 'stop2':
                y = parent_bbox.height / 1.22
                # 'stop2' = top of square ranks 3 (750/615)
            elif value == 'left8stop':
                x = parent_bbox.width / 3.079
                # 'left8stop' = bottom left half of square ranks 3 (625/203)
                # (x = parent_bbox.width / 3 with 3% compensation <--> for
                # 'left8stop' and 'right8stop')
            elif value == 'right8stop':
                x = parent_bbox.width / 1.481
                # 'right8stop' = bottom right half of square ranks 3 (625/422)

            # Adjust to dot center base and overshoot of round ranks glyphs.
            x -= dot_bbox.width / 2
            y -= dot_bbox.height / 2
            if parent != 'uniE8C9':
                y += helpers.configvalue('Accordion', 'round ranks overshoot')

            components.append(Component(dot_index, Point(x, y)))
            if i == 0:
                components.append(Component(parent_index, Point(0, 0)))

        new_glyph = Glyph()
        for item in components:
            new_glyph.components.append(item)

        metrics = parent_glyph.GetMetrics()
        if child:
            helpers.handle_replaced(child)
            helpers.append_glyph(new_glyph, child, metrics)

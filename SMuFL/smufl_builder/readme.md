# SMuFLbuilder

SMuFLbuilder is a Python script for FontLab Studio 5 that lets you build
composite glyphs across selected ranges in SMuFL fonts, based on created
components. For glyphs involving primitives (like barlines, staves, stems,
etc.), SMuFLbuilder will even draw the parent glyphs for you, based on your
own specifications.

Considering the many component-based symbols used in music notation generally,
and the numerous – partially or fully – visually identical glyphs found
in the SMuFL standard, makes SMuFLbuilder a real timesaver for any creator of
SMuFL fonts.

## Table of contents

[License](#license)<br>
[Supported ranges](#supported-ranges)<br>
[Installation](#installation)<br>
[Running the script](#running-the-script)<br>
[Settings](#settings)<br>
[Required and created glyphs](#required-and-created-glyphs)<br>

## License
SMuFLbuilder is written and maintained by Knut Nergaard, and is available under the
**[MITLicense](https://github.com/knutnergaard/FontLab-Scripts/tree/main/SMuFL/SMuFLbuilder/Lisence.txt)**.<br/>

## Supported ranges
The current beta (0.2) supports the following ranges, including recommended
alternates and ligatures where applicable:

- [Staves (U+E010-U+E02F)](#staves-ue010-ue02f)
- [Barlines (U+E030-U+E03F)](#barlines-ue030-ue03f)
- [Repeats (U+E040-U+E04F)](#repeats-ue040-ue04f)
- [Time signatures (U+E080-U+E09F)](#time-signatures-ue080-ue09f)
- [Individual notes (U+E1D0-U+E1EF)](#individual-notes-ue1d0-ue1ef)
- [Beamed groups of notes (U+E1F0-U+E20F)](#beamed-groups-of-notes-ue1f0-ue20f)
- [Stems (U+E210-U+E21F)](#stems-ue210-ue21f)
- [Tremolos (U+E220-U+E23F)](#tremolos-ue220-ue23f)
- [Flags (U+E240-U+E25F)](#flags-ue240-ue25f)
- [Octaves (U+E510-U+E51F)](#octaves-ue510-ue51f)
- [Dynamics (U+E520-U+E54F)](#dynamics-ue520-ue54f)
- [Accordion (U+E8A0-U+E8DF)](#accordion-ue8a0-ue8df)
- [Time signatures supplement (U+EC80-U+EC8F)](#time-signatures-supplement-uec80-uec8f)
- [Octaves supplement (U+EC90-U+EC9F)](#octaves-supplement-uec90-uec9f)
- [Turned time signatures (U+ECE0-U+ECEF)](#turned-time-signatures-uece0-uecef)
- [Reversed time signatures (U+ECF0-U+ECF](#reversed-time-signatures-uecf0-uecf)

## Installation
### Automatically
On Mac, SMuFLbuilder can be installed automatically running the enclosed bash
script in Terminal. Simply drag and drop the file `install.sh` into the
Terminal window, press enter and follow any prompts.

Please be advised that this software is in the early beta stages, and that
you use this method **at your own risk!**

### Manually
#####On Mac:
1. Move the folder `SMuFL` to `~/Library/Application Support/FontLab/Studio 5/Macros`.
2. Move the module folder named `smuflbuilder` to `~/Library/Application Support/FontLab/Studio 5/Macros/System/Modules`.
3. Move the folder named `SMuFLbuilder Settings` anywhere you like on your system,
and rename the file if you wish. (When running the installer, this folder is
moved to ~/Documents).
4. Procede to [Reset path](#reset-path) below or enter your settings filepath
manually by opening `filepaths.py` in the smuflbuilder module folder
and entering your chosen path (including the filename) in between the empty
quote marks of `user = ''`.

#####On Windows:
The installation process on Windows is exactly the same as above, except that
the filepaths will be different. You will also need to change the path for
the default settings manually in filepaths.py to reflect the Windows syntax.
Please refer to the FontLab manual for the correct locations of Python macros
and modules on Windows.

### Reset path
The folder `SMuFLbuilder Settings` (installed in your Documents folder by
default) contains your user settings file, `smuflbuilder.ini`, as well as an
additional bash script, `reset_path.sh`, which will establish a
new path or filename if you ever would want to move or rename the file.

Effectively, this script allows you to maintain multiple versions of
SMuFLbuilder settings relatively easily by simple drag and drop into your Terminal
window whenever you want to switch to a new file. It's only required that you
run the script from inside the directory where your single new version of
`smuflbuilder.ini` lives.

## Running the script
SMuFLbuilder is most simply run from the Macros panel in FontLab Studio.
Assuming **Python 2.7** is correctly installed on your system:

1. Select Wiew > Toolbars > Macro in the application menu to show the Macro Toolbar.
2. Choose `SMuFL` in the Top level dropdown and then `SMuFLbuilder` in the dropdown to the right.
3. Press the triangular 'play' button to run the script.

Refer to the chapter *Macro Programming* in the FontLab Studio Manual for more detailed instructions.

## Settings
All user-specific options and settings for SMuFLbuilder are defined in
`smuflbuilder.ini`, which can be altered in any basic text editor.
Default settings are defined in a separate file named `defaults.ini`,
located in `~/Library/Application Support/FontLab/Studio 5/Macros/System/Modules/smuflbuilder`.

`smuflbuilder.ini` must contain all available sections (enclosed in square brackets),
but options may be 'commented out' (by preceding them with a semicolon) or deleted as needed,
in which case, SMuFLbuilder will fall back on the default value.

Generally, the dimensional settings below are only relevant if you
want any glyphs to be drawn for you. Otherwise, SMuFLbuilder will base such
calculations on bounding boxes or advance widths.

A summary of each section and available options are provided under the following paragraphs:

[[Include]](#include) [[Exclude]](#exclude) [[Global]](#global) [[Accordion]](#accordion) [[Barlines]](#barlines) [[Beams]](#beams)
[[Dynamics]](#dynamics) [[Flags]](#flags) [[Notes]](#notes) [[Octaves]](#octaves)
[[Repeats]](#repeats) [[Staves]](#staves) [[Stems]](#stems)
[[Time&nbsp;Signatures]](#time-signatures) [[Tremolos]](#tremolos) [[Set&nbsp;Suffixes]](#set-suffixes)

##### [Include]
Unsurprisingly, this section is where you choose the ranges and categories to
include in your build. To make changes as expedient as possible, booleans
(true/false values) in this and other sections are set with numbers 1 (true) or 0 (false).

The first paragraph lists all supported ranges according to the SMuFL standard.
In addition, you may choose whether or not to include recommended characters,
alternates, ligatures and specific stylistic sets in your build.

```
[Include]

Staves (U+E010-U+E02F) = 0
Barlines (U+E030-U+E03F) = 0
Repeats (U+E040-U+E04F) = 0
...

characters = 1
alternates = 0
ligatures = 0

; Stylistic sets:

small staff = 0
short flags = 0
...
```

##### [Exclude]
Any glyphnames, followed by `= 1`, that you wish to exclude from generation
can be entered in this section. This is a good option to make sure that certain
characters remain untouched, even if you've chosen to globally overwrite
preexisting glyphs when building.

```
[Exclude]

uniE032 = 1
uniE036 = 0
```

In this example, the glyph *finalBarline* will be excluded from generation,
while the glyph *barlineDashed* will be included even if it's listed, since it
has a value of 0.

Be sure to remove any slashes from glyphnames in this section when copying
them directly from FontLab Studio.

##### [Global]

Options affecting the entire build are available in this section. `draw missing`
lets you choose whether or not to automatically generate non-existent parent
glyphs whenever possible, according to the settings provided in later sections.
For obvious reasons, this feature is limited to very rudimentary shapes like
barlines, stems, augmentation dots, accordion ranks, etc.

`handle replaced` lets you choose between different ways to handle
pre-existing glyphs: 0 will simply skip them, 1 will append the name of the
glyphs with a timestamp, as formatted below, and set the unicode to None.
If set to 2, any preexisting glyphs will be overwritten, so handle this
option with care!

`timestamp` is where you specify the aforementioned timestamp format.
You may freely choose between any of the letters or separators stated in the
succeeding explanatory comments, as well as the order in which to place them.

`mark colour` takes a colour code between 0 and 250 with which to mark any
generated glyphs. 0 leaves the glyphs unmarked, while the scale goes from red
(1), via, green (75), cyan (130), blue (175), magenta (210) and back to red.
Choose any shade you desire on this spectrum.

The option `values in staff spaces` is of particular importance to the
following sections, as it allows you to specify whether to interpret placement
and dimensional settings of glyphs in staff spaces, as is commonly used in the
SMuFL documentation and metadata (1), or in font units (0). Exceptions to this
global rule may be made by enclosing values in parenthesis, however, for the
sake of efficiency if not consistency, it is advisable to keep these to a
minimum.

##### [Accordion]

These options apply to the rank glyphs in the Accordion range, and let's you
choose the size and line width at which to draw the empty ranks and coupler
dot, as well as provide any overshoot value to use when drawing and building
registration composites.

##### [Barlines]

SMuFLbuilder has the ability to draw all types of barlines, so this section
provides all the options needed for this purpose. Most of these, and many other
dimensional settings in the file, can be  find in the Engraving Options section
in the SMuFL metadata file, and may therefore  be useful later on in the design
process, when generating font metadata.

##### [Beams]

This section houses all settings related to note beams, which at present, is
limited to glyphs in the Beamed groups of notes range. Settings for placement
of tuplet number and bracket, applicable to the same range, is also provided
here.

##### [Dynamics]

This section holds settings for drawing hairpin and niente glyphs, as well as
vertical and horizontal spacing values.

SMuFLbuilder takes both bounding box dimensions, advance widths and
kerning into account when spacing letter components in the dynamics range.
Even so, `component spacing` provides you with an additional value option to
base this spacing on, should you ever need it. Adjustment values for hairpin
height and spacing (gab between components in *dynamicMessaDiVoce*) is also
available here.

##### [Flags]

Here you'll find the necessary settings to space your internal flags (for 32nd
notes and higher) and straight flags.

##### [Notes]

This section will potentially provide options for drawing geometric notehead
shapes and slash noteheads, among other things. For the time being, though,
only the radius at which to draw augmentation dots can be found here.

##### [Octaves]

While SMuFLbuilder handles vertical spacing of superscript glyphs in the Octaves
range automatically, by relating them to the height of the numerals, `superscript
height adjustment` gives you the option to tweak SMuFLbuilder's algorithm.

To make sure that horizontal spacing of superscript letters is equally to your liking,
you may adjust their relation to the numerical characters with `superscript kern`.
Overall spacing adjustment for the letters in this section is provided by
`component spacing`.

Additionally, since SMuFL does not include every single component in the Octaves
range as recommended characters, SMuFLbuilder requires a few extra characters to be
able to construct certain composites. While you do not need to encode these
characters in the font, they must each have a name which you may provide in
this section:
```
...
c = octaveBaselineC
l = octaveBaselineL
o = octaveBaselineO
s = octaveBaselineS
```

These names are only recommendations; you need to make sure that
the names are unique to each character, but they can be named whatever you like.

##### [Repeats]

While the Barlines section contains the settings for the actual repeat *barlines*,
the Repeats section presently provides the settings for repeat dot size (radius),
and separation relative to barlines.

Potentially, this section will also contain settings for bar repeats.

##### [Staves]

Here you can find every setting needed to draw both staff lines and leger lines.
options for three different widths of each type, as recommended by SMuFL, are
provided, in addition to line thickness and the amount of leger line extension.

##### [Stems]

This secion provides stem dimensions used in different SMuFL ranges. In addition
to the obvious settings for stem thickness, and lengths, `stem retraction`
provides the means to retract the headless stems in the Beamed groups of notes
range (U+E204-U+E20A) from the baseline by a desired amount.

While SMuFL does not specify such a retraction for the stems in this range,
they are present in the current version 1.38 of Bravura, and so, they are
provided as an option here as well.

##### [Time Signatures]

Most of the calculations in the ranges related to time signatures are done
without the need for user input, apart from the required glyphs, of course.
One exception to this is fractional time signature glyphs. SMuFLbuilder
provides decent automatic spacing for these glyphs under normal circumstances,
but even then, you will likely improve your results by experimenting with these
options:

```
fraction spacing = 0.08
fraction sidebearings = 0.04
fraction one kern = 0.08
fraction four kern = -0.16
...

```

While the effect of most of these options are made fairly obvious by their names,
it should be clarified that the kerning settings are specifically intended
for adjustment related to the bottom serif of numerator 1 and the triangular
top of denominator 4.

As with the Octaves section, an additional non-standard component – in the form of
a vertical stroke – is needed to be able to build cut time symbols in both the main and
supplementary time signature ranges. The name of this glyph can be provided
here, and again, does not need to be encoded in the font.

##### [Tremolos]

SMuFlbuilder does not yet draw tremolo glyphs, but the means to spacing both
tremolo slashes and divisi dots can be found in this section.

##### [Set Suffixes]

In this last section you have the option to alter the suffixes of stylistic
sets from the ones used in Bravura, should you ever feel so inclined.

## Required and created glyphs

The following paragraphs give an overview of the ranges and glyphs that
SMuFLbuilder is able to create, as well as the glyphs required to produce them.
In some cases, glyphs not presently encoded in SMuFL are needed to build
certain composites. These glyphs do not need to be encoded, and their names
below are only recommendations. As mentioned above, their actual names must
however be specified in the settings, under the section to which they apply.

##### Staves (U+E010-U+E02F)
<details open>
    <summary>Required</summary>
    None

</details> <details open>
    <summary>Created</summary>
    All

</details>

##### Barlines (U+E030-U+E03F)
<details open>
    <summary>Required</summary>
    None

</details>
<details open>
    <summary>Created</summary>
    All

</details>

##### Repeats (U+E040-U+E04F)
<details open>
    <summary>Required</summary>
    None

</details> <details open>
    <summary>Created</summary>
    All

</details>

##### Time signatures (U+E080-U+E09F)
<details open>
<summary>Required</summary>
U+E080&nbsp;|&nbsp;<i>timeSig0</i>, U+E081&nbsp;|&nbsp;<i>timeSig1</i>,
U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>,
U+E084&nbsp;|&nbsp;<i>timeSig4</i>, U+E085&nbsp;|&nbsp;<i>timeSig5</i>,
U+E086&nbsp;|&nbsp;<i>timeSig6</i>, U+E087&nbsp;|&nbsp;<i>timeSig7</i>,
U+E088&nbsp;|&nbsp;<i>timeSig8</i>, U+E089&nbsp;|&nbsp;<i>timeSig9</i>,
U+E08A&nbsp;|&nbsp;<i>timeSigCommon</i>,
U+E08E&nbsp;|&nbsp;<i>timeSigFractionalSlash</i>,
—&nbsp;|&nbsp;<i>timeSigVerticalStroke*</i>

</details>
<details open>
<summary>Created</summary>
U+E08B&nbsp;|&nbsp;<i>timeSigCutCommon</i>,
U+E097&nbsp;|&nbsp;<i>timeSigFractionQuarter</i>,
U+E098&nbsp;|&nbsp;<i>timeSigFractionHalf</i>,
U+E099&nbsp;|&nbsp;<i>timeSigFractionThreeQuarters</i>,
U+E09A&nbsp;|&nbsp;<i>timeSigFractionOneThird</i>,
U+E09B&nbsp;|&nbsp;<i>timeSigFractionTwoThirds</i>, All&nbsp;ligatures

</details>

##### Individual notes (U+E1D0-U+E1EF)
<details open>
<summary>Required</summary>
U+E0A0&nbsp;|&nbsp;<i>noteheadDoubleWhole</i>,
U+E0A0.salt01&nbsp;|&nbsp;<i>noteDoubleWholeAlt</i>,
U+E0A1&nbsp;|&nbsp;<i>noteheadDoubleWholeSquare</i>,
U+E0A2&nbsp;|&nbsp;<i>noteheadWhole</i>,
U+E0A3&nbsp;|&nbsp;<i>noteheadHalf</i>,
U+E0A4&nbsp;|&nbsp;<i>noteheadBlack</i>,
U+E240&nbsp;|&nbsp;<i>flag8thUp</i>, U+E241&nbsp;|&nbsp;<i>flag8thDown</i>,
U+E242&nbsp;|&nbsp;<i>flag16thUp</i>, U+E243&nbsp;|&nbsp;<i>flag16thDown</i>,
U+E250&nbsp;|&nbsp;<i>flagInternalUp</i>,
U+E251&nbsp;|&nbsp;<i>flagInternalDown</i>

</details>
<details open>
<summary>Created</summary>
All

</details>
<details open>
    <summary>Created</summary>
    All

</details>

##### Beamed groups of notes (U+E1F0-U+E20F)
<details open>
    <summary>Required</summary>
    U+E0A4&nbsp;|&nbsp;<i>noteheadBlack</i>,
    U+E883&nbsp;|&nbsp;<i>tuplet3</i>

</details>
<details open>
    <summary>Created</summary>
    All

</details>

##### Stems (U+E210-U+E21F)
<details open>
    <summary>Required</summary>
    U+E22A&nbsp;|&nbsp;<i>buzzRoll</i>,
    U+E22B&nbsp;|&nbsp;<i>pendereckiTremolo</i>,
    U+E263&nbsp;|&nbsp;<i>accidentalDoubleSharp</i>,
    U+E607&nbsp;|&nbsp;<i>windMultiphonicsBlackStem</i>,
    U+E608&nbsp;|&nbsp;<i>windMultiphonicsWhiteStem</i>,
    U+E609&nbsp;|&nbsp;<i>windMultiphonicsBlackWhiteStem</i>,
    U+E618&nbsp;|&nbsp;<i>stringsBowBehindBridge</i>,
    U+E619&nbsp;|&nbsp;<i>stringsBowOnBridge</i>,
    U+E61A&nbsp;|&nbsp;<i>stringsBowOnTailpiece</i>,
    U+E623&nbsp;|&nbsp;<i>stringsVibratoPulse</i>,
    U+E63B&nbsp;|&nbsp;<i>pluckedDampOnStem</i>,
    U+E645&nbsp;|&nbsp;<i>vocalSprechgesang</i>,
    U+E646&nbsp;|&nbsp;<i>vocalsSussurando</i>,
    U+E694&nbsp;|&nbsp;<i>harpStringNoiseStem</i>,
    U+E808&nbsp;|&nbsp;<i>pictSwishStem</i>

</details>
<details open>
    <summary>Created</summary>
    All

</details>

##### Tremolos (U+E220-U+E23F)
<details open>
    <summary>Required</summary>
    U+E220&nbsp;|&nbsp;<i>tremolo1</i>
    U+E225&nbsp;|&nbsp;<i>tremoloFingered1</i>
    U+E4A2&nbsp;|&nbsp;<i>articStaccatoAbove</i>

</details>
<details open>
    <summary>Created</summary>
    U+E221&nbsp;|&nbsp;<i>tremolo2</i>,
    U+E222&nbsp;|&nbsp;<i>tremolo3</i>,
    U+E223&nbsp;|&nbsp;<i>tremolo4</i>,
    U+E224&nbsp;|&nbsp;<i>tremolo5</i>,
    U+E226&nbsp;|&nbsp;<i>tremoloFingered2</i>,
    U+E227&nbsp;|&nbsp;<i>tremoloFingered3</i>,
    U+E228&nbsp;|&nbsp;<i>tremoloFingered4</i>,
    U+E229&nbsp;|&nbsp;<i>tremoloFingered5</i>,
    U+E22E&nbsp;|&nbsp;<i>tremoloDivisiDots2</i>,
    U+E22F&nbsp;|&nbsp;<i>tremoloDivisiDots3</i>,
    U+E230&nbsp;|&nbsp;<i>tremoloDivisiDots4</i>,
    U+E231&nbsp;|&nbsp;<i>tremoloDivisiDots6</i>

</details>

##### Flags (U+E240-U+E25F)
<details open>
    <summary>Required</summary>
    U+E242&nbsp;|&nbsp;<i>flag16thUp</i>,
    U+E243&nbsp;|&nbsp;<i>flag16thDown</i>,
    U+E250&nbsp;|&nbsp;<i>flagInternalUp</i>,
    U+E251&nbsp;|&nbsp;<i>flagInternalDown</i>

</details>
<details open>
    <summary>Created</summary>
    U+E24A&nbsp;|&nbsp;<i>flag256thUp</i>,
    U+E24B&nbsp;|&nbsp;<i>flag256thDown</i>,
    U+E24C&nbsp;|&nbsp;<i>flag512thUp</i>,
    U+E24D&nbsp;|&nbsp;<i>flag512thDown</i>,
    U+E24E&nbsp;|&nbsp;<i>flag1024thUp</i>,
    U+E24F&nbsp;|&nbsp;<i>flag1024thDown</i>,
    U+E244&nbsp;|&nbsp;<i>flag32ndUp</i>,
    U+E245&nbsp;|&nbsp;<i>flag32ndDown</i>,
    U+E246&nbsp;|&nbsp;<i>flag64thUp</i>,
    U+E247&nbsp;|&nbsp;<i>flag64thDown</i>,
    U+E248&nbsp;|&nbsp;<i>flag128thUp</i>,
    U+E249&nbsp;|&nbsp;<i>flag128thDown</i>,
    All&nbsp;stylistic&nbsp;sets

</details>

##### Octaves (U+E510-U+E51F)
<details open>
<summary>Required</summary>
U+E510&nbsp;|&nbsp;<i>ottava</i>,
U+E514&nbsp;|&nbsp;<i>quindicesima</i>,
U+E517&nbsp;|&nbsp;<i>ventiduesima</i>,
U+EC91&nbsp;|&nbsp;<i>octaveBaselineA</i>,
U+EC93&nbsp;|&nbsp;<i>octaveBaselineB</i>,
U+EC95&nbsp;|&nbsp;<i>octaveBaselineM</i>,
U+EC97&nbsp;|&nbsp;<i>octaveBaselineV</i>,
—&nbsp;|&nbsp;<i>octaveBaselineS*</i>

</details>
<details open>
<summary>Created</summary>
All

</details>

##### Dynamics (U+E520-U+E54F)
<details open>
<summary>Required</summary>
U+E520&nbsp;|&nbsp;<i>dynamicPiano</i>,
U+E521&nbsp;|&nbsp;<i>dynamicMezzo</i>,
U+E522&nbsp;|&nbsp;<i>dynamicForte</i>,
U+E523&nbsp;|&nbsp;<i>dynamicRinforzando</i>,
U+E524&nbsp;|&nbsp;<i>dynamicSforzando</i>,
U+E525&nbsp;|&nbsp;<i>dynamicZ</i>

</details>
<details open>
<summary>Created</summary>
U+E527&nbsp;|&nbsp;<i>dynamicPPPPPP</i>,
U+E528&nbsp;|&nbsp;<i>dynamicPPPPP</i>,
U+E529&nbsp;|&nbsp;<i>dynamicPPPP</i>,
U+E52A&nbsp;|&nbsp;<i>dynamicPPP</i>,
U+E52B&nbsp;|&nbsp;<i>dynamicPP</i>,
U+E52C&nbsp;|&nbsp;<i>dynamicMP</i>,
U+E52D&nbsp;|&nbsp;<i>dynamicMF</i>,
U+E52E&nbsp;|&nbsp;<i>dynamicPF</i>,
U+E52F&nbsp;|&nbsp;<i>dynamicFF</i>,
U+E530&nbsp;|&nbsp;<i>dynamicFFF</i>,
U+E531&nbsp;|&nbsp;<i>dynamicFFFF</i>,
U+E532&nbsp;|&nbsp;<i>dynamicFFFFF</i>,
U+E533&nbsp;|&nbsp;<i>dynamicFFFFFF</i>,
U+E534&nbsp;|&nbsp;<i>dynamicFortePiano</i>,
U+E535&nbsp;|&nbsp;<i>dynamicForzando</i>,
U+E536&nbsp;|&nbsp;<i>dynamicSforzando1</i>,
U+E537&nbsp;|&nbsp;<i>dynamicSforzandoPiano</i>,
U+E538&nbsp;|&nbsp;<i>dynamicSforzandoPianissimo</i>,
U+E539&nbsp;|&nbsp;<i>dynamicSforzato</i>,
U+E53A&nbsp;|&nbsp;<i>dynamicSforzatoPiano</i>,
U+E53B&nbsp;|&nbsp;<i>dynamicSforzatoFF</i>,
U+E53C&nbsp;|&nbsp;<i>dynamicRinforzando1</i>,
U+E53D&nbsp;|&nbsp;<i>dynamicRinforzando2</i>,
U+E53E&nbsp;|&nbsp;<i>dynamicCrecendoHairpin</i>,
U+E53F&nbsp;|&nbsp;<i>dynamicDiminuendoHairpin</i>,
U+E540&nbsp;|&nbsp;<i>dynamicMessaDiVoce</i>
U+E541&nbsp;|&nbsp;<i>dynamicNienteForHairpin</i>

</details>

##### Accordion (U+E8A0-U+E8DF)
<details open>
    <summary>Required</summary>
    None

</details>
<details open>
    <summary>Created</summary>
    All&nbsp;ranks&nbsp;and&nbsp;registration

</details>

##### Time signatures supplement (U+EC80-U+EC8F)
<details open>
<summary>Required</summary>
U+E082&nbsp;|&nbsp;<i>timeSig2</i>,
U+E083&nbsp;|&nbsp;<i>timeSig3</i>,
—&nbsp;|&nbsp;<i>timeSigVerticalStroke*</i>

</details>
<details open>
<summary>Created</summary>
U+EC85&nbsp;|&nbsp;<i>timeSigCut2</i>, U+EC86&nbsp;|&nbsp;<i>timeSigCut3</i>

</details>

##### Octaves supplement (U+EC90-U+EC9F)
<details open>
<summary>Required</summary>
U+EC91&nbsp;|&nbsp;<i>octaveBaselineA</i>,
U+EC93&nbsp;|&nbsp;<i>octaveBaselineB</i>,
U+EC95&nbsp;|&nbsp;<i>octaveBaselineM</i>,
U+EC97&nbsp;|&nbsp;<i>octaveBaselineV</i>,
—&nbsp;|&nbsp;<i>octaveBaselineC*</i>, —&nbsp;|&nbsp;<i>octaveBaselineL*</i>,
—&nbsp;|&nbsp;<i>octaveBaselineO*</i>

</details>
<details open>
<summary>Created</summary>
U+EC90&nbsp;|&nbsp;<i>octaveLoco</i>,
U+EC92&nbsp;|&nbsp;<i>octaveSuperscriptA</i>,
U+EC94&nbsp;|&nbsp;<i>octaveSuperscriptB</i>,
U+EC96&nbsp;|&nbsp;<i>octaveSuperscriptM</i>,
U+EC98&nbsp;|&nbsp;<i>octaveSuperscriptV</i>

</details>

##### Turned time signatures (U+ECE0-U+ECEF)
<details open>
<summary>Required</summary>
U+E080&nbsp;|&nbsp;<i>timeSig0</i>, U+E081&nbsp;|&nbsp;<i>timeSig1</i>,
U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>,
U+E084&nbsp;|&nbsp;<i>timeSig4</i>, U+E085&nbsp;|&nbsp;<i>timeSig5</i>,
U+E086&nbsp;|&nbsp;<i>timeSig6</i>, U+E087&nbsp;|&nbsp;<i>timeSig7</i>,
U+E088&nbsp;|&nbsp;<i>timeSig8</i>, U+E089&nbsp;|&nbsp;<i>timeSig9</i>,
U+E08A&nbsp;|&nbsp;<i>timeSigCommon</i>,
—&nbsp;|&nbsp;<i>timeSigVerticalStroke*</i>

</details>
<details open>
    <summary>Created</summary>
    All

</details>

##### Reversed time signatures (U+ECF0-U+ECFF)
<details open>
<summary>Required</summary>
U+E080&nbsp;|&nbsp;<i>timeSig0</i>, U+E081&nbsp;|&nbsp;<i>timeSig1</i>,
U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>,
U+E084&nbsp;|&nbsp;<i>timeSig4</i>, U+E085&nbsp;|&nbsp;<i>timeSig5</i>,
U+E086&nbsp;|&nbsp;<i>timeSig6</i>, U+E087&nbsp;|&nbsp;<i>timeSig7</i>,
U+E088&nbsp;|&nbsp;<i>timeSig8</i>, U+E089&nbsp;|&nbsp;<i>timeSig9</i>,
U+E08A&nbsp;|&nbsp;<i>timeSigCommon</i>,
—&nbsp;|&nbsp;<i>timeSigVerticalStroke*</i>

</details>
<details open>
    <summary>Created</summary>
    All

</details>

\* Component not encoded in SMuFL

Please experiment, enjoy and please let me know if anything doesn't work or
can be improved!

Knut






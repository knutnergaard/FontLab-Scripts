# SMuFLbuilder
## Documentation

SMuFLbuilder is a Python script for FontLab Studio 5 that lets you build composite glyphs across selected ranges in SMuFL fonts, based on created components.
For glyphs involving primitives (like barlines, staves, stems, etc.), SMuFLbuilder will even draw the parent glyphs for you, based on your own specifications.

Considering the many component-based symbols used in music notation generally, as well as the numerous, partially or fully, visually identical glyphs found in the SMuFL standard, makes SMuFLbuilder a real timesaver for any creator of SMuFL fonts.

### License
SMuFLbuilder is written and maintained by Knut Nergaard, and is available under the **[MIT License](https://github.com/knutnergaard/FontLab-Scripts/blob/main/SMuFL/smufl_builder/license.txt)**.
Copyright © by Knut Nergaard 2021.

### Supported ranges
The current beta version (0.1) supports the following ranges (including recommended alternates and ligatures where applicable):

- Staves (U+E010-U+E02F)
- Barlines (U+E030-U+E03F)
- Repeats (U+E040-U+E04F)
- Time signatures (U+E080-U+E09F)
- Individual notes (U+E1D0-U+E1EF)
- Beamed groups of notes (U+E1F0-U+E20F)
- Stems (U+E210-U+E21F)
- Tremolos (U+E220-U+E23F)
- Flags (U+E240-U+E25F)
- Accordion (U+E8A0-U+E8DF)
- Time signatures supplement (U+EC80-U+EC8F)
- Turned time signatures (U+ECE0-U+ECEF)
- Reversed time signatures (U+ECF0-U+ECFF)

### Installation
Install SMuFLbuilder manually as follows:

**On Mac:**

1. Move the folder `SMuFL` to `~/Library/Application Support/FontLab/Studio 5/Macros`.
2. Move the module folder named `smuflbuilder` to `~/Library/Application Support/FontLab/Studio 5/Macros/System/Modules`.
3. Put the file named `smuflbuilder_settings.ini` anywhere you like on your system, and rename the file if you wish.
4. In the `smuflbuilder` module folder, open `filepaths.py` and enter your chosen filepath (including the filename) in between the empty quote marks of `user = ''`.

**On Windows:**

The installation process on Windows is exactly the same as above, except that the filepaths will be different. You will also need to change the filepath for the default settings in filepaths.py to reflect the Windows syntax.
An installer is planned to make this easier.

### Running the script
SMuFLbuilder is most simply from the Macros panel in FontLab Studio. Assuming **Python 2.7** is correctly installed on your system,

- Select Wiew > Toolbars > Macro in the application menu to show the Macro Toolbar.
- Choose `SMuFL` in the Top level dropdown and then `SMuFLbuilder` in the dropdown to the right.
- Press the triangular 'play' button to run the script.
- Refer to the chapter *Macro Programming* in the FontLab Studio Manual for more detailed instructions.

### Settings
All user-specific options and settings for SMuFLbuilder are defined in `smuflbuilder_settings.ini`, which can be edited in any basic text editor.
Default settings are defined in a separate file named `defaults.ini`, located in the FontLab Modules folder.

Defaults are always read by the script prior to user defined settings, which means that, for the sake of simplicity, `smuflbuilder_settings.ini` only needs to contain the settings differing from the defaults.
Short of actually deleting what you don't need, however, settings can be disabled by a preceding semicolon `;`, converting them into comments (see below).

A rundown of the most important sections in this settings file, will give you what you need to make SMuFLbuilder work for you:

**[Include]**

Unsurprisingly, this section is where you choose the ranges and categories to include in your build.

```
[Include]

; Include (1) or exclude (0) ranges, alternates, ligatures and sets from generation:

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

To make quick changes as easy as possible, booleans (true/false values) in this and other sections are set by 1 (true) and 0 (false).

**[Exclude]**

Any glyphnames, followed by `= 1`, that you wish to exclude from generation can be entered in this section.

```
[Exclude]

uniE032 = 1
```

In the example, the glyph finalBarline will be excluded from generation. If value is set to 0, the glyph will be included anyway.

(Be sure to remove any slashes (`/`) from glyphnames when copying them directly from FontLab Studio.)

**[Global]**

```
[Global]

mark colour = 130
...

values in staff spaces = 1
...
```

The colour with which new glyphs are marked is chosen in this section. The given value `130` gives you cyan, while `0` would leave glyphs unmarked. Other example values are given in the file.

The option `values in staff spaces` is especially important, as this is where you choose whether adjustment values and dimensions in the following sections are given in staff spaces (really, 1/4 of the font UPM) or font units.
At present, there is no way to specify this on an option-by-option basis.

The following sections are dedicated to specific ranges and font elements. A more thorough description of these is planned for a future installment of this documentation. Until then, their names should hopefully be self-explanatory enough to anyone with a general knowledge of music engraving and font creation and a familiarity with SMuFL more specifically.

### Required and Created Glyphs

A full overview of glyphs required for full support is in the works.
For the time being, here's a list of all the ranges and glyphs SMuFLbuilder will create for you:


**Staves (U+E010-U+E02F)**

All


**Barlines (U+E030-U+E03F)**

All


**Repeats (U+E040-U+E04F)**

All


**Stems (U+E210-U+E21F)**

All


**Time signatures (U+E080-U+E09F)**

 U+E08B | *timeSigCutCommon* | U+E097 | *timeSigFractionQuarter*, U+E098 | *timeSigFractionHalf*, U+E099 | *timeSigFractionThreeQuarters*, U+E09A | *timeSigFractionOneThird*, U+E09B | *timeSigFractionTwoThirds*
\+ All Ligatures


**Individual notes (U+E1D0-U+E1EF)**

 U+E1D9 | *note16thUp*, U+E1D8 | *note8thDown*, U+E1D3 | *noteHalfUp*, U+E1D2 | *noteWhole*, U+E1D1 | *noteDoubleWholeSquare*, U+E1D0 | *noteDoubleWhole*, U+E1D7 | *note8thUp*, U+E1D6 | *noteQuarterDown*, U+E1D5 | *noteQuarterUp*, U+E1D4 | *noteHalfDown*, U+E1E0 | *note128thDown*, U+E1E1 | *note256thUp*, U+E1E2 | *note256thDown*, U+E1E3 | *note512thUp*, U+E1E4 | *note512thDown*, U+E1E5 | *note1024thUp*, U+E1E6 | *note1024thDown*, None | *None*, U+E1DC | *note32ndDown*, U+E1DB | *note32ndUp*, U+E1DA | *note16thDown*, U+E1DF | *note128thUp*, U+E1DE | *note64thDown*, U+E1DD | *note64thUp*

**Beamed groups of notes (U+E1F0-U+E20F)**

 U+E1FF | *textTuplet3ShortStem*, U+E1FA | *textCont16thBeamLongStem*, U+E209 | *textHeadlessBlackNoteFrac16thLongStem*, U+E1FC | *textAugmentationDot*, U+E1FB | *textCont32ndBeamLongStem*, U+E206 | *textHeadlessBlackNoteFrac8thShortStem*, U+E207 | *textHeadlessBlackNoteFrac8thLongStem*, U+E200 | *textTupletBracketEndShortStem*, U+E201 | *textTupletBracketStartLongStem*, U+E202 | *textTuplet3LongStem*, U+E203 | *textTupletBracketEndLongStem*, U+E208 | *textHeadlessBlackNoteFrac16thShortStem*, U+E1F8 | *textCont8thBeamLongStem*, U+E1F5 | *textBlackNoteFrac16thLongStem*, U+E1F4 | *textBlackNoteFrac16thShortStem*, U+E1F6 | *textBlackNoteFrac32ndLongStem*, U+E1F1 | *textBlackNoteLongStem*, U+E1F0 | *textBlackNoteShortStem*, U+E1F3 | *textBlackNoteFrac8thLongStem*, U+E1F2 | *textBlackNoteFrac8thShortStem*, U+E1F9 | *textCont16thBeamShortStem*, U+E20A | *textHeadlessBlackNoteFrac32ndLongStem*

**Accordion (U+E8A0-U+E8DF)**

All


**Reversed time signatures (U+ECF0-U+ECFF)**

 U+ECF0 | *timeSig0Reversed*, U+ECF1 | *timeSig1Reversed*, U+ECF2 | *timeSig2Reversed*, U+ECF3 | *timeSig3Reversed*, U+ECF4 | *timeSig4Reversed*, U+ECF5 | *timeSig5Reversed*, U+ECF6 | *timeSig6Reversed*, U+ECF7 | *timeSig7Reversed*, U+ECF8 | *timeSig8Reversed*, U+ECF9 | *timeSig9Reversed*, U+ECFA | *timeSigCommonReversed*, U+ECFB | *timeSigCutCommonReversed*

**Time signatures supplement (U+EC80-U+EC8F)**

 U+EC85 | *timeSigCut2*, U+EC86 | *timeSigCut3*


**Flags (U+E240-U+E25F)**

 U+E24A | *flag256thUp*, U+E24B | *flag256thDown*, U+E24C | *flag512thUp*, U+E24D | *flag512thDown*, U+E24E | *flag1024thUp*, U+E24F | *flag1024thDown*, U+E244 | *flag32ndUp*, U+E245 | *flag32ndDown*, U+E246 | *flag64thUp*, U+E247 | *flag64thDown*, U+E248 | *flag128thUp*, U+E249 | *flag128thDown*
\+ stylistic sets


**Tremolos (U+E220-U+E23F)**

U+E220 | *tremolo1*, U+E225 | *tremoloFingered1*, U+E4A2 |
*articStaccatoAbove*


**Turned time signatures (U+ECE0-U+ECEF)**

U+ECE0 | *timeSig0Turned*, U+ECE1 | *timeSig1Turned*, U+ECE2 | *timeSig2Turned*, U+ECE3 | *timeSig3Turned*, U+ECE4 | *timeSig4Turned*, U+ECE5 | *timeSig5Turned*, U+ECE6 | *timeSig6Turned*, U+ECE7 | *timeSig7Turned*, U+ECE8 | *timeSig8Turned*, U+ECE9 | *timeSig9Turned*, U+ECEA | *timeSigCommonTurned*, U+ECEB | *timeSigCutCommonTurned*


Please experiment, enjoy and be sure to let me know if anything doesn't work or needs improvement!

Knut

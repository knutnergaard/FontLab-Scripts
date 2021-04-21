# SMuFLbuilder
## Documentation

SMuFLbuilder is a Python script for FontLab Studio 5 that lets you build composite glyphs across selected ranges in SMuFL fonts, based on created components.
For glyphs involving primitives (like barlines, staves, stems, etc.), SMuFLbuilder will even draw the parent glyphs for you, based on your own specifications.

Considering the many component-based symbols used in music notation generally, as well as the numerous, partially or fully, visually identical glyphs found in the SMuFL standard, SMuFLbuilder can be a real timesaver for any creator of SMuFL fonts.

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

###Required and Created Glyphs

The following paragraphs give an overview of the ranges and glyphs that SMuFLbuilder is able  create, as well as the glyphs required to produce them.
In some cases, glyphs not presently encoded in SMuFL are needed to build certain composites. These glyphs do not need to be encoded, and their names below are only recommendations. Their actual names, however, must be specified in the settings, under the section to which they apply.

**Staves (U+E010-U+E02F)**
<details open>
<summary>Required</summary>
None

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Barlines (U+E030-U+E03F)**
<details open>
<summary>Required</summary>
None

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Repeats (U+E040-U+E04F)**
<details open>
<summary>Required</summary>
None

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Time signatures (U+E080-U+E09F)**
<details open>
<summary>Required</summary>
U+E080&nbsp;|&nbsp;<i>timeSig0</i>, U+E081&nbsp;|&nbsp;<i>timeSig1</i>, U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>, U+E084&nbsp;|&nbsp;<i>timeSig4</i>, U+E085&nbsp;|&nbsp;<i>timeSig5</i>, U+E086&nbsp;|&nbsp;<i>timeSig6</i>, U+E087&nbsp;|&nbsp;<i>timeSig7</i>, U+E088&nbsp;|&nbsp;<i>timeSig8</i>, U+E089&nbsp;|&nbsp;<i>timeSig9</i>, U+E08A&nbsp;|&nbsp;<i>timeSigCommon</i>, -&nbsp;|&nbsp;<i>timeSigVerticalStroke*</i>, U+E08E&nbsp;|&nbsp;<i>timeSigFractionalSlash</i>

</details>
<details open>        
<summary>Created</summary>
U+E08B&nbsp;|&nbsp;<i>timeSigCutCommon</i>, U+E097&nbsp;|&nbsp;<i>timeSigFractionQuarter</i>, U+E098&nbsp;|&nbsp;<i>timeSigFractionHalf</i>, U+E099&nbsp;|&nbsp;<i>timeSigFractionThreeQuarters</i>, U+E09A&nbsp;|&nbsp;<i>timeSigFractionOneThird</i>, U+E09B&nbsp;|&nbsp;<i>timeSigFractionTwoThirds</i>, All ligatures

</details>

**Individual notes (U+E1D0-U+E1EF)**
<details open>
<summary>Required</summary>
U+E0A0&nbsp;|&nbsp;<i>noteheadDoubleWhole</i>, –&nbsp;|&nbsp;<i>uniE0A0.salt01</i>, U+E0A1&nbsp;|&nbsp;<i>noteheadDoubleWholeSquare</i>, U+E0A2&nbsp;|&nbsp;<i>noteheadWhole</i>, U+E0A3&nbsp;|&nbsp;<i>noteheadHalf</i>, U+E0A4&nbsp;|&nbsp;<i>noteheadBlack</i>, U+E1E7&nbsp;|&nbsp;<i>augmentationDot</i>, U+E210&nbsp;|&nbsp;<i>stem</i>, U+E240&nbsp;|&nbsp;<i>flag8thUp</i>, U+E241&nbsp;|&nbsp;<i>flag8thDown</i>, U+E242&nbsp;|&nbsp;<i>flag16thUp</i>, U+E243&nbsp;|&nbsp;<i>flag16thDown</i>, U+E250&nbsp;|&nbsp;<i>flagInternalUp</i>, U+E251&nbsp;|&nbsp;<i>flagInternalDown</i>

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Beamed groups of notes (U+E1F0-U+E20F)**
<details open>
<summary>Required</summary>
U+E0A4&nbsp;|&nbsp;<i>noteheadBlack</i>, U+E883&nbsp;|&nbsp;<i>tuplet3</i>

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Stems (U+E210-U+E21F)**
<details open>
<summary>Required</summary>
U+E22A&nbsp;|&nbsp;<i>buzzRoll</i>, U+E22B&nbsp;|&nbsp;<i>pendereckiTremolo</i>, U+E263&nbsp;|&nbsp;<i>accidentalDoubleSharp</i>, U+E607&nbsp;|&nbsp;<i>windMultiphonicsBlackStem</i>, U+E608&nbsp;|&nbsp;<i>windMultiphonicsWhiteStem</i>, U+E609&nbsp;|&nbsp;<i>windMultiphonicsBlackWhiteStem</i>, U+E618&nbsp;|&nbsp;<i>stringsBowBehindBridge</i>, U+E619&nbsp;|&nbsp;<i>stringsBowOnBridge</i>, U+E61A&nbsp;|&nbsp;<i>stringsBowOnTailpiece</i>, U+E623&nbsp;|&nbsp;<i>stringsVibratoPulse</i>, U+E63B&nbsp;|&nbsp;<i>pluckedDampOnStem</i>, U+E645&nbsp;|&nbsp;<i>vocalSprechgesang</i>, U+E646&nbsp;|&nbsp;<i>vocalsSussurando</i>, U+E694&nbsp;|&nbsp;<i>harpStringNoiseStem</i>, U+E808&nbsp;|&nbsp;<i>pictSwishStem</i>

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Tremolos (U+E220-U+E23F)**
<details open>
<summary>Required</summary>
None

</details>
<details open>        
<summary>Created</summary>
U+E221&nbsp;|&nbsp;<i>tremolo2</i>, U+E222&nbsp;|&nbsp;<i>tremolo3</i>, U+E223&nbsp;|&nbsp;<i>tremolo4</i>, U+E224&nbsp;|&nbsp;<i>tremolo5</i>, U+E226&nbsp;|&nbsp;<i>tremoloFingered2</i>, U+E227&nbsp;|&nbsp;<i>tremoloFingered3</i>, U+E228&nbsp;|&nbsp;<i>tremoloFingered4</i>, U+E229&nbsp;|&nbsp;<i>tremoloFingered5</i>, U+E22E&nbsp;|&nbsp;<i>tremoloDivisiDots2</i>, U+E22F&nbsp;|&nbsp;<i>tremoloDivisiDots3</i>, U+E230&nbsp;|&nbsp;<i>tremoloDivisiDots4</i>, U+E231&nbsp;|&nbsp;<i>tremoloDivisiDots6</i>

</details>

**Flags (U+E240-U+E25F)**
<details open>
<summary>Required</summary>
U+E242&nbsp;|&nbsp;<i>flag16thUp</i>, U+E243&nbsp;|&nbsp;<i>flag16thDown</i>, U+E250&nbsp;|&nbsp;<i>flagInternalUp</i>, U+E251&nbsp;|&nbsp;<i>flagInternalDown</i>

</details>
<details open>        
<summary>Created</summary>
U+E24A&nbsp;|&nbsp;<i>flag256thUp</i>, U+E24B&nbsp;|&nbsp;<i>flag256thDown</i>, U+E24C&nbsp;|&nbsp;<i>flag512thUp</i>, U+E24D&nbsp;|&nbsp;<i>flag512thDown</i>, U+E24E&nbsp;|&nbsp;<i>flag1024thUp</i>, U+E24F&nbsp;|&nbsp;<i>flag1024thDown</i>, U+E244&nbsp;|&nbsp;<i>flag32ndUp</i>, U+E245&nbsp;|&nbsp;<i>flag32ndDown</i>, U+E246&nbsp;|&nbsp;<i>flag64thUp</i>, U+E247&nbsp;|&nbsp;<i>flag64thDown</i>, U+E248&nbsp;|&nbsp;<i>flag128thUp</i>, U+E249&nbsp;|&nbsp;<i>flag128thDown</i>, All stylistic sets

</details>

**Accordion (U+E8A0-U+E8DF)**
<details open>
<summary>Required</summary>
None

</details>
<details open>        
<summary>Created</summary>
All ranks and registration

</details>

**Time signatures supplement (U+EC80-U+EC8F)**
<details open>
<summary>Required</summary>
U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>, -&nbsp;|&nbsp;<i>timeSigVerticalStroke*</i>

</details>
<details open>        
<summary>Created</summary>
U+EC85&nbsp;|&nbsp;<i>timeSigCut2</i>, U+EC86&nbsp;|&nbsp;<i>timeSigCut3</i>

</details>

**Turned time signatures (U+ECE0-U+ECEF)**
<details open>
<summary>Required</summary>
U+E080&nbsp;|&nbsp;<i>timeSig0</i>, U+E081&nbsp;|&nbsp;<i>timeSig1</i>, U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>, U+E084&nbsp;|&nbsp;<i>timeSig4</i>, U+E085&nbsp;|&nbsp;<i>timeSig5</i>, U+E086&nbsp;|&nbsp;<i>timeSig6</i>, U+E087&nbsp;|&nbsp;<i>timeSig7</i>, U+E088&nbsp;|&nbsp;<i>timeSig8</i>, U+E089&nbsp;|&nbsp;<i>timeSig9</i>, U+E08A&nbsp;|&nbsp;<i>timeSigCommon</i>, U+E08B&nbsp;|&nbsp;<i>timeSigCutCommon</i>

</details>
<details open>        
<summary>Created</summary>
All

</details>

**Reversed time signatures (U+ECF0-U+ECFF)**
<details open>
<summary>Required</summary>
U+E080&nbsp;|&nbsp;<i>timeSig0</i>, U+E081&nbsp;|&nbsp;<i>timeSig1</i>, U+E082&nbsp;|&nbsp;<i>timeSig2</i>, U+E083&nbsp;|&nbsp;<i>timeSig3</i>, U+E084&nbsp;|&nbsp;<i>timeSig4</i>, U+E085&nbsp;|&nbsp;<i>timeSig5</i>, U+E086&nbsp;|&nbsp;<i>timeSig6</i>, U+E087&nbsp;|&nbsp;<i>timeSig7</i>, U+E088&nbsp;|&nbsp;<i>timeSig8</i>, U+E089&nbsp;|&nbsp;<i>timeSig9</i>, U+E08A&nbsp;|&nbsp;<i>timeSigCommon</i>, U+E08B&nbsp;|&nbsp;<i>timeSigCutCommon</i>

</details>
<details open>        
<summary>Created</summary>
All

</details>

\* Component not encoded in SMuFL


Please experiment, enjoy and please let me know if anything doesn't work or can be improved!

Knut

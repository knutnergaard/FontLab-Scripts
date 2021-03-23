# build_glyphs
Python scripts for FontLab Studio 5 and later to build ranges of glyphs in SMuFL fonts.

These scripts should be regarded as modules in the work to build an eventual master script that generates glyphs accross SMuFL's entire scope.

## Summary of available scripts
### build_accordion_registrations.py
Builds composites from the combining rank and dot glyphs in SMuFLs Accordion range.

The script assigns grid values to the bounding box of each combining rank glyph, and places dots accordingly. To ensure accurate placements, all glyphs must be registered according to SMuFL guidelines, with the bottom left corner at the origin point, and with zero - width side bearings. Setting for overshoot in round rank glyphs is provided.

For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

### build_barlines.py
Builds composite glyphs in SMuFLs Barlines range from single barline glyphs.
For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

### build_staves.py
Builds composite glyphs in SMuFLs Staves range from single staff line glyphs. Script will draw
primitives in place of non-existent source glyphs, according to engraving default settings below.

For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

### build_time_signatures.py

Builds composite glyphs in the Time Signatures, Time signatures supplement, Turned time signatures and Reversed time signatures ranges. 
Current version supports fractions, cut time glyphs turned glyphs, reversed glyphs and ligatures. Support for stylistic sets is planned. 

**Note:** Script requires the presence of basic Time signature numerals (U+E080 - U+E089), common time symbol (U+E08A) and fraction slash (U+E08E). Additionally, cut time symbols build requires a vertical stroke glyph to be used as component in those glyphs. See script for further instructions.

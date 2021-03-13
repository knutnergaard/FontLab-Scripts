# build_glyphs
Python scripts for FontLab Studio 5 and later to build ranges of glyphs in SMuFL fonts.

These scripts should be regarded as modules in the work to build an eventual master script that generates glyphs accross the entire SMuFL scope.

## Summary of available scripts
### build_accordion_registrations.py
Builds composites from the combining rank and dot glyphs in SMuFLs Accordion ramge.

The script assigns grid values to the bounding box of each combining rank glyph, and places dots accordingly. To ensure accurate placements, all glyphs must be registered according to SMuFL guidelines, with the bottom left corner at the origin point, and with zero - width side bearings. Setting for overshoot in round rank glyphs is provided.

For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

### build_barlines.py
Builds composite glyphs in SMuFLs Barlines range from single barline glyphs.
For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

### build_staves.py
Builds composite glyphs in SMuFLs Staves range from single staff line glyphs.
For any preexisting glyphs, name will be appended with '_001' and unicode will be set to None.

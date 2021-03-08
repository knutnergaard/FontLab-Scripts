# FontLab Scripts for SMuFL
Python scripts to aide the creation of SMuFL fonts using FontLab Studio 5 and later.

## Summary of available scripts
### smufl_to_finale.py
Generates composite glyphs from the SMuFL PUA range in codepoints compatible with Finale's Maestro font for Mac & Windows, and alters
metrics and registration to comply with the software. Any preexisting glyphs at appropriate codepoints are automatically skipped.

**Beware** that the script will decompose any components in the reference glyphs prior to generating new glyphs.

Under the current version, FontLab will crash if you attempt to generate glyphs for both OS encodings at the same time. Therefore, please uncomment and recomment the appropriate line at the bottom of the script to chose different OS.

The script does not currently support horizontal shifting of components, necessary with respect to 'uniE0CE' (noteheadParenthesis).

### check_anchors.py
Compares font anchors to latest Bravura metadata file, published at the [Bravura repository](https://github.com/steinbergmedia/bravura) to find missing or superfluous glyph anchors according to the SMuFL standard. Script will print any findings and mark glyphs with discrepancies unless colour value is set to 0.

### copy_notes_to_glyph_names.py
Renames glyphs with AGLFN names (uniXXXX) to descriptive SMuFL names by copying the annotations made by the script [annotate_glyphs_with_smufl_names](https://github.com/w3c/smufl/blob/gh-pages/scripts/fontlab/annotate_glyphs_with_smufl_names.py), available at the [SMuFL repository](https://github.com/w3c/smufl).

### create_smufl_encoding.py
Generates FontLab encoding file (.enc) for the SMuFL PUA range based on the latest metadata release at the [SMuFL repository].

By default, glyph names are formatted uniXXXX (UV with 'uni' prefix), according to the [AGL specification](https://github.com/adobe-type-tools/agl-specification), but encoding of descriptive SMuFLs glyph names is optional.

**Beware:** If chosen file path already exists, the existing file will be overwritten. The script must be run using Python 3 in the command line. 

Please refer to the FontLab manual for more information about custom encoding tables.

### pua_to_unicode_musical_symbols.py
Generates composite glyphs in Unicode ranges 'Miscellaneous Symbols'and 'Musical Symbols' (UMS) from identical glyphs in the Private User Area (PUA) range of a SMuFL font. Any preexisting glyphs in the UMS ranges are automatically skipped.

Version 1.0 does not generate glyphs in **Medieval and Renaissance**, **Daseian notation** or **Chord diagrams** ranges.

**Beware:** Script will decompose any components in the reference glyphs before generating new glyphs.

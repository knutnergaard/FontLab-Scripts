# FontLab Scripts for SMuFL
Python scripts to aide the creation of SMuFL fonts using FontLab Studio 5 and later.

## Summary of available scripts
### build_glyphs
Scripts to build composite glyphs from basic and combined SMuFL glyphs.
See dedicated readme file.

### check_anchors.py
Compares font anchors to latest Bravura metadata file, published at the [Bravura repository](https://github.com/steinbergmedia/bravura) to find missing or superfluous glyph anchors according to the SMuFL standard. Script will print any findings and mark glyphs with discrepancies unless colour value is set to 0.

Script will skip glyphs not containing descriptive SMuFL names as notes or glyph names.

### clean_smufl_font.py ###
Deletes any unencoded glyphs and glyphs without a valid SMuFL codepoint, i.e., outside the unicode ranges Private User Area (U+E000-U+F8FF), Musical Symbols (U+1D100-U+1D1FF) and the Musical Symbols part of Miscellaneous Symbols (U+2669-U+266F).
Further exclusions can be added to included list of glyph names, which by default contains glyphs *.notdef* and *space*.

**Beware:** This script permanently deletes glyphs, and could, in the event of any software bugs or system flaws, result in unintended data loss. **Use at your own risk!**

### copy_notes_to_glyph_names.py
Renames glyphs with AGLFN names (uniXXXX) to descriptive SMuFL names by copying the annotations made by **set_smufl_names.py** or [annotate_glyphs_with_smufl_names](https://github.com/w3c/smufl/blob/gh-pages/scripts/fontlab/annotate_glyphs_with_smufl_names.py), available at the [SMuFL repository](https://github.com/w3c/smufl).

### create_smufl_encoding.py
Generates FontLab encoding file (.enc) for the SMuFL PUA range based on the latest metadata release at the SMuFL repository.
By default, glyph names are formatted uniXXXX (UV with 'uni' prefix), according to the [AGL specification](https://github.com/adobe-type-tools/agl-specification), but encoding of descriptive SMuFLs glyph names is optional.

**Beware:** If chosen file path already exists, the existing file will be overwritten. The script must be run using Python 3 in the command line. Please refer to the FontLab manual for more information about custom encoding tables.

### create_smufl_encoding_2.py
Same as above, except rewritten in Python 2, and thus, can be run from inside FontLab.

### pua_to_unicode_musical_symbols.py
Generates composite glyphs in Unicode ranges Miscellaneous Symbols and Musical Symbols from identical glyphs in the Private User Area range of a SMuFL font. Any preexisting glyphs in the target ranges are automatically skipped. Version 1.0 does not generate glyphs in the *Medieval and Renaissance*, *Daseian notation* or *Chord diagrams* ranges.

**Beware:** Script will decompose any components in the reference glyphs before generating new glyphs.

### set_smufl_names.py
his script retrieves discriptive SMuFL names from the latest published glyphnames.json metadata file published at the SMuFL repository, and adds them to the Note field of the glyphs at the corresponding codepoint.

**Note:** This is a modified version of Ben Timms's script **annotate_glyphs_with_smufl_names**, available at the SMuFL repository.

### smufl_to_finale.py
Generates composite glyphs from the SMuFL PUA range in codepoints compatible with Finale's Maestro font for Mac & Windows, and alters metrics and registration to comply with the software. Any preexisting glyphs at appropriate codepoints are automatically skipped.

**Beware** that the script will decompose any components in the reference glyphs prior to generating new glyphs.

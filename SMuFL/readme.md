# FontLab Scripts for SMuFL
Python scripts to aide the creation of SMuFL fonts using FontLab Studio 5 and later.

## Summary of available scripts
### SMuFL_to_Finale.py
Generates composite glyphs from the SMuFL PUA range in codepoints compatible with Finale's Maestro font for Mac & Windows, and alters
metrics and registration to comply with the software.

Any preexisting glyphs at appropriate codepoints are automatically skipped.

**Beware** that the script will decompose any components in the reference glyphs prior to generating new glyphs.

Under the current version, FontLab will crash if you attempt to generate glyphs for both OS encodings at the same time. Therefore, please uncomment and recomment the appropriate line at the bottom of the script to chose different OS.

The script does not currently support horizontal shifting of components, necessary with respect to 'uniE0CE' (noteheadParenthesis).


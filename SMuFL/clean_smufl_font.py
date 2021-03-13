# FLM Clean SMuFL Font

# Description:
# Deletes any unencoded glyphs and glyphs without a valid SMuFL codepoint, i.e., outside
# the unicode ranges Private User Area (U+E000-U+F8FF), Musical Symbols (U+1D100-U+1D1FF) and
# the Musical Symbols part of Miscellaneous Symbols (u+2669-u+266F).

# Further exclusions can be added to list 'excluded_glyphs' below, which by default contains glyphs
# '.notdef' and 'space'.

# Beware:
# This script permanently deletes glyphs, and could, in the event of any software bugs or system
# flaws, result in unintended data loss.
# Use at your own risk!

# (c) 2021 by Knut Nergaard
# Use, modify and distribute as desired.


excluded_glyphs = ['.notdef', 'space', ]


f = fl.font

private_use = range(57344, 63743)
mus_symbols = range(119040, 119295)
misc_symbols = range(9833, 9839)

# Do two backwards passes over all glyphs in font to prevent break.
for _ in range(2):
    for i in range(len(f.glyphs) - 1, -1, -1):
        g = f.glyphs[i]
        # Find glyph index from name.
        g_indx = f.FindGlyph(g.name)
        # Delete everything but:
        if (g_indx > -1 and g.unicode not in private_use and g.unicode not in mus_symbols and
                g.unicode not in misc_symbols and g.name not in excluded_glyphs):
            print('deleting: {}'.format(g.name))
            del fl.font.glyphs[g_indx]

fl.UpdateFont(fl.ifont)

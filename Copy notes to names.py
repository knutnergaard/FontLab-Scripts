#FLM: Copy Notes to Glyph Names

# Description:
# Renames glyphs with AGLFN names (uniXXXX)
# to SMuFL names in FLs "Note" field

# Credits:
# Knut Nergaard

from FL import *

if fl.font is None:
	raise Exception ("You must open a font first.")

# Get glyph with unicode name
f = fl.font
gs = f.glyphs

# Rename glyphs to note name
for g in gs:
    if "uni" in g.name:
    	print "Renaming: " + g.name
    	if g.note is None:
    		print ("Skipped: Note empty")
    	else:
    		g.name = str(g.note)
print "Done"

fl.UpdateFont(fl.ifont)
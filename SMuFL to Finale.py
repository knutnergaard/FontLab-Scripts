#FLM: SMuFL to Finale

# Version 1.0

# Description:
# Generates composite glyphs from the SMuFL PUA range in codepoints 
# compatible with Finale's Maestro font for Mac & Windows, and alters 
# metrics and registration to comply with the software. 

# Glyphs with Preexisting composite glyphs at appropriate codepoints
# are automatically skipped.


# CAUTION! 
# Script will decompose any components in the reference glyphs
# prior to generating new glyphs.

# FontLab will crash if you attempt to generate glyphs for both OS
# encodings at the same time. Therefore, please uncomment and recomment
# the appropriate line at the bottom of the script to chose different OS.


# Note:
# Script does not support horizontal shifting of components, necessary
# with respect to 'uniE0CE' (noteheadParenthesis).


# Credits:
# Knut Nergaard


# Please enter either Mac or Windows


print "Starting ..."

from FL import *


# List of glyphs to generate 
# (SMuFL name, Windows name, Mac name, Mac unicode index)
genList = {
'uniE01A': ('uniF03D', 'equal', 61, 0),
'uniE022': ('uniF05F', 'underscore', 95, 0),
'uniE030': ('uniF05C', 'backslash', 92, 0),
'uniE036': ('uniF0F1', 'Ograve', 210, 0),
'uniE047': ('uniF025', 'percent', 37, 0),
'uniE048': ('uniF0DE', 'fi', 64257, 0),
'uniE04A': ('uniF09F', 'udieresis', 252, 0),
'uniE050': ('uniF026', 'ampersand', 38, 0),
'uniE052': ('uniF056', 'V', 86, 0),
'uniE053': ('uniF0A0', 'dagger', 8224, 0),
'uniE05C': ('uniF042', 'B', 66, 0),
'uniE062': ('uniF03F', 'question', 63, 0),
'uniE064': ('uniF074', 't', 116, 0),
'uniE065': ('uniF0E6', 'Ecircumflex', 202, 0),
'uniE069': ('uniF08B', 'atilde', 227, 'bottom'),
'uniE069.salt01': ('uniF02F', 'slash', 47, -250),
'uniE06A': ('uniF0D6', 'divide', 247, 0),
'uniE080': ('uniF030', 'zero', 48, 0),
'uniE081': ('uniF031', 'one', 49, 0),
'uniE082': ('uniF032', 'two', 50, 0),
'uniE083': ('uniF033', 'three', 51, 0),
'uniE084': ('uniF034', 'four', 52, 0),
'uniE085': ('uniF035', 'five', 53, 0),
'uniE086': ('uniF036', 'six', 54, 0),
'uniE087': ('uniF037', 'seven', 55, 0),
'uniE088': ('uniF038', 'eight', 56, 0),
'uniE089': ('uniF039', 'nine', 57, 0),
'uniE08A': ('uniF063', 'c', 99, 0),
'uniE08B': ('uniF043', 'C', 67, 0),
'uniE08C': ('uniF0F6', 'circumflex', 710, 0),
'uniE0A0': ('uniF057', 'W', 87, 0),
'uniE0A0.salt01': ('uniF087', 'aacute', 225, 0),
'uniE0A1': ('uniF0DD', 'guilsinglright', 8250, 0),
'uniE0A2': ('uniF077', 'w', 119, 0),
'uniE0A3': ('uniF0FA', 'dotaccent', 729, 0),
'uniE0A4': ('uniF0CF', 'oe', 339, 0),
'uniE0A9': ('uniF0C0', 'questiondown', 191, 0),
'uniE0B8': ('uniF0AD', 'notequal', 8800, 0),
'uniE0B9': ('uniF0D0', 'endash', 8211, 0),
'uniE0BD': ('uniF079', 'y', 121, 0),
'uniE0BE': ('uniF0D1', 'emdash', 8212, 0),
'uniE0BF': ('uniF0E7', 'Aacute', 193, 0),
'uniE0C1': ('uniF06C', 'l', 108, 0),
'uniE0C6': ('uniF0C6', 'Delta', 8710, 0),
'uniE0C7': ('uniF0E0', 'daggerdbl', 8225, 0),
'uniE0CA': ('uniF059', 'Y', 89, 0),
'uniE0CE': ('uniF07D', 'braceright', 125, 'zeroWidth'),
'uniE0D9': ('uniF04F', 'O', 79, 0),
'uniE0DB': ('uniF0E2', 'quotesinglbase', 8218, 0),
'uniE0DD': ('uniF0E1', 'periodcentered', 183, 0),
'uniE0DE': ('uniF0B4', 'yen', 165, 0),
'uniE0F5': ('uniF028', 'parenleft', 40, 'bottomHalf'),
'uniE0F6': ('uniF029', 'parenright', 41, 'bottomHalf'),
'uniE100': ('uniF0CB', 'Agrave', 192, 0),
'uniE101': ('uniF0D5', 'quoteright', 8217, -250),
'uniE102': ('uniD0DA', 'fraction', 8260, -250),
'uniE104': ('uniF07C', 'bar', 124, 'bottom'),
'uniE105': ('uniF0F3', 'Ucircumflex', 219, 0),
'uniE1D3': ('uniF068', 'h', 104, -125),
'uniE1D4': ('uniF048', 'H', 72, -125),
'uniE1D5': ('uniF071', 'q', 113, -125),
'uniE1D6': ('uniF051', 'Q', 81, -125),
'uniE1D7': ('uniF065', 'e', 101, -125),
'uniE1D8': ('uniF045', 'E', 69, -125),
'uniE1D9': ('uniF078', 'x', 120, -125),
'uniE1DA': ('uniF058', 'X', 88, -125),
'uniE1E7': ('uniF02E', 'period', 46, 'bottomHalf'),
'uniE220': ('uniF021', 'exclam', 33, 'bottom'),
'uniE221': ('uniF040', 'at', 64, 'bottom'),
'uniE222': ('uniF0BE', 'ae', 230, 'bottom'),
'uniE240': ('uniF06A', 'j', 106, -250),
'uniE240.salt01': ('uniF0FB', 'ring', 730, 0),
'uniE240.ss02': ('uniF091', 'edieresis', 235, -250),
'uniE241': ('uniF04A', 'J', 74, 250),
'uniE241.salt01': ('uniF0F0', 'apple', 63743, 250),
'uniE241.ss02': ('uniF093', 'igrave', 236, 250),
'uniE242': ('uniF072', 'r', 114, -250),
'uniE242.ss02': ('uniF090', 'ecircumflex', 234, -250),
'uniE243': ('uniF052', 'R', 82, 250),
'uniE243.ss02': ('uniF092', 'iacute', 237, 250),
'uniE250': ('uniF04B', 'K', 75, -250),
'uniE251': ('uniF0EF', 'Ocircumflex', 212, 250),
'uniE260': ('uniF062', 'b', 98, 0),
'uniE261': ('uniF06E', 'n', 110, 0),
'uniE262': ('uniF023', 'numbersign', 35, 0),
'uniE263': ('uniF0DC', 'guilsinglleft', 8249, 0),
'uniE264': ('uniF0BA', 'integral', 8747, 0),
'uniE26A_uniE260_uniE26B': ('uniF041', 'A', 65, 0),
'uniE26A_uniE261_uniE26B': ('uniF04E', 'N', 78, 0),
'uniE26A_uniE262_uniE26B': ('uniF061', 'a', 97, 0),
'uniE26A_uniE263_uniE26B': ('uniF081', 'Aring', 197, 0),
'uniE26A_uniE264_uniE26B': ('uniF08C', 'aring', 229, 0),
'uniE47E': ('uniF024', 'dollar', 36, 0),
'uniE47F': ('uniF0F5', 'dotlessi', 305, 0),
'uniE4A0': ('uniF03E', 'greater', 62, 0),
'uniE4A2': ('uniF06B', 'k', 107, 0),
'uniE4A4': ('uniF02D', 'hyphen', 45, 0),
'uniE4A6': ('uniF0AE', 'AE', 198, 0),
'uniE4A7': ('uniF027', 'quotesingle', 39, 'bottom'),
'uniE4A8': ('uniF0AB', 'acute', 180, 0),
'uniE4A9': ('uniF0D8', 'ydieresis', 255, 'bottom'),
'uniE4AC': ('uniF05E', 'asciicircum', 94, 0),
'uniE4AD': ('uniF076', 'v', 118, 'bottom'),
'uniE4AE': ('uniF0AC', 'dieresis', 168, 0),
'uniE4AF': ('uniF0E8', 'Edieresis', 203, 'bottom'),
'uniE4B0': ('uniF0F9', 'breve', 728, 0),
'uniE4B1': ('uniF0DF', 'fl', 64258, 'bottom'),
'uniE4B2': ('uniF0F8', 'macron', 175, 0),
'uniE4B3': ('uniF03C', 'less', 60, 'bottom'),
'uniE4B4': ('uniF08A', 'adieresis', 228, 0),
'uniE4B5': ('uniF089', 'acircumflex', 226, 'bottom'),
'uniE4C0': ('uniF055', 'U', 85, 0),
'uniE4C1': ('uniF075', 'u', 117, 0),
'uniE4CE': ('uniF02C', 'comma', 44, 0),
'uniE4CF': ('uniF085', 'Odieresis', 214, 0),
'uniE4D1': ('uniF022', 'quotedbl', 34, 0),
'uniE4E2': ('uniF0E3', 'quotedblbase', 8222, 0),
'uniE4E3': ('uniF0B7', 'summation', 8721, -250),
'uniE4E4': ('uniF0EE', 'Oacute', 211, 0),
'uniE4E5': ('uniF0CE', 'OE', 338, 0),
'uniE4E6': ('uniF0E4', 'perthousand', 8240, 0),
'uniE4E7': ('uniF0C5', 'approxequal', 8776, 0),
'uniE4E8': ('uniF0A8', 'registered', 174, 0),
'uniE4E9': ('uniF0F4', 'Ugrave', 217, -250),
'uniE4EA': ('uniF0E5', 'Acircumflex', 194, -250),
'uniE500': ('uniF0D4', 'quoteleft', 8216, -250),
'uniE501': ('uniF0C7', 'guillemotleft', 171, -250),
'uniE510': ('uniF083', 'Eacute', 201, 125),
'uniE511': ('uniF0C3', 'radical', 8730, 125),
'uniE514': ('uniF086', 'Udieresis', 220, 125),
'uniE515': ('uniF0DB', 'currency', 164, 125),
'uniE51C': ('uniF0D7', 'lozenge', 9674, 125),
'uniE51D': ('uniF060', 'grave', 96, 125),
'uniE520': ('uniF070', 'p', 112, 0),
'uniE521': ('uniF0BD', 'Omega', 8486, 0),
'uniE522': ('uniF066', 'f', 102, 0),
'uniE523': ('uniF08E', 'eacute', 233, 0),
'uniE524': ('uniF073', 's', 115, 0),
'uniE525': ('uniF07A', 'z', 122, 0),
'uniE526': ('uniF096', 'ntilde', 241, 0),
'uniE529': ('uniF0AF', 'Oslash', 216, 0),
'uniE52A': ('uniF0B8', 'product', 8719, 0),
'uniE52B': ('uniF0B9', 'pi', 960, 0),
'uniE52C': ('uniF050', 'P', 80, 0),
'uniE52D': ('uniF046', 'F', 70, 0),
'uniE52F': ('uniF0C4', 'florin', 402, 0),
'uniE530': ('uniF0EC', 'Idieresis', 207, 0),
'uniE531': ('uniF0EB', 'Icircumflex', 206, 0),
'uniE534': ('uniF0EA', 'Iacute', 205, 0),
'uniE535': ('uniF05A', 'Z', 90, 0),
'uniE536': ('uniF053', 'S', 83, 0),
'uniE537': ('uniF082', 'Ccedilla', 199, 0),
'uniE538': ('uniF0B6', 'partialdiff', 8706, 0),
'uniE539': ('uniF0A7', 'germandbls', 223, 0),
'uniE53B': ('uniF08D', 'ccedilla', 231, 0),
'uniE560': ('uniF0C9', 'ellipsis', 8230, 0),
'uniE562': ('uniF03B', 'semicolon', 59, 0),
'uniE563': ('uniF03A', 'colon', 58, 0),
'uniE566': ('uniF0D9', 'Ydieresis', 376, 'center'),
'uniE567': ('uniF054', 'T', 84, 'center'),
'uniE56C': ('uniF06D', 'm', 109, 0),
'uniE56D': ('uniF04D', 'M', 77, 0),
'uniE56E': ('uniF0B5', 'mu', 181, 0),
'uniE5E5': ('uniF02B', 'plus', 43, 'center'),
'uniE5E7': ('uniF04C', 'L', 76, 'center'),
'uniE610': ('uniF0B3', 'greaterequal', 8805, 0),
'uniE612': ('uniF0B2', 'lessequal', 8804, 0),
'uniE614': ('uniF06F', 'o', 111, 'center'),
'uniE650': ('uniF0A1', 'degree', 176, 0),
'uniE655': ('uniF02A', 'asterisk', 42, 0),
'uniE870': ('uniF0F7', 'tilde', 732, '?'),
'uniE871': ('uniF0BF', 'oslash', 248, '?'),
'uniE872': ('uniF084', 'Ntilde', 209, 0),
'uniE880': ('uniF0BC', 'ordmasculine', 186, 0),
'uniE881': ('uniF0C1', 'exclamdown', 161, 0),
'uniE882': ('uniF0AA', 'trademark', 8482, 0),
'uniE883': ('uniF0A3', 'sterling', 163, 0),
'uniE884': ('uniF0A2', 'cent', 162, 0),
'uniE885': ('uniF0B0', 'infinity', 8734, 0),
'uniE886': ('uniF0A4', 'section', 167, 0),
'uniE887': ('uniF0A6', 'paragraph', 182, 0),
'uniE888': ('uniF0A5', 'bullet', 8226, 0),
'uniE889': ('uniF0BB', 'ordfeminine', 170, 0),
'uniE88A': ('uniF088', 'agrave', 224, 0),
'uniEAA4': ('uniF07E', 'asciitilde', 126, 'uniE566')}

# Get the Font
f = fl.font


# Check & decompose
print 'Checking source material ...'
for smuflName in genList:
	if not f.has_key(smuflName):
		print smuflName + ' is missing'
		
for g in f.glyphs:
	if g.name in genList and len(g.components) > 0:
		g.Decompose()
		print 'Decomposing: ' + g.name

# OS dependent Unicode Index definition
def uIndx(osName):
	if 'uni' in osName:
		return int(osName[3:], 16)
	else:
		return macUI


# Main process definition
def generateGlyphs(osName):
					
	smuflIndx = f.FindGlyph(smuflName)
	smuflGlyph = f.glyphs[smuflIndx]
	newGlyph = Glyph()
	newGlyph.name = osName
	newGlyph.unicode = uIndx(osName)
	newGlyph.mark = 120
	bBox = smuflGlyph.GetBoundingRect()
	bBoxBottom = bBox.ll.y
	bBoxTop = bBox.ur.y
	bBoxCenter = (bBoxBottom + bBoxTop)/2
	offset = 0
	if metricsMod == 'bottom':
		offset = -int(bBoxBottom)
	elif metricsMod == 'top':
		offset = -int(bBoxTop)
	elif metricsMod == 'center':
		offset = -int(bBoxCenter)
	elif metricsMod == 'bottomHalf':
		offset = -int(bBoxBottom - bBoxCenter/2)
# elif 'uni' in str(metricsMod):
	elif metricsMod is not str(metricsMod):
		offset = int(metricsMod)
	
	if f.has_key(osName):
		print 'Skipping prexisting glyph: ' + (osName)
	else:
		newGlyph.components.append(Component(smuflIndx, Point(0,offset)))
 
# Set metrics
		metrics = smuflGlyph.GetMetrics()
		if metricsMod == 'zeroWidth':
			metrics.x = bBox.width
		newGlyph.SetMetrics(metrics)
			
			
		f.glyphs.append(newGlyph)
		
		
# Execute definitions
print 'Creating new glyphs ...'
for smuflName, (winName, macName, macUI, metricsMod) in genList.iteritems():
# Uncomment one line at a time only.
		generateGlyphs(macName)
#		generateGlyphs(winName)
	else:
		print 'Please enter either Mac or Windows

fl.UpdateFont(fl.ifont)

print 'All done!'


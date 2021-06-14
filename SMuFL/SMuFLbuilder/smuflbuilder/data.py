"""Datamodule for SMuFLbuilder.

Contains all glyphdata, except for a few special, hard-coded cases currently
implemented.

Except for datasets involving ligatures and special characters,
the sets below are dictionaries with parent: child or child: parent
relationship (depending on practicality).
"""

# (c) 2021 by Knut Nergaard.


# pylint: disable=invalid-name

# Ranges ======================================================================

ranges = {
    'staves': 'Staves (U+E010-U+E02F)',
    'barlines': 'Barlines (U+E030-U+E03F)',
    'repeats': 'Repeats (U+E040-U+E04F)',
    'time': 'Time signatures (U+E080-U+E09F)',
    'indv notes': 'Individual notes (U+E1D0-U+E1EF)',
    'beamed notes': 'Beamed groups of notes (U+E1F0-U+E20F)',
    'stems': 'Stems (U+E210-U+E21F)',
    'tremolos': 'Tremolos (U+E220-U+E23F)',
    'flags': 'Flags (U+E240-U+E25F)',
    'octaves': 'Octaves (U+E510-U+E51F)',
    'dynamics': 'Dynamics (U+E520-U+E54F)',
    # 'Common ornaments (U+E560-U+E56F)',
    # 'Other baroque ornaments (U+E570-U+E58F)',
    # 'Precomposed trills and mordents: (U+E5B0-U+E5CF)',
    'accordion': 'Accordion (U+E8A0-U+E8DF)',
    'time sup': 'Time signatures supplement (U+EC80-U+EC8F)',
    'octaves sup': 'Octaves supplement (U+EC90-U+EC9F)',
    'turned time': 'Turned time signatures (U+ECE0-U+ECEF)',
    'reversed time': 'Reversed time signatures (U+ECF0-U+ECFF)',
}

# Barlines and Repeats ========================================================

barlines = {
    # barlineDouble
    'uniE031': ('uniE030', 'uniE030'),
    # barlineFinal
    'uniE032': ('uniE030', 'uniE034'),
    # barlineReverseFinal
    'uniE033': ('uniE034', 'uniE030'),
    # barlineHeavyHeavy
    'uniE035': ('uniE034', 'uniE034'),
    #  barlineDashed, barlineDotted, barlineShort, barlineTick
    None: ('uniE036', 'uniE037', 'uniE038', 'uniE039'),
}

repeat_barlines = {
    # repeatLeft
    'uniE040': ('uniE034', 'uniE030', 'uniE044', 'uniE044'),
    # repeatRight
    'uniE041': ('uniE044', 'uniE044', 'uniE030', 'uniE034'),
    # repeatRightLeft
    'uniE042': ('uniE044', 'uniE044', 'uniE030', 'uniE034',
                'uniE030', 'uniE044', 'uniE044'),
    # Repeat dots
    'uniE043': ('uniE044', 'uniE044'),
}

repeat_barlines_alt = {
    # repeatRightLeftThick
    'uniE042.salt01': ('uniE044', 'uniE044', 'uniE034',
                       'uniE034', 'uniE044', 'uniE044')
}

# Staves ======================================================================

staves = {
    # parent : (children)
    # staffLine
    'uniE010': ('uniE011', 'uniE012', 'uniE013', 'uniE014', 'uniE015'),
    # staffLineWide
    'uniE016': ('uniE017', 'uniE018', 'uniE019', 'uniE01A', 'uniE01B'),
    # staffLineNarrow
    'uniE01C': ('uniE01D', 'uniE01E', 'uniE01F', 'uniE020', 'uniE021'),
    # legerLine
    'uniE022': None,
    # legerLineWide
    'uniE023': None,
    # legerLineNarrow
    'uniE024': None,
}

# Time signatures =============================================================

time_fractions = {
    #  child:  (numerator,   slash,  denominator)
    'uniE097': ('uniE081', 'uniE08E', 'uniE084'),
    'uniE098': ('uniE081', 'uniE08E', 'uniE082'),
    'uniE099': ('uniE083', 'uniE08E', 'uniE084'),
    'uniE09A': ('uniE081', 'uniE08E', 'uniE083'),
    'uniE09B': ('uniE082', 'uniE08E', 'uniE083'),
}

cut_time_common = {'uniE08A': 'uniE08B'}

cut_time_sup = {'uniE082': 'uniEC85', 'uniE083': 'uniEC86'}

turned_time = {
    'uniE080': 'uniECE0', 'uniE081': 'uniECE1',
    'uniE082': 'uniECE2', 'uniE083': 'uniECE3',
    'uniE084': 'uniECE4', 'uniE085': 'uniECE5',
    'uniE086': 'uniECE6', 'uniE087': 'uniECE7',
    'uniE088': 'uniECE8', 'uniE089': 'uniECE9',
    'uniE08A': 'uniECEA', 'uniE08B': 'uniECEB',
}

reversed_time = {
    'uniE080': 'uniECF0', 'uniE081': 'uniECF1',
    'uniE082': 'uniECF2', 'uniE083': 'uniECF3',
    'uniE084': 'uniECF4', 'uniE085': 'uniECF5',
    'uniE086': 'uniECF6', 'uniE087': 'uniECF7',
    'uniE088': 'uniECF8', 'uniE089': 'uniECF9',
    'uniE08A': 'uniECFA', 'uniE08B': 'uniECFB',
}

time_ligatures = (
    'uniE09F_uniE080', 'uniE09E_uniE080', 'uniE09F_uniE081', 'uniE09E_uniE081',
    'uniE09F_uniE082', 'uniE09E_uniE082', 'uniE09F_uniE083', 'uniE09E_uniE083',
    'uniE09F_uniE084', 'uniE09E_uniE084', 'uniE09F_uniE085', 'uniE09E_uniE085',
    'uniE09F_uniE086', 'uniE09E_uniE086', 'uniE09F_uniE087', 'uniE09E_uniE087',
    'uniE09F_uniE088', 'uniE09E_uniE088', 'uniE09F_uniE089', 'uniE09E_uniE089',
    'uniE09E_uniE082_uniE09F_uniE084', 'uniE09E_uniE082_uniE09F_uniE082',
    'uniE09E_uniE083_uniE09F_uniE082', 'uniE09E_uniE083_uniE09F_uniE084',
    'uniE09E_uniE083_uniE09F_uniE088', 'uniE09E_uniE084_uniE09F_uniE084',
    'uniE09E_uniE085_uniE09F_uniE084', 'uniE09E_uniE085_uniE09F_uniE088',
    'uniE09E_uniE086_uniE09F_uniE084', 'uniE09E_uniE086_uniE09F_uniE088',
    'uniE09E_uniE087_uniE09F_uniE088', 'uniE09E_uniE089_uniE09F_uniE088',
    'uniE09E_uniE081_uniE09E_uniE082_uniE09F_uniE088',
)

ctrl_char = {'uniE09E', 'uniE09F'}


# Notes =======================================================================

stems = {
    # child:  parent
    None: 'uniE210',       # stem
    'uniE211': 'uniE645',  # stemSprechgesang
    'uniE212': 'uniE808',  # stemSwished
    'uniE213': 'uniE22B',  # stemPendereckiTremolo
    'uniE214': 'uniE618',  # stemSulPonticello
    'uniE215': 'uniE619',  # stemBowOnBridge
    'uniE216': 'uniE61A',  # stemBowOnTailpiece
    'uniE217': 'uniE22A',  # stemBuzzRoll
    'uniE218': 'uniE63B',  # stemDamp
    'uniE219': 'uniE623',  # stemVibratoPulse
    'uniE21A': 'uniE607',  # stemMultiphonicsBlack
    'uniE21B': 'uniE608',  # stemMultiphonicsWhite
    'uniE21C': 'uniE609',  # stemMultiphonicsBlackWhite
    'uniE21D': 'uniE646',  # stemSussurando
    'uniE21E': 'uniE263',  # stemRimShot
    'uniE21F': 'uniE694',   # stemHarpStringNoise
}


flags = {
    'uniE244': ('uniE242', 'uniE250'),
    'uniE245': ('uniE243', 'uniE251'),
    'uniE246': ('uniE242', 'uniE250', 'uniE250'),
    'uniE247': ('uniE243', 'uniE251', 'uniE251'),
    'uniE248': ('uniE242', 'uniE250', 'uniE250', 'uniE250'),
    'uniE249': ('uniE243', 'uniE251', 'uniE251', 'uniE251'),
    'uniE24A': ('uniE242', 'uniE250', 'uniE250', 'uniE250', 'uniE250'),
    'uniE24B': ('uniE243', 'uniE251', 'uniE251', 'uniE251', 'uniE251'),
    'uniE24C': ('uniE242', 'uniE250', 'uniE250',
                'uniE250', 'uniE250', 'uniE250'),
    'uniE24D': ('uniE243', 'uniE251', 'uniE251',
                'uniE251', 'uniE251', 'uniE251'),
    'uniE24E': ('uniE242', 'uniE250', 'uniE250',
                'uniE250', 'uniE250', 'uniE250', 'uniE250'),
    'uniE24F': ('uniE243', 'uniE251', 'uniE251',
                'uniE251', 'uniE251', 'uniE251', 'uniE251'),
}

indv_notes = {
    'uniE1D0': ('uniE0A0',),  # noteDoubleWhole
    'uniE1D1': ('uniE0A1',),  # noteDoubleWholeSquare
    'uniE1D2': ('uniE0A2',),  # noteWhole
    'uniE1D3': ('uniE0A3', 'uniE210'),  # noteHalfUp
    'uniE1D4': ('uniE0A3', 'uniE210'),  # noteHalfDown
    'uniE1D5': ('uniE0A4', 'uniE210'),  # noteQuarterUp
    'uniE1D6': ('uniE0A4', 'uniE210'),  # noteQuarterDown
    'uniE1D7': ('uniE0A4', 'uniE210', 'uniE240'),  # note8thUp
    'uniE1D8': ('uniE0A4', 'uniE210', 'uniE241'),  # note8thDown
    'uniE1D9': ('uniE0A4', 'uniE210', 'uniE242'),  # note16thUp
    'uniE1DA': ('uniE0A4', 'uniE210', 'uniE243'),  # note16ndDown
    'uniE1DB': ('uniE0A4', 'uniE210', 'uniE242', 'uniE250'),  # note32ndUp
    'uniE1DC': ('uniE0A4', 'uniE210', 'uniE243', 'uniE251'),  # note32ndDown
    'uniE1DD': ('uniE0A4', 'uniE210',
                'uniE242', 'uniE250', 'uniE250'),  # note32ndUp
    'uniE1DE': ('uniE0A4', 'uniE210',
                'uniE243', 'uniE251', 'uniE251'),  # note32ndDown
    'uniE1DF': ('uniE0A4', 'uniE210', 'uniE242',
                'uniE250', 'uniE250', 'uniE250'),  # note32ndUp
    'uniE1E0': ('uniE0A4', 'uniE210', 'uniE243',
                'uniE251', 'uniE251', 'uniE251'),  # note32ndDown
    'uniE1E1': ('uniE0A4', 'uniE210', 'uniE242',
                'uniE250', 'uniE250', 'uniE250', 'uniE250'),  # note64ndUp
    'uniE1E2': ('uniE0A4', 'uniE210', 'uniE243',
                'uniE251', 'uniE251', 'uniE251', 'uniE251'),  # note64ndDown
    'uniE1E3': ('uniE0A4', 'uniE210', 'uniE242', 'uniE250',
                'uniE250', 'uniE250', 'uniE250', 'uniE250'),  # note128ndUp
    'uniE1E4': ('uniE0A4', 'uniE210', 'uniE243', 'uniE251',
                'uniE251', 'uniE251', 'uniE251', 'uniE251'),  # note128ndDown
    'uniE1E5': ('uniE0A4', 'uniE210', 'uniE242', 'uniE250', 'uniE250',
                'uniE250', 'uniE250', 'uniE250', 'uniE250'),  # note256ndUp
    'uniE1E6': ('uniE0A4', 'uniE210', 'uniE243', 'uniE251', 'uniE251',
                'uniE251', 'uniE251', 'uniE251', 'uniE251'),  # note256ndDown
    None: ('uniE1E7',),
}

indv_notes_alt = {'uniE1D0.salt01': ('uniE0A0.salt01',)}


beamed_notes = {
    'uniE1F0': ('uniE204', 'uniE0A4'),
    'uniE1F1': ('uniE205', 'uniE0A4'),
    'uniE1F2': ('uniE204', 'uniE0A4', 'uniE1F7'),
    'uniE1F3': ('uniE205', 'uniE0A4', 'uniE1F7'),
    'uniE1F4': ('uniE204', 'uniE0A4', 'uniE1F7', 'uniE1F7'),
    'uniE1F5': ('uniE205', 'uniE0A4', 'uniE1F7', 'uniE1F7'),
    'uniE1F6': ('uniE205', 'uniE0A4', 'uniE1F7', 'uniE1F7', 'uniE1F7'),
    'uniE1F8': (None, None, 'uniE1F7'),
    'uniE1F9': (None, None, 'uniE1F7', 'uniE1F7'),
    'uniE1FA': (None, None, 'uniE1F7', 'uniE1F7'),
    'uniE1FB': (None, None, 'uniE1F7', 'uniE1F7', 'uniE1F7'),
    'uniE1FC': (None, None, 'uniE1E7'),
    'uniE1FF': ('uniE883',),
    'uniE200': ('uniE1FE',),
    'uniE201': ('uniE1FE',),
    'uniE202': ('uniE883',),
    'uniE203': ('uniE1FE',),
    'uniE206': (None, 'uniE204', 'uniE1F7'),
    'uniE207': (None, 'uniE205', 'uniE1F7'),
    'uniE208': (None, 'uniE204', 'uniE1F7', 'uniE1F7'),
    'uniE209': (None, 'uniE205', 'uniE1F7', 'uniE1F7'),
    'uniE20A': (None, 'uniE205', 'uniE1F7', 'uniE1F7', 'uniE1F7'),
}

# Tremolos ====================================================================

tremolos = {
    # parent:  (children)
    'uniE220': ('uniE221', 'uniE222', 'uniE223', 'uniE224'),
    # regular tremoli
    'uniE225': ('uniE226', 'uniE227', 'uniE228', 'uniE229'),
    # fingered tremoli
    'uniE4A2': ('uniE22E', 'uniE22F', 'uniE230', 'uniE231'),
    # divisi dots
}

# Ornaments ===================================================================

common_ornaments = {
    'uniE560': ('uniE0A4', 'uniE210', 'uniE240', 'uniE564'),
    'uniE561': ('uniE0A4', 'uniE210', 'uniE241', 'uniE564'),
    'uniE568': ('uniE567',),
    'uniE569': ('uniE567', 'ornamentTurnVerticalStroke'),
    'uniE56B': ('uniE56A',),
    'uniE56C': ('uniE59D', 'uniE59E'),
    'uniE56D': ('uniE59D', 'uniE59F', 'uniE59E'),
    'uniE56E': ('uniE59D', 'uniE59F', 'uniE59F',),
}

other_ornaments = {
    'uniE572': ('uniE571',),
    'uniE574': ('uniE573',),
    'uniE576': ('uniE575',),
    'uniE578': ('uniE577',),
    'uniE586': ('uniE585',),
}

precomp_ornaments = {
    'uniE5B0': ('uniE59D', 'uniE5A2'),
    'uniE5B1': ('uniE59D', 'uniE59D', 'uniE5A8'),
    'uniE5B2': ('uniE594', 'uniE59E', 'uniE59D'),
    'uniE5B3': ('uniE594', 'uniE5A4'),
    'uniE5B4': ('uniE593', 'uniE59D', 'uniE5A0'),
    'uniE5B5': ('uniE59B', 'uniE59D', 'uniE59E'),
    'uniE5B6': ('uniE59B', 'uniE59D', 'uniE5A1'),
    'uniE5B7': ('uniE593', 'uniE59D', 'uniE59D', 'uniE59F', 'uniE59E'),
    'uniE5B8': ('uniE59A', 'uniE59E', 'uniE59F', 'uniE59D'),
    'uniE5B9': ('uniE59C', 'uniE5A0'),
    'uniE5BA': ('uniE59C', 'uniE5A1'),
    'uniE5BB': ('uniE59D', 'uniE59D', 'uniE5A1'),
    'uniE5BC': ('uniE598', 'uniE59E', 'uniE59F', 'uniE59D', 'uniE59D'),
    'uniE5BD': ('uniE59D', 'uniE59D', 'uniE59F', 'uniE59E'),
    'uniE5BE': ('uniE592', 'uniE59E', 'uniE59D'),
    'uniE5BF': ('uniE592', 'uniE59D', 'uniE59F', 'uniE59E'),
    'uniE5C0': ('uniE592', 'uniE59E', 'uniE59D', 'uniE59D'),
    'uniE5C1': ('uniE599', 'uniE59E'),
    'uniE5C2': ('uniE599', 'uniE59E', 'uniE59F'),
    'uniE5C3': ('uniE599', 'uniE59E', 'uniE59D'),
    'uniE5C4': ('uniE599', 'uniE59D', 'uniE59F', 'uniE59E'),
    'uniE5C5': ('uniE59D', 'uniE5A1'),
    'uniE5C6': ('uniE591', 'uniE59E', 'uniE59D', 'uniE59D'),
    'uniE5C7': ('uniE591', 'uniE59D', 'uniE59D', 'uniE59E', 'uniE59F'),
    'uniE5C8': ('uniE59D', 'uniE59D', 'uniE5A7'),
}

liga_ornaments = (
    'uniE260_uniE566', 'uniE261_uniE566', 'uniE262_uniE566',
    'uniE260_uniE567', 'uniE260_uniE567_uniE262', 'uniE567_uniE260',
    'uniE261_uniE567', 'uniE567_uniE261', 'uniE262_uniE567',
    'uniE262_uniE567_uniE260', 'uniE567_uniE262'
)

# Octaves =====================================================================

octaves = {
    'uniE511': ('uniE510', 'uniEC97', 'uniEC91'),
    'uniE512': ('uniE510', 'uniEC97', 'uniEC91'),
    'uniE513': ('uniE510', 'uniEC93', 'uniEC91'),
    'uniE515': ('uniE514', 'uniEC95', 'uniEC91'),
    'uniE516': ('uniE514', 'uniEC95', 'uniEC91'),
    'uniE518': ('uniE517', 'uniEC95', 'uniEC91'),
    'uniE519': ('uniE517', 'uniEC95', 'uniEC91'),
    'uniE51C': ('uniE510', 'uniEC97', 'uniEC93'),
    'uniE51D': ('uniE514', 'uniEC95', 'uniEC93'),
    'uniE51E': ('uniE517', 'uniEC95', 'uniEC93'),
    'uniE51F': ('uniEC93', 'uniEC91', 'octaveS', 'octaveS', 'uniEC91'),
}

octaves_sup = {
    'uniEC90': ('octaveL', 'octaveO', 'octaveC', 'octaveO'),
    'uniEC92': ('uniEC91',),
    'uniEC94': ('uniEC93',),
    'uniEC96': ('uniEC95',),
    'uniEC98': ('uniEC97',),
}

octaves_alt = {
    'uniE515.salt01': ('uniE514.salt01', 'uniEC95', 'uniEC91'),
    'uniE516.salt01': ('uniE514.salt01', 'uniEC95', 'uniEC91'),
    'uniE518.salt01': ('uniE517.salt01', 'uniEC95', 'uniEC91'),
    'uniE519.salt01': ('uniE517.salt01', 'uniEC95', 'uniEC91'),
    'uniE51D.salt01': ('uniE514.salt01', 'uniEC95', 'uniEC93'),
    'uniE51E.salt01': ('uniE517.salt01', 'uniEC95', 'uniEC93'),
}

# Dynamics ====================================================================

dynamics = {
    # None: ('uniE53E',),  # hairpin
    None: ('uniE541',),  # niente circle
    'uniE527': ('uniE520',) * 6,
    'uniE528': ('uniE520',) * 5,
    'uniE529': ('uniE520',) * 4,
    'uniE52A': ('uniE520',) * 3,
    'uniE52B': ('uniE520',) * 2,
    'uniE52C': ('uniE521', 'uniE520'),
    'uniE52D': ('uniE521', 'uniE522'),
    'uniE52E': ('uniE520', 'uniE522'),
    'uniE52F': ('uniE522',) * 2,
    'uniE530': ('uniE522',) * 3,
    'uniE531': ('uniE522',) * 4,
    'uniE532': ('uniE522',) * 5,
    'uniE533': ('uniE522',) * 6,
    'uniE534': ('uniE522', 'uniE520'),
    'uniE535': ('uniE522', 'uniE525'),
    'uniE536': ('uniE524', 'uniE522'),
    'uniE537': ('uniE524', 'uniE522', 'uniE520'),
    'uniE538': ('uniE524', 'uniE522', 'uniE520', 'uniE520'),
    'uniE539': ('uniE524', 'uniE522', 'uniE525'),
    'uniE53A': ('uniE524', 'uniE522', 'uniE525', 'uniE520'),
    'uniE53B': ('uniE524', 'uniE522', 'uniE522', 'uniE525'),
    'uniE53C': ('uniE523', 'uniE522'),
    'uniE53D': ('uniE523', 'uniE522', 'uniE525'),
    'uniE53F': ('uniE53E',),
    'uniE540': ('uniE53E', 'uniE53E'),
}

# Accordion ===================================================================

accordion_ranks = {
    'uniE8C6': 3, 'uniE8C7': 4, 'uniE8C8': 2, 'uniE8C9': 3, 'uniE8CA': None
}

accordion_reg = {
    # child : (ranks,     placement)
    'uniE8A0': ('uniE8C6', 'stop4'),
    'uniE8A1': ('uniE8C6', 'stop8'),
    'uniE8A2': ('uniE8C6', 'upper8'),
    'uniE8A3': ('uniE8C6', 'lower8'),
    'uniE8A4': ('uniE8C6', 'stop16'),
    'uniE8A5': ('uniE8C6', 'stop4', 'stop8'),
    'uniE8A6': ('uniE8C6', 'stop8', 'upper8'),
    'uniE8A7': ('uniE8C6', 'stop4', 'stop8', 'upper8'),
    'uniE8A8': ('uniE8C6', 'lower8', 'stop8', 'upper8'),
    'uniE8A9': ('uniE8C6', 'stop4', 'stop16'),
    'uniE8AA': ('uniE8C6', 'stop4', 'stop8', 'stop16'),
    'uniE8AB': ('uniE8C6', 'stop8', 'stop16'),
    'uniE8AC': ('uniE8C6', 'stop8', 'upper8', 'stop16'),
    'uniE8AD': ('uniE8C6', 'stop4', 'lower8', 'upper8' 'stop16'),
    'uniE8AE': ('uniE8C6', 'lower8', 'upper8'),
    'uniE8AF': ('uniE8C6', 'lower8', 'upper8', 'stop16'),
    'uniE8B0': ('uniE8C6', 'stop4', 'lower8', 'upper8'),
    'uniE8B1': ('uniE8C6', 'lower8', 'stop8', 'upper8', 'stop16'),
    'uniE8B2': ('uniE8C6', 'stop4', 'lower8', 'stop8', 'upper8'),
    'uniE8B3': ('uniE8C6', 'stop4', 'lower8', 'stop8', 'upper8' 'stop16'),
    'uniE8B4': ('uniE8C7', 'soprano'),
    'uniE8B5': ('uniE8C7', 'soprano', 'alto'),
    'uniE8B6': ('uniE8C7', 'soprano', 'alto', 'tenor'),
    'uniE8B7': ('uniE8C7', 'soprano', 'alto', 'tenor', 'bass', 'master'),
    'uniE8B8': ('uniE8C7', 'tenor', 'bass', 'master'),
    'uniE8B9': ('uniE8C7', 'alto', 'tenor'),
    'uniE8BA': ('uniE8C7', 'soprano', 'alto', 'bass'),
    'uniE8BB': ('uniE8C8', 'stop8b'),
    'uniE8BC': ('uniE8C8', 'stop16b'),
    'uniE8BD': ('uniE8C8', 'stop8b', 'stop16b'),
    'uniE8BE': ('uniE8C8', 'master'),
    'uniE8BF': ('uniE8C8', 'stop16b', 'master'),
    'uniE8C0': ('uniE8C8', 'stop8b', 'stop16b', 'master'),
    'uniE8C1': ('uniE8C9', 'stop8c'),
    'uniE8C2': ('uniE8C9', 'stop2'),
    'uniE8C3': ('uniE8C9', 'double8stop'),
    'uniE8C4': ('uniE8C9', 'stop2' 'stop8c'),
    'uniE8C5': ('uniE8C9', 'stop2', 'left8stop', 'right8stop'),
}

# Other =======================================================================

do_not_decompose = {'uniE08B', }

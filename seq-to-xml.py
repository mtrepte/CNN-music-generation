from lxml import etree
"""
Takes an input sequence of characters, and outputs a musicXML file
Divisions=4, a single character represents a sixteenth
"""
char_ls = ['$', '%', '^', '&', '*', '(', ')',
			'~', '=', '+', '[', ']', '{', '}', '.', ',', '<', 
			'>', '?', '/', 'A', 'B', 'C', 'D', 'E', 'F', 
			'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
			'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
			'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
			'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
			'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', 
			'5', '6', '7', '8', '9', '0', ';', ':', '|']
key_ls = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
count = 0
octave = 0
char_dict = []
for char in char_ls:
    note = key_ls[count % len(key_ls)]
    if note == 'C':
        octave += 1
    char_dict.append((char, note + str(octave)))
    count += 1
char_dict = dict(char_dict)

class Symbol:
    def __init__(self, string):
        self.char_ls = string.split("-")
        self.duration = str(len(self.char_ls))
        self.symbol = self.to_symbol(self.duration)

    def to_symbol(self, duration):
        symbol = {
            '16': "whole",
            '12': "dhalf",
            '8': "half",
            '6': "dquarter",
            '4': "quarter",
            '3': "deighth",
            '2': "eighth",
            '1': "sixteenth"
        }.get(duration, "quarter") # quarter returned as default
        return symbol

    def to_xml(self, chord=False):
        """
        Defines basic structure of a note/chord symbol.
        """
        note = etree.Element("note")
        if chord:
            note.append(etree.Element("chord"))
        pitch = etree.SubElement(note, "pitch")
        step = etree.SubElement(pitch, "step")
        octave = etree.SubElement(pitch, "octave")
        dur = etree.SubElement(note, "duration")
        dur.text = self.duration
        symbol = etree.SubElement(note, "type")
        if self.symbol[0] == "d":
            symbol.text = self.symbol[1:]
            note.append(etree.Element("dot"))
        else:
            symbol.text = self.symbol
        return note

    def get_duration(self):
        return int(self.duration)

class Note(Symbol):
    """
    A single note. 
    On initialization, we pass through a string of the same character(s)
    separated by dashes.
    
    """
    def __init__(self, string):
        Symbol.__init__(self, string)
        self.note, self.octave = self.to_pitch(self.char_ls[0])

    def to_pitch(self, char):
        global char_dict
        symbol = char_dict[char]
        if len(symbol) == 2:
            return symbol[0], symbol[1]
        else:
            return symbol[:2], symbol[2]

    def to_xml(self, chord=False):
        note = Symbol.to_xml(self, chord)
        if chord:
            if len(self.note) == 1:
                note[1][0].text = self.note
                note[1][1].text = self.octave
            else:
                note[1][0].text = self.note[0]
                note[1][1].text = self.octave
                note[1].append(etree.Element("alter"))
                note[1][2].text = "1"
        else:
            if len(self.note) == 1:
                note[0][0].text = self.note
                note[0][1].text = self.octave
            else:
                note[0][0].text = self.note[0]
                note[0][1].text = self.octave
                note[0].append(etree.Element("alter"))
                note[0][2].text = "1"
        return note

class Rest(Symbol):
    """
    A single rest.
    """
    def __init__(self, string):
        Symbol.__init__(self, string)

    def to_xml(self):
        note = etree.Element("note")
        rest = etree.SubElement(note, "rest")
        dur = etree.SubElement(note, "duration")
        dur.text = self.duration
        symbol = etree.SubElement(note, "type")
        symbol.text = self.symbol
        return note

seq = open('output3.txt', 'r').read()
string_ls = seq.split(" ")

header = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!DOCTYPE score-partwise PUBLIC \"-//Recordare//DTD MusicXML 3.0 Partwise//EN\" \"http://www.musicxml.org/dtds/partwise.dtd\">\n"

root = etree.Element("score-partwise")

work = etree.SubElement(root, "work")
work_title = etree.SubElement(work, "work-title")
work_title.text = "Output"

part_list = etree.SubElement(root, "part-list")
score_part = etree.SubElement(part_list, "score-part", id="P1")
part_name = etree.SubElement(score_part, "part-name")
part_name.text = "Music"

part = etree.SubElement(root, "part", id="P1")
# Run through char_ls and generate measures
m1 = etree.SubElement(part, "measure", number="1")
attr = etree.SubElement(m1, "attributes")
div = etree.SubElement(attr, "divisions")
div.text = "4"
key = etree.SubElement(attr, "key")
fifths = etree.SubElement(key, "fifths")
fifths.text = "0"
time = etree.SubElement(attr, "time")
beats = etree.SubElement(time, "beats")
beats.text = "4"
beat_type = etree.SubElement(time, "beat-type")
beat_type.text = "4"
staves = etree.SubElement(attr, "staves")
staves.text = "2"
c1 = etree.SubElement(attr, "clef", number="1")
sign = etree.SubElement(c1, "sign")
sign.text = "G"
line = etree.SubElement(c1, "line")
line.text = "2"
c2 = etree.SubElement(attr, "clef", number="2")
sign = etree.SubElement(c2, "sign")
sign.text = "F"
line = etree.SubElement(c2, "line")
line.text = "4"

def rest_filler(remainder):
    rest_str = ""
    for i in range(remainder-1):
        rest_str += "!" + "-"
    rest_str += "!"
    return rest_str

def split_note(symbol, remainder):
    # Needs fixing
    fill_len = symbol.get_duration()-remainder
    s = symbol.char_ls[0]
    note_str1 = ""
    note_str2 = ""
    for i in range(fill_len-1):
        note_str1 += s + "-"
    note_str1 += s
    for j in range(remainder-1):
        note_str2 += s + "-"
    note_str2 += s
    return note_str1, note_str2

def chord_to_notes(chord, dur):
    """
    Returns list of individual notes of a chord
    """
    note_str = ""
    ls = []
    for note in chord:
        for i in range(dur-1):
            note_str += note + "-"
        note_str += note
        ls.append(note_str)
        note_str = ""
    print(ls)
    return ls

msr_dur = 16
curr_dur = 0
curr_msr = m1
curr_msr_num = 1
for i in range(len(string_ls)):
    # remove last measure tag
    sym_str = string_ls[i].strip()
    tmp = Symbol(sym_str)
    curr_dur += tmp.get_duration()
    if curr_dur == msr_dur:
        if tmp.char_ls[0] == "!": # rest
            sym = Rest(sym_str).to_xml()
            curr_msr.append(sym)
        elif len(tmp.char_ls[0]) == 1: # single note
            sym = Note(sym_str).to_xml()
            curr_msr.append(sym)
        else: # chord
            note_ls = chord_to_notes(tmp.char_ls[0], tmp.get_duration())
            sym = Note(note_ls[0]).to_xml()
            curr_msr.append(sym)
            for i in range(1, len(note_ls)):
                sym = Note(note_ls[i]).to_xml(chord=True)
                curr_msr.append(sym)
        # create new measure, reset curr_dur
        curr_msr_num += 1
        curr_msr = etree.SubElement(part, "measure", number=str(curr_msr_num))
        curr_dur = 0
    elif curr_dur < msr_dur:
        if tmp.char_ls[0] == "!": # rest
            sym = Rest(sym_str).to_xml()
            curr_msr.append(sym)
        elif len(tmp.char_ls[0]) == 1: # single note
            sym = Note(sym_str).to_xml()
            curr_msr.append(sym)
        else: # chord
            print(tmp.char_ls[0])
            note_ls = chord_to_notes(tmp.char_ls[0], tmp.get_duration())
            if len(note_ls) != 0:
                sym = Note(note_ls[0]).to_xml()
                curr_msr.append(sym)
                for i in range(1, len(note_ls)):
                    sym = Note(note_ls[i]).to_xml(chord=True)
                    curr_msr.append(sym)
    else: # split
        remainder = curr_dur-msr_dur
        str1, str2 = split_note(tmp, remainder)
        if tmp.char_ls[0] == "!":
            sym1 = Rest(str1).to_xml()
            curr_msr.append(sym1)
        elif len(tmp.char_ls[0]) == 1: # single note
            sym1 = Note(str1).to_xml()
            curr_msr.append(sym1)
        else: # chord
            tmp1 = Symbol(str1)
            note_ls = chord_to_notes(tmp1.char_ls[0], tmp1.get_duration())
            sym1 = Note(note_ls[0]).to_xml()
            curr_msr.append(sym1)
            for i in range(1, len(note_ls)):
                sym1 = Note(note_ls[i]).to_xml(chord=True)
                curr_msr.append(sym1)
        curr_msr_num += 1
        curr_msr = etree.SubElement(part, "measure", number=str(curr_msr_num))
        if tmp.char_ls[0] == "!":
            sym2 = Rest(str2).to_xml()
            curr_msr.append(sym2)
        elif len(tmp.char_ls[0]) == 1: # single note
            sym2 = Note(str2).to_xml()
            curr_msr.append(sym2)
        else: # chord
            tmp2 = Symbol(str2)
            note_ls = chord_to_notes(tmp2.char_ls[0], tmp2.get_duration())
            sym2 = Note(note_ls[0]).to_xml()
            curr_msr.append(sym2)
            for i in range(1, len(note_ls)):
                sym2 = Note(note_ls[i]).to_xml(chord=True)
                curr_msr.append(sym2)
        curr_dur = remainder
        curr_msr.append(sym2)
    if i == len(string_ls) - 1 and curr_dur != msr_dur:
        sym = Rest(rest_filler(msr_dur-curr_dur)).to_xml()
        curr_msr.append(sym)

file = open("output.xml", "w")
file.write(header + etree.tostring(root, pretty_print=True))

print(header + etree.tostring(root, pretty_print=True))

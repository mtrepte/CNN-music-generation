def vectorize(filename):
	file = open('standardized/' + filename,'r')
	lines = file.readlines()
	file.close()

	note_to_index = {'C':0, 'C_sharp':1, 'D':2, 'D_sharp':3, 'E':4, 'F':5, 'F_sharp':6,
						'G':7, 'G_sharp':8, 'A':9, 'A_sharp':10, 'B':11}
	in_note = False; in_chord = False; in_grace = False
	sequence = ''; chord_str = ''
	duration = 0; prev_duration = 0

	for line in lines:
		if '<note' in line:
			in_note = True
			in_chord = False
			has_alter = False
			in_grace = False

		if '<grace/>' in line:
			in_grace = True

		if not in_grace:
			if in_note:
				if '<chord/>' in line:
					in_chord = True
				if '<step>' and '</step>' in line:
					step = line.strip()[6:-7].strip()
				if '<alter>' and '</alter>' in line:
					has_alter = True
					step += '_sharp'
				if '<octave>' and '</octave>' in line:
					octave = int(line.strip()[8:-9].strip())
				if '<duration>' and '</duration>' in line:
					prev_duration = duration
					duration = int(line.strip()[10:-11].strip()) // 2

			if '</note>' in line:
				in_note = False
				pitch = str(3 + (octave - 1) * 12 + note_to_index[step])
				if not in_chord:
					for i in range(prev_duration):
						if i == 0:
							sequence += ' ' + chord_str
						else:
							sequence += '-' + chord_str
					chord_str = pitch
				else:
					chord_str += '|' + pitch

	sequence += chord_str

	return sequence[1:]

filename = 'MozartPianoSonata_standardized.xml'
print(vectorize(filename))
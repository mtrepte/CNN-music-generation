from os import listdir
from os.path import isfile, join

def vectorize(path, filename):
	file = open(path + filename,'r')
	lines = file.readlines()
	file.close()

	unique_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', 
					'~', '=', '+', '[', ']', '{', '}', '.', ',', '<', 
					'>', '?', '/', 'A', 'B', 'C', 'D', 'E', 'F', 
					'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 
					'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
					'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 
					'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 
					'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', 
					'5', '6', '7', '8', '9', '0', ';', ':', '|']
	index_to_char = {}
	for i in range(len(unique_chars)):
		index_to_char[i] = unique_chars[i]

	note_to_index = {'B_sharp': 0, 'C':0, 'C_sharp':1, 'D':2, 'D_sharp':3, 'E':4, 'E_sharp':5, 'F':5, 'F_sharp':6, 'G':7,
						'G_sharp':8, 'A':9, 'A_sharp':10, 'B':11}
	in_note = False; in_chord = False; in_grace = False; in_rest = False
	sequence = ''; chord_str = ''
	duration = 0; prev_duration = 0
	image = []
	step_keys = []
	divisions = 4
	octave = 5
	step = 'C'
	pitch = 0

	for line in lines:
		if '<divisions>' and '</divisions>' in line:
			divisions = int(line.strip()[11:-12].strip())

		if '<note' in line:
			in_note = True
			in_chord = False
			has_alter = False
			in_grace = False
			in_rest = False

		if '<grace/>' in line:
			in_grace = True

		if not in_grace:
			if in_note:
				if '<rest/>' in line:
					in_rest = True
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
					duration = int(float(line.strip()[10:-11].strip()) / divisions * 4)

			if '</note>' in line:
				in_note = False
				if in_rest:
					pitch = 0
				else:	
					pitch = 3 + (octave - 1) * 12 + note_to_index[step]

				if not in_chord:
					for i in range(prev_duration):
						if i == 0:
							sequence += ' ' + chord_str
						else:
							sequence += '-' + chord_str
						image.append([0 for _ in range(88)]) # Assuming 88 keys
						for key in step_keys:
							image[len(image) - 1][key] = 1

					chord_str = str(index_to_char[pitch])
					step_keys = []
				else:
					chord_str += str(index_to_char[pitch])
				step_keys.append(pitch)

	for i in range(duration):
		if i == 0:
			sequence += ' ' + chord_str
		else:
			sequence += '-' + chord_str
	chord_str = pitch
	sequence = sequence[1:]

	return sequence, image

def dump(path, filename, text):
	open(path + filename, 'w').close() # clear file
	f = open(path + filename, 'w+')
	f.write(text)
	f.close()

# # SPECIFIC FILE
# filename = 'MozartPianoSonata_standardized.xml'
# sequence, img = vectorize(path, filename)
# print(sequence)

# ALL FILES IN DIR
path = 'standardized/'
filenames = [f for f in listdir(path) if isfile(join(path, f))]
total_sequences = ''
for filename in filenames:
	sequence, img = vectorize(path, filename)
	total_sequences += sequence + ' '

dump('', 'seqs.txt', total_sequences)

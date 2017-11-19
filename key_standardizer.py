def get_key_and_offset(lines):
	fifth_to_key_major = {0:'C_maj', 1:'G_maj', 2:'D_maj', 3:'A_maj', 4:'E_maj', 5:'B_maj', 6:'G_flat_maj', 
						7:'D_flat_maj', 8:'A_flat_maj', 9:'E_flat_maj', 10:'B_flat_maj', 11:'F_maj'}
	fifth_to_key_minor = {0:'A_min', 1:'E_min', 2:'B_min', 3:'F_sharp_min', 4:'C_sharp_min', 5:'G_sharp_min', 6:'E_flat_min', 
						7:'B_flat_min', 8:'F_min', 9:'C_min', 10:'G_min', 11:'D_min'}

	in_key = False
	for line in lines:
		if '<key>' in line:
			in_key = True
		if '</key>' in line:
			in_key = False
			break

		if in_key:
			if '<fifths>' in line: # might not always work
				fifth = int(line.strip()[8:-9]) % 12
			if '<mode>' in line:
				mode = line.strip()[6:-7]

	if mode == 'major':
		key = fifth_to_key_major[fifth]
		if fifth % 2 == 0:
			offset = fifth % 12
		else:
			offset = (fifth + 6) % 12
	elif mode == 'minor':
		key = fifth_to_key_minor[fifth]
		if fifth % 2 == 0:
			offset = (fifth + 9) % 12
		else:
			offset = (fifth + 3) % 12
	else:
		print('welp, mode not recognized!')

	return key, offset

def make_key_c(lines):
	_, offset = get_key_and_offset(lines)

	note_to_index = {'C':0, 'C_sharp':1, 'D':2, 'D_sharp':3, 'E':4, 'F':5, 'F_sharp':6, 'G':7,
						'G_sharp':8, 'A':9, 'A_sharp':10, 'B':11}
	index_to_note = {v: k for k, v in note_to_index.items()}

	in_note = False
	for i in range(len(lines)):
		line = lines[i]
		if '<step>' in line:
			note = line.strip()[6:-7].strip()
			in_note = True
			has_alter = False

		if in_note and '<alter>' in line:
			has_alter = True

		if '<octave>' in line:
			if has_alter:
				note += '_sharp'
			index = (note_to_index[note] - offset) % 12
			note = index_to_note[index]
			if '_sharp' in note:
				print("_sharp")
				lines[i - 1] = '          <alter>1</alter>\n'
				lines[i - 2] = '          <step>' + note[0] + '</step>\n'
			else:
				if has_alter:
					lines[i - 2] = '          <step>' + note + '</step>\n'
					lines[i - 1] = ''
				else:
					lines[i - 1] = '          <step>' + note + '</step>\n'
				pass
			in_note = False

	return lines

def remove_left_hand(lines):
	in_note = False
	new_lines = []
	note_lines = []
	staff = -1

	for line in lines:
		if '<note' in line:
			in_note = True
			note_lines = []
			staff = -1

		if in_note:
			note_lines.append(line)
			if '<staff>' in line and '</staff>' in line:
				staff = int(line.strip()[7:-8].strip())
		else:
			new_lines.append(line)
			
		if '</note>' in line:
			if staff == 1:
				new_lines.extend(note_lines)
			in_note = False

	return new_lines


def standardize_musicXML_key(filename):
	file = open('samples/' + filename,'r')
	lines = file.readlines()
	file.close()
	lines = make_key_c(lines)
	lines = remove_left_hand(lines)

	path = 'standardized/' + filename[:-4] + '_standardized.xml'
	open(path, 'w').close()
	new_file = open(path, 'w')
	for line in lines:
		new_file.write(line)
	new_file.close()

filename = 'MozartPianoSonata.xml'
standardize_musicXML_key(filename)

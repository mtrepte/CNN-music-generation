# import music api

def play_seq(seq):
	# char_to_note = { ... }
	notes = seq.split(' ')
	for note in notes:
		note_len = 0
		for char in note:
			if char == '-':
				note_len += 1
		chord_chars = (note.split('-')[0]).split('|')
		# chord = [char_to_note[char] for char in chord_chars]
		# note_len *= ?
		# play_note(chord, note_len)

def play_img(img):
	# index_to_note = { ... }
	note_len = 0
	for step in img:
		chord = []; last_chord = []
		for index in range(len(step)):
			pitch = step[index]
			if pitch == 1:
				chord.append(index_to_note[index])
		if chord == last_chord:
			note_len += 1
		else:
			#play_note(last_chord, note_len)
			note_len = 0

		last_chord = chord

	#play_note(last_chord, note_len)



from scipy.io import wavfile
import argparse
import numpy as np
import pygame
import time
import sys

def play_seq(seq, note_sounds):
	#char_to_note = { ... }
	notes = seq.split(' ')
	for note in notes:
		duration = 0
		for char in note:
			if char == '-':
				duration += 1
		chord = (note.split('-')[0]).split('|')
		# chord = [char_to_note[char] for char in chord_chars]
		# duration *= ?
		play_note(chord, duration, note_sounds)

def play_img(img, note_sounds):
	# index_to_note = { ... }
	duration = 0
	for step in img:
		chord = []; last_chord = []
		for index in range(len(step)):
			pitch = step[index]
			if pitch == 1:
				chord.append(index_to_note[index])
		if chord == last_chord:
			duration += 1
		else:
			play_note(last_chord, duration, note_sounds)
			duration = 0

		last_chord = chord

	play_note(last_chord, duration)

# Adapted from https://github.com/Zulko/pianoputer
def init_sounds(soundfile):
	fps, sound = wavfile.read(soundfile)

	tones = range(-66, 22)
	sys.stdout.write('Transponding sound file... ')
	sys.stdout.flush()
	transposed_sounds = [speedx(pitchshift(sound, n), 1) for n in tones]
	print('finished!')

	pygame.mixer.init(fps, -16, 1, 2048)

	keys = range(88)
	sounds = map(pygame.sndarray.make_sound, transposed_sounds)
	note_sounds = dict(zip(keys, sounds))
	return note_sounds

# Adapted from https://github.com/Zulko/pianoputer
def play_note(chord, duration, key_sounds):
	for note in chord:
		note_sounds[int(note)].play(fade_ms=200)

	duration_time = min([.5 * (duration / 4), 5])
	time.sleep(duration_time)

	# for note in chord:
	# 	note_sounds[int(note)].fadeout(400)

# Adapted from https://github.com/Zulko/pianoputer
def speedx(snd_array, factor):
    """ Speeds up / slows down a sound, by some factor. """
    indices = np.round(np.arange(0, len(snd_array), factor))
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[indices]

# Adapted from https://github.com/Zulko/pianoputer
def stretch(snd_array, factor, window_size, h):
    """ Stretches/shortens a sound, by some factor. """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        # Two potentially overlapping subarrays
        i = int(i)
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')

# Adapted from https://github.com/Zulko/pianoputer
def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)


file = open('output.txt','r')
seq = file.readlines()[0]
file.close()

print(seq)

soundfile = 'bowl.wav'
note_sounds = init_sounds(soundfile)

play_seq(seq, note_sounds)
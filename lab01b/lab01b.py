3#!/usr/bin/env python

from wav_utils import wav_read, wav_write
import math
import matplotlib
#matplotlib.use('agg') #this fixes issue where matplotlib crashes bc no Tkinter
import matplotlib.pyplot as plot


    
def sine_shifted(amplitude, freq, phi, samp_rate, duration):
	out = []
	for i in range(0, int(duration*samp_rate)): 
		out.append(amplitude*math.sin(-phi + 2*math.pi*i*freq/samp_rate))
		i += 1
	return out

def sine(amplitude, freq, samp_rate, duration):
	out = []
	for i in range(0, int(duration*samp_rate)): 
		out.append(amplitude*math.sin(2*math.pi*i*freq/samp_rate))
		i += 1
	return out

def sine_sum(amplitude_a, amplitude_b, freq, phi, samp_rate, duration):
	out = []
	for i in range(0, int(duration*samp_rate)): 
		out.append( amplitude_a * math.sin(2*math.pi*i*freq/samp_rate) + \
		amplitude_b * math.sin(-phi + 2*math.pi*i*freq/samp_rate) )
		i += 1
	return out


def dt_pulse(A, P, Q, N, NN):
	out = []
	for i in range(int(NN*N)):
		out.append(A if (i%N>=P and i%N < (Q+P) ) else 0 )
		i += 1
	return out

def tuple_assembler(tuples, samp_rate):
	out = []
	for i in range(len(tuples)):
		i_period = samp_rate/tuples[i][0]
		note = dt_pulse(1, 0, i_period/2, i_period, tuples[i][1]*samp_rate/i_period)
		for n in range(len(note)):
			out.append(note[n])
			n+=1
		i += 1
	return out

def tuple_sine_assembler(tuples, samp_rate):
	out = []
	for i in range(len(tuples)):
		note = sine(1, tuples[i][0], samp_rate, tuples[i][1])
		for n in range(len(note)):
			out.append(note[n])
			n+=1
		i += 1
	return out

mystery_tune = [(195.9977179908746, 0.3750), (130.8127826502993, 0.3750),
                (155.5634918610405, 0.1875), (174.6141157165019, 0.1875),
                (195.9977179908746, 0.3750), (130.8127826502993, 0.3750),
                (155.5634918610405, 0.1875), (174.6141157165019, 0.1875),
                (195.9977179908746, 0.3750), (130.8127826502993, 0.3750),
                (155.5634918610405, 0.1875), (174.6141157165019, 0.1875),
                (195.9977179908746, 0.3750), (130.8127826502993, 0.3750),
                (155.5634918610405, 0.1875), (174.6141157165019, 0.1875),
                (195.9977179908746, 1.1250), (130.8127826502993, 1.1250),
                (155.5634918610405, 0.1875), (174.6141157165019, 0.1875),
                (195.9977179908746, 0.7500), (130.8127826502993, 0.7500),
                (155.5634918610405, 0.1875), (174.6141157165019, 0.1875),
                (146.8323839587038, 4.5000), (174.6141157165019, 1.1250),
                (116.5409403795224, 1.1250), (155.5634918610405, 0.1875),
                (146.8323839587038, 0.1875), (174.6141157165019, 0.7500),
                (116.5409403795224, 1.1250), (155.5634918610405, 0.1875),
                (146.8323839587038, 0.1875), (130.8127826502993, 4.5000)]

tune = tuple_assembler(mystery_tune, 44100)
wav_write(tune, 44100, 'tune.wav')
#plot.plot(tune)
plot.show()

print("done")

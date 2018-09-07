import os
import wave
import struct


def wav_read(fname):
    """
    Read a wave file.  This will always convert to mono.

    Arguments:
      * fname: a string containing a file name of a WAV file.

    Returns a tuple with 2 elements:
      * a Python list with floats in the range [-1, 1] representing samples.
        the length of this list will be the number of samples in the given wave
        file.
      * an integer containing the sample rate
    """
    f = wave.open(fname, 'r')
    chan, bd, sr, count, _, _ = f.getparams()

    assert bd == 2, "bit depth must be 16"

    data = []
    for i in range(count):
        frame = f.readframes(1)
        if chan == 2:
            l = struct.unpack('<h', frame[:2])[0]
            r = struct.unpack('<h', frame[2:])[0]
            datum = (l + r) / 2
        else:
            datum = struct.unpack('<h', frame)[0]
        data.append(datum)

    if chan == 2:
        # if stereo, convert to mono
        data = [(data[2*i]+data[2*i+1])/2 for i in range(count//2)]

    return [i/2**15 for i in data], sr


def wav_write(samples, sr, fname):
    """
    Write a mono wave file.

    Arguments:
      * samples: a Python list of numbers in the range [-1, 1], one for each
                 sample in the output WAV file.  Numbers in the list that are
                 outside this range will be clipped to -1 or 1.
      * sr: an integer representing the sampling rate of the output
            (samples/second).
      * fname: a string containing a file name of the WAV file to be written.
    """
    output_file = wave.open(fname, 'w')
    output_file.setparams((1, 2, sr, 0, 'NONE', 'not compressed'))

    out = []
    for frame in samples:
        frame = max(-1, min(1, frame))
        frame = int(frame * (2**15 - 1))
        out.append(frame)

    output_file.writeframes(b''.join(struct.pack('<h', frame)
                                     for frame in out))
    output_file.close()

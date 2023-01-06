from scipy.io.wavfile import read , write


with open('audio.wav') as wavfile:
    input_wav = wavfile.read()

rate, data = read(io.BytesIO(input_wav))
reversed_data = data[::-1] #reversing it

#then, let's save it to a BytesIO object, which is a buffer for bytes object
bytes_wav = bytes()
byte_io = io.BytesIO(bytes_wav)
write(byte_io, rate, reversed_data)
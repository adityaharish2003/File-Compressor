# # import wave
# # # import audioop
# import wave
# import struct
# from HuffmanCoding import HuffmanCoding
# import io
# # Open .wav file in binary mode
# with wave.open("audio.wav", "rb") as wav_file:
#     # Read audio data from file
#     audio_data = wav_file.readframes(wav_file.getnframes())
#     # Get information about the .wav file
#     sample_width = wav_file.getsampwidth()
#     nchannels = wav_file.getnchannels()
#     sample_rate = wav_file.getframerate()

# # Convert audio data to string
# audio_string_bytes = struct.pack("<" + "h"*(len(audio_data)//2), *struct.unpack("<" + "h"*(len(audio_data)//2), audio_data))
# print(type(io.BytesIO(audio_string_bytes).getvalue()))

# with open('audio.txt' , 'w') as f:
#     f.write(audio_string)

# compressed_object = HuffmanCoding(audio_string)
# compressed_object.compress()

# compressed_object.decompress('')



# # Write compressed audio data to file
# # compressed_object.compress()

# # Convert audio string back to audio data
# audio_data = struct.pack("<" + "h"*(len(audio_string)//2), *struct.unpack("<" + "h"*(len(audio_string)//2), audio_string))

# # Create new .wav file
# with wave.open("output.wav", "wb") as wav_file:
#     # Set .wav file parameters
#     wav_file.setnchannels(nchannels)
#     wav_file.setsampwidth(sample_width)
#     wav_file.setframerate(sample_rate)
#     # Write audio data to file
#     wav_file.writeframes(audio_data)

# with wave.open('audio.wav') as fd:
#     params = fd.getparams()
#     frames = fd.readframes(100000000) # 1 million frames max

# print(bytes(frames.decode('utf-16') == frames))  

# with open('input.txt' , 'w') as f:
#     f.write(str(frames))


# with open('input.txt', 'r') as f:
#     string = f.read()

# byte_stream = bytes(string , 'utf-8')

# with wave.open('output.wav', 'wb') as fd:
#     fd.setparams(params)
#     fd.writeframes(byte_stream)
with open("audio.wav", "rb") as f:
    wav_bytes = f.read()
wav_string = wav_bytes.decode("HP-ROMAN8")

# Save string to file
with open("example_string.txt", "w") as f:
    f.write(wav_string)

# Read string from file
with open("example_string.txt", "r") as f:
    wav_string = f.read()

# Convert string back to .wav file
wav_bytes = wav_string.encode("HP-ROMAN8")
with open("example_regenerated1.wav", "wb") as f:
    f.write(wav_bytes)

import re
import numpy as  np
from HuffmanCoding import HuffmanCoding
from PIL import Image
from Metric import Metric

file = "cat.bmp"
byte_stream = np.asarray(Image.open(file) , np.uint8)
byte_string = str(byte_stream.tolist())
shape = byte_stream.shape
with open('image_input.txt' , 'w') as FileHandler:
    FileHandler.write(byte_string)

huffman_coding = HuffmanCoding('image_input.txt')
huffman_coding.compress()
metric = Metric('image_input.txt' , 'image_input.bin')
percentage = metric.calculate_metric()
print(percentage)


huffman_coding.decompress('image_input.bin')

with open('image_input_decompressed.txt') as FileHandler:
    # byte_stream_uncompressed = np.asarray(FileHandler.read(), np.uint8)
    byte_string_uncompressed = str(FileHandler.read())


temp = re.findall(r'\d+', byte_string_uncompressed)
res = list(map(int, temp))
res = np.array(res)
res = res.astype(np.uint8)
res = np.reshape(res, shape)
data = Image.fromarray(res)
data.save('uncompressed.png')
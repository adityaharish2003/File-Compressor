import re
import numpy as  np
from HuffmanCoding import HuffmanCoding
from PIL import Image
from Metric import Metric
import os

class ImageEncoding:
    def __init__(self,file) :
        self.path = file
        self.filename, self.file_extension = os.path.splitext(file)
    def encode(self):
        byte_stream = np.asarray(Image.open(self.filename + self.file_extension) , np.uint8)
        byte_string = str(byte_stream.tolist())
        shape = byte_stream.shape
        file_text_path = self.filename + ".txt"
        with open(file_text_path , 'w') as FileHandler:
            FileHandler.write(byte_string)

        huffman_coding = HuffmanCoding(file_text_path)
        comp_path = huffman_coding.compress('.bmp')

        return shape,comp_path
    def metric_calc(self) :
        metric = Metric('image_input.txt' , 'image_input.bin')
        percentage = metric.calculate_metric()
        print(percentage)

    def huff_decode(self,file_bin_path,shape):
        huffman_coding = HuffmanCoding(file_bin_path)
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
        data.save('cat_uncompressed.png')
    def txt_to_img(self,shape = (853, 1280, 3)):
        with open(self.path) as FileHandler:
            # byte_stream_uncompressed = np.asarray(FileHandler.read(), np.uint8)
            byte_string_uncompressed = str(FileHandler.read())
        temp = re.findall(r'\d+', byte_string_uncompressed)
        res = list(map(int, temp))
        res = np.array(res)
        res = res.astype(np.uint8)
        res = np.reshape(res, shape)
        data = Image.fromarray(res)
        data.save(self.filename + ".png")

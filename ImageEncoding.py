import re
import numpy as  np
from HuffmanCoding import HuffmanCoding
from PIL import Image
from Metric import Metric
import os
from collections import Counter
from itertools import chain

class ImageEncoding:
    def __init__(self,file) :
        self.path = file
        self.filename, self.file_extension = os.path.splitext(file)

    def to_binary_list(self,n):
        return [n] if (n <= 1) else self.to_binary_list(n >> 1) + [n & 1]

    def from_binary_list(self,bits):
        result = 0
        for bit in bits:
            result = (result << 1) | bit
        return result

    def pad_bits(self,bits, n):
        assert(n >= len(bits))
        return ([0] * (n - len(bits)) + bits)

    class OutputBitStream(object): 
        def __init__(self, file_name): 
            self.file_name = file_name
            self.file = open(self.file_name, 'wb') 
            self.bytes_written = 0
            self.buffer = []

        def write_bit(self, value):
            self.write_bits([value])

        def write_bits(self, values):
            self.buffer += values
            while len(self.buffer) >= 8:
                self._save_byte()        


        def _save_byte(self):
            bits = self.buffer[:8]
            self.buffer[:] = self.buffer[8:]

            byte_value = self.from_binary_list(bits)
            self.file.write(bytes([byte_value]))
            self.bytes_written += 1

        def close(self): 
            self.flush()
            self.file.close()

    class InputBitStream(object): 
        def __init__(self, file_name): 
            self.file_name = file_name
            self.file = open(self.file_name, 'rb') 
            self.bytes_read = 0
            self.buffer = []

        def read_bit(self):
            return self.read_bits(1)[0]

        def read_bits(self, count):
            while len(self.buffer) < count:
                self._load_byte()
            result = self.buffer[:count]
            self.buffer[:] = self.buffer[count:]
            return result

        def flush(self):
            assert(not any(self.buffer))
            self.buffer[:] = []

        def _load_byte(self):
            value = ord(self.file.read(1))
            self.buffer += self.pad_bits(self.to_binary_list(value), 8)
            self.bytes_read += 1

        def close(self): 
            self.file.close()


    def encode(self):
        # byte_stream = np.asarray(Image.open(self.filename + self.file_extension) , np.uint8)
        # byte_string = str(byte_stream.tolist())
        byte_stream = Image.open(self.filename + self.file_extension)
        byte_string = byte_stream.getdata()
        values = chain.from_iterable(byte_string)
        shape = (byte_stream.height,byte_stream.width)
        file_text_path = self.filename + ".txt"
        with open(file_text_path , 'wb') as FileHandler:
            FileHandler.write(bytes(values))
        huffman_coding = HuffmanCoding(file_text_path)
        comp_path,codes = huffman_coding.compress('.bmp',shape)

        return shape,comp_path,codes
        
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
        byte_string_uncompressed = []
        with open(self.path,'rb') as FileHandler:
            byte = FileHandler.read(1)
            byte_string_uncompressed.append(int.from_bytes(byte,"big"))
            while(len(byte)>0):
                byte = FileHandler.read(1)
                byte_string_uncompressed.append(int.from_bytes(byte,"big"))
            # byte_stream_uncompressed = np.asarray(FileHandler.read(), np.uint8)
        # temp = re.findall(r'\d+', byte_string_uncompressed)
        # res = list(map(int, temp))
        # res = np.array(res)
        # res = res.astype(np.uint8)
        # res = np.reshape(res, shape)
        data = Image.frombytes('RGB', shape , bytes(byte_string_uncompressed))
        # data = Image.fromarray(res)
        data.save(self.filename  + ".bmp")

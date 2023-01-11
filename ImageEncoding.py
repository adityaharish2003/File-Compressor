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
        self.file_extension = self.file_extension.lower()

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
        # print(list(byte_string))
        values = chain.from_iterable(byte_string)
        # print(*values)
        shape = (byte_stream.width,byte_stream.height)
        file_text_path = self.filename + ".txt"
        with open(file_text_path , 'wb') as FileHandler:
            FileHandler.write(bytes(values))
        huffman_coding = HuffmanCoding(file_text_path)
        comp_path = huffman_coding.compress_img(self.file_extension,shape)

        return comp_path
        
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
        
    # def txt_to_img(self,shape = (853, 1280, 3)):
    #     byte_string_uncompressed = []
    #     with open(self.path,'rb') as FileHandler:
    #         byte = FileHandler.read(1)
    #         byte_string_uncompressed.append(int.from_bytes(byte,"big"))
    #         while(len(byte)>0):
    #             byte = FileHandler.read(1)
    #             byte_string_uncompressed.append(int.from_bytes(byte,"big"))
    #         # byte_stream_uncompressed = np.asarray(FileHandler.read(), np.uint8)
    #     # temp = re.findall(r'\d+', byte_string_uncompressed)
    #     # res = list(map(int, temp))
    #     # res = np.array(res)
    #     # res = res.astype(np.uint8)
    #     # res = np.reshape(res, shape)
    #     data = Image.frombytes('RGB', shape , bytes(byte_string_uncompressed))
    #     # data = Image.fromarray(res)
    #     data.save(self.filename  + ".bmp")
        
    def txt_to_img(self,shape,file_ext):
        byte_string_uncompressed = []
        with open(self.path,'rb') as FileHandler:
            byte = FileHandler.read(1)
            byte_string_uncompressed.append(int.from_bytes(byte,"little"))
            while(len(byte)>0):
                byte = FileHandler.read(1)
                byte_string_uncompressed.append(int.from_bytes(byte,"little"))
            # byte_stream_uncompressed = np.asarray(FileHandler.read(), np.uint8)
        # temp = re.findall(r'\d+', byte_string_uncompressed)
        # res = list(map(int, temp))
        # res = np.array(res)
        # res = res.astype(np.uint8)
        # res = np.reshape(res, shape)
        # byte_string_uncompressed = byte_string_uncompressed[0:shape[0]*shape[1]*3]
        # byte_string_uncompressed = np.array(byte_string_uncompressed).reshape(shape[0],shape[1],3)
        k = 0
        data = Image.new(mode = "RGB",size = (shape[0],shape[1]))
        pixel_map = data.load()
        average = [0,0,0]
        # print(len(byte_string_uncompressed))
        for i in range(shape[1]):
            for j in range(shape[0]):
                if(k+3 > len(byte_string_uncompressed)):
                    break
                pixel_map[j,i] = (byte_string_uncompressed[k],byte_string_uncompressed[k+1],byte_string_uncompressed[k+2])

                average[0] += byte_string_uncompressed[k]
                average[1] += byte_string_uncompressed[k+1]
                
                average[2] += byte_string_uncompressed[k+2]
                k+=3
        average[0]/=shape[0]*shape[1]
        average[1]/=shape[0]*shape[1]
        average[2]/=shape[0]*shape[1]
        # print(byte_string_uncompressed)
        # print(average)
        # data = Image.fromarray(res)
        data.save(self.filename + file_ext)
        os.remove(self.filename + '.txt')

import os
import numpy as  np
from HuffmanCoding import HuffmanCoding
from Metric import Metric

class PdfEncoding :
    def __init__(self,path):
        self.path = path
        self.huffman_coding = HuffmanCoding(self.path)
    def encode(self):
        filename, file_extension = os.path.splitext(self.path)
        text_filename = filename + ".txt"
        with open(self.path, 'rb') as f, open(text_filename,'w',encoding='latin1') as output :
            data = f.read()
            output.write(str(data))

        enc_path = self.huffman_coding.compress(file_extension)
        return enc_path
    def decode(self):
        filename, file_extension = os.path.splitext(self.path)
        file_extension = '.pdf'
        # file = open(filename  + file_extension, 'wb')
        # for line in open(self.path, 'rb').readlines():
        #     file.write(line)
        with open(filename  + file_extension,'wb') as file, open(self.path,'rb') as data:
            text = data.read()
            text = text.decode('latin1')
            file.write(bytes(text,'latin1'))
        os.remove(filename + '.txt')
        file.close()
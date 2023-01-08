from HuffmanCoding import HuffmanCoding
import os
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename,asksaveasfilename
from ImageEncoding import ImageEncoding
from PIL import Image
import numpy as  np
from pdf_driver import PdfEncoding

class driver:
    def send(self):
        Tk().withdraw()
        path = askopenfilename()
        print(path)
        filename, file_extension = os.path.splitext(path)
        shape = 0
        enc_path = ""
        if(file_extension == ".txt"):
            FileHandler = HuffmanCoding(path)
            enc_path = FileHandler.compress()
            # out,ext = FileHandler.decompress(path)
        elif(file_extension == ".bmp"):
            imgenc = ImageEncoding(path)
            shape,enc_path,codes = imgenc.encode()
            # imgenc.decode(enc_path,shape)
        elif(file_extension == ".pdf"):
            pdfenc = PdfEncoding(path)
            enc_path = pdfenc.encode()
        return enc_path,codes

    def receive(self, enc_path):
        # Tk().withdraw()
        # enc_path = asksaveasfilename()
        #add code for writing binary string into binary file
        decoding_huff = HuffmanCoding(enc_path)
        text_path,ext,shape,codes = decoding_huff.decompress()
        # ext = '.bmp'
        # text_path = "cat_decompressed.txt"
        # byte_stream = np.asarray(Image.open("cat.bmp") , np.uint8)
        # byte_string = str(byte_stream.tolist())
        # shape = byte_stream.shape
        # print(text_path,ext)
        # print(shape)

        if(ext == ".bmp"):
            imgenc = ImageEncoding(text_path)
            imgenc.txt_to_img(shape)
        elif(ext == ".pdf"):
            pdfenc = PdfEncoding(text_path)
            pdfenc.decode()
        return codes
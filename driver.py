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
        filename, file_extension = os.path.splitext(path)
        shape = 0
        enc_path = ""
        if(file_extension == ".txt"):
            FileHandler = HuffmanCoding(path)
            enc_path = FileHandler.compress()
            # out,ext = FileHandler.decompress(path)
        elif(file_extension.lower() == ".bmp" or file_extension.lower() == ".png" or file_extension.lower() == ".jpg"):
            imgenc = ImageEncoding(path)
            enc_path = imgenc.encode()
            # imgenc.decode(enc_path,shape)
        elif(file_extension == ".pdf"):
            pdfenc = PdfEncoding(path)
            enc_path = pdfenc.encode()
        return enc_path

    def receive(self, enc_path):
        # Tk().withdraw()
        # enc_path = asksaveasfilename()
        #add code for writing binary string into binary file
        decoding_huff = HuffmanCoding(enc_path)
        text_path,ext,shape= decoding_huff.decompress()
        if(ext == ".bmp" or ext == ".png" or ext == ".jpg"):
            text_path,ext,shape= decoding_huff.decompress_img()
        # ext = '.bmp'
        # text_path = "cat_decompressed.txt"
        # byte_stream = np.asarray(Image.open("cat.bmp") , np.uint8)
        # byte_string = str(byte_stream.tolist())
        # shape = byte_stream.shape
        # print(text_path,ext)
        # print(shape)

        if(ext == ".bmp" or ext == ".png" or ext == ".jpg"):
            imgenc = ImageEncoding(text_path)
            imgenc.txt_to_img(shape,ext)
        elif(ext == ".pdf"):
            pdfenc = PdfEncoding(text_path)
            pdfenc.decode()
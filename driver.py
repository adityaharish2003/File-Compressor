from HuffmanCoding import HuffmanCoding

FileHandler = HuffmanCoding('D:/Programs/IT206_Project/DSA_PROJECT/input.txt')
path = FileHandler.compress()

out,ext = FileHandler.decompress(path)

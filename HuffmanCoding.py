import heapq
import os
import pickle
from itertools import chain
import numpy as np

class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}
		self.delimiter = '\x01'
		self.delimiter += '\x02'
		self.delimiter += '\x03'

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, HeapNode)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap) > 1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text
	


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b

	def compress_img(self,file_ext = '.txt',shape = 0):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"
		file_extension = file_ext
		with open(self.path, 'rb') as FileHandler, open(output_path, 'wb') as output:
			output.write(bytes((' '.join('{0:08b}'.format(ord(x), 'b') for x in file_extension)),'latin1'))
			output.write(bytes('\x01','latin1'))
			byte = FileHandler.read(1)
			byte_string_uncompressed =[]
			byte_string_uncompressed.append(int.from_bytes(byte,"little"))
			delimiter =  bytes(self.delimiter,'latin1')
			while(len(byte)>0):
				byte = FileHandler.read(1)
				byte_string_uncompressed.append(int.from_bytes(byte,"little"))
			red_array = byte_string_uncompressed[0::3]
			green_array = byte_string_uncompressed[1::3]
			blue_array = byte_string_uncompressed[2::3]
			print(f"{np.average(red_array)} {np.average(green_array)} {np.average(blue_array)}")
			frequency = self.make_frequency_dict(byte_string_uncompressed)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()
			exp_size = 0
			for i in self.codes.keys():
				exp_size += frequency[i]*(len(self.codes[i]))
			#red
			print(exp_size)
			encoded_text = self.get_encoded_text(red_array)
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))
			output.write(delimiter)
			#green
			encoded_text = self.get_encoded_text(green_array)
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))
			output.write(delimiter)
			#blue
			encoded_text = self.get_encoded_text(blue_array)
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))
			output.write(delimiter)
			self.codes["shape"] = shape
			pickle.dump(self.codes, output)
		print("Compressed")
		return output_path

	def compress(self,file_ext = '.txt',shape = 0):

		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"
		file_extension = file_ext
		with open(self.path, 'r+' , encoding = 'latin1') as file, open(output_path, 'wb') as output:
			output.write(bytes((' '.join('{0:08b}'.format(ord(x), 'b') for x in file_extension)),'latin1'))
			output.write(bytes('\x01','latin1'))
			text = file.read()
			text = text.rstrip()
			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()
			encoded_text = self.get_encoded_text(text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			# print(len(self.codes))
			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))
			delimiter =  bytes(self.delimiter,'latin1')
			output.write(delimiter)
			self.codes["shape"] = shape
			pickle.dump(self.codes, output)
		print("Compressed")
		return output_path


	""" functions for decompression: """


	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text

	def decode_img(self, encoded_text):
		current_code = ""
		decoded_text  = []

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text.append(character)
				current_code = ""

		return decoded_text

	def decompress_img(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename  + "_unc" + ".txt"
		file_extension = ""
		huff_code = {}
		delimiter = [bytes('\x01','latin1'),bytes('\x02','latin1'),bytes('\x03','latin1')]
		with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
			bit_string = ""
			byte = file.read(1)
			shape = 0
			while(len(byte) >0 and byte != delimiter[0]):
				file_extension += chr(ord(byte))
				byte = file.read(1)
			file_extension = [chr(int(i,2)) for i in file_extension.split()]
			file_extension = ''.join(file_extension)
			#Red
			byte = file.read(1)
			while(True):
			# while(len(byte) > 0 and byte != bytes(' '.join('{0:08b}'.format(ord(x), 'b') for x in delimiter),encoding= 'utf-8')):
				while(len(byte) >0 and byte != delimiter[0]):
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string += bits
					byte = file.read(1)
				char1 = file.read(1)
				char2 = file.read(1)
				if(char1 == delimiter[1] and char2 == delimiter[2]):
						break
				else :
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string += bits
					char1= ord(char1)
					bits = bin(char1)[2:].rjust(8, '0')
					bit_string += bits
					char2 = ord(char2)
					bits = bin(char2)[2:].rjust(8, '0')
					bit_string += bits
					byte = file.read(1)
			#Green
			# print(len(bit_string))
			byte = file.read(1)
			# print(byte)
			bit_string2 = ""
			while(True):
			# while(len(byte) > 0 and byte != bytes(' '.join('{0:08b}'.format(ord(x), 'b') for x in delimiter),encoding= 'utf-8')):
				while(len(byte) >0 and byte != delimiter[0]):
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string2 += bits
					byte = file.read(1)
				char1 = file.read(1)
				char2 = file.read(1)
				if(char1 == delimiter[1] and char2 == delimiter[2]):
					break
				else :
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string2 += bits
					char1 = ord(char1)
					bits = bin(char1)[2:].rjust(8, '0')
					bit_string2 += bits
					char2 = ord(char2)
					bits = bin(char2)[2:].rjust(8, '0')
					bit_string2 += bits
					byte = file.read(1)
			#Blue
			byte = file.read(1)
			bit_string3 = ""
			while(True):
			# while(len(byte) > 0 and byte != bytes(' '.join('{0:08b}'.format(ord(x), 'b') for x in delimiter),encoding= 'utf-8')):
				while(len(byte) >0 and byte != delimiter[0]):
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string3 += bits
					byte = file.read(1)
				char1 = file.read(1)
				char2 = file.read(1)
				if(char1 == delimiter[1] and char2 == delimiter[2]):
					break
				else :
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string3 += bits
					char1= ord(char1)
					bits = bin(char1)[2:].rjust(8, '0')
					bit_string3 += bits
					char2= ord(char2)
					bits = bin(char2)[2:].rjust(8, '0')
					bit_string3 += bits
					byte = file.read(1)

			encoded_text1 = self.remove_padding(bit_string)
			encoded_text2 = self.remove_padding(bit_string2)
			encoded_text3 = self.remove_padding(bit_string3)
			# byte = file.read(1)
			# while(len(byte) > 0 and (byte) != bytes(' '.join('{0:08b}'.format(ord(x), 'b') for x in delimiter),encoding= 'utf-8')):
			huff_code = pickle.load(file,encoding='latin1')
			shape = huff_code.pop("shape")
			print(huff_code)
			# rev_huff_code = {v:k for k,v in codes.items()}
			# print(huff_code)
			rev_huff_code = {v:k for k,v in huff_code.items()}
			self.reverse_mapping = rev_huff_code
			red = self.decode_img(encoded_text1)
			green = self.decode_img(encoded_text2)
			blue = self.decode_img(encoded_text3)
			length = shape[0]*shape[1]
			print(len(red),len(blue),len(green))
			red = np.resize(red,length)
			green = np.resize(green,length)
			blue = np.resize(blue,length)
			decompressed_text = []
			# print(len(decompressed_text))
			# decompressed_text = chain.from_iterable(decompressed_text)
			for i in range(length):
				decompressed_text.append(red[i])
				decompressed_text.append(green[i])
				decompressed_text.append(blue[i])
			output.write(bytes(decompressed_text))

		print("Decompressed")
		return output_path,file_extension,shape

	def decompress(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename  + "_unc" + ".txt"
		file_extension = ""
		huff_code = {}
		delimiter = [bytes('\x01','latin1'),bytes('\x02','latin1'),bytes('\x03','latin1')]
		with open(self.path, 'rb') as file, open(output_path, 'w',encoding='latin1') as output:
			bit_string = ""
			byte = file.read(1)
			shape = 0

			# while(len(byte) > 0 and byte != bytes(' '.join('{0:08b}'.format(ord(x), 'b') for x in delimiter),encoding= 'utf-8')):
			while(len(byte) >0 and byte != delimiter[0]):
				file_extension += chr(ord(byte))
				byte = file.read(1)
			file_extension = [chr(int(i,2)) for i in file_extension.split()]
			file_extension = ''.join(file_extension)
			if file_extension == '.bmp':
				return output_path,file_extension,shape
			while(True):
				while(len(byte) >0 and byte != delimiter[0]):
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string += bits
					byte = file.read(1)
				char1 = file.read(1)
				char2 = file.read(1)
				if(char1 == delimiter[1]):
					break
				else :
					byte = ord(byte)
					bits = bin(byte)[2:].rjust(8, '0')
					bit_string += bits
					char1= ord(char1)
					bits = bin(char1)[2:].rjust(8, '0')
					bit_string += bits
					char2 = ord(char2)
					bits = bin(char2)[2:].rjust(8, '0')
					bit_string += bits
					byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)
			# byte = file.read(1)
			# while(len(byte) > 0 and (byte) != bytes(' '.join('{0:08b}'.format(ord(x), 'b') for x in delimiter),encoding= 'utf-8')):
			huff_code = pickle.load(file,encoding='latin1')
			shape = huff_code.pop("shape")
			# rev_huff_code = {v:k for k,v in codes.items()}
			rev_huff_code = {v:k for k,v in huff_code.items()}
			self.reverse_mapping = rev_huff_code

			decompressed_text = self.decode_text(encoded_text)
			output.write(decompressed_text)

		print("Decompressed")
		return output_path,file_extension,shape
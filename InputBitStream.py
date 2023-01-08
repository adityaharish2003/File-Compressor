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
        self.buffer += pad_bits(to_binary_list(value), 8)
        self.bytes_read += 1

    def close(self): 
        self.file.close()
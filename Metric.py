import os
class Metric:
    def __init__(self, 
    uncompressed_file_name : str , 
    compressed_file_name : str):
        self.uncompressed_file_name = uncompressed_file_name
        self.compressed_file_name = compressed_file_name
    
    def calculate_metric(self) -> float:  
        uncompressed_size = os.path.getsize(self.uncompressed_file_name)
        compressed_size = os.path.getsize(self.compressed_file_name)
        return ((uncompressed_size - compressed_size) / uncompressed_size)*100
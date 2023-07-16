# CLI tool for File Transfer with Compression

This project is a Python-based file transfer tool that enables you to transfer files between different systems while compressingn the files for efficient transfer. The tool utilizes compression algorithms to reduce the size of the files before transferring them, optimizing bandwidth usage and reducing transfer time. It supports various file formats including text files, images, and PDF files.

# Features
* Transfer files between systems using a client-server architecture.
* Support for compression of text files, images (BMP, PNG, JPG), and PDF files.
* Utilize Huffman Coding algorithm for text file compression.
* Provides image encoding techniques to compress and decompress images.
* Preserve file integrity and ensure successful decompression on the receiving end.
* User-friendly command-line interface for ease of use.
* Cross-platform compatibility.

# Installation 
* Run `server.py`.
* Run `client.py` and create a new user if necessary, else login.

# Usage
* The recipient client should choose the `listen` mode and the sender should choose `connect` mode. 
* The recipient client should choose a port that does not conflict with other applications and the server.
* The sender can type the command `\GET_CLIENT_INFO` to connect to a recipient.
* Once the sender has entered the command, the username of the recipient client must be entered. 
* Following that, a file transfer prompt will appear. 
* The sender can type the `\SEND_FILE` command to send a file.
* A window will be created for file selection, and the compressed file will be sent to the recipient client.
* Another window will be created on the recipient's side, which prompts the user to enter a filename for the recieved file.

# Contributions

If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request. To contribute to the project, follow these steps:

* Fork the repository.
* Create a new branch for your feature or bug fix.
* Make your changes and commit them.
* Push your changes to your fork.
* Submit a pull request to the main repository.


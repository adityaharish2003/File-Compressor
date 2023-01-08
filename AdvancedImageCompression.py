from PIL import Image
from HuffmanCoding import HuffmanCoding

# Open the image file
image = Image.open('image.jpg')

# Convert the image to a format that supports lossless compression
# This step is necessary because JPEG does not support lossless compression by default
image = image.convert('RGB')

# Create an empty list to store the image data
image_data = []

# Iterate through the pixels in the image
for pixel in image.getdata():
    # Append the pixel data to the image_data list
    image_data.append(pixel)

# Encode the image data using a lossless compression algorithm
compressed_image_data = lossless_compress(image_data)

# Save the compressed image data to a new file
with open('compressed_image.jpg', 'wb') as f:
    f.write(compressed_image_data)


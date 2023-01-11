from driver import driver
from ImageEncoding import ImageEncoding

# img = ImageEncoding('tests/blackbuck.txt')
# img.txt_to_img((512,512))
driver_ = driver()
path = driver_.send()
driver_.receive(path)
count = 0


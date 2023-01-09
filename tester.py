from driver import driver
from ImageEncoding import ImageEncoding

# img = ImageEncoding('tests/yellow.txt')
# img.txt_to_img((200,144))
driver_ = driver()
path = driver_.send()
driver_.receive(path)
count = 0


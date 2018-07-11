from PIL import Image
from math import floor
f = Image.open("grayscale.jpg")
pix = f.load()

brightness = 0.25

array = []

for i in range(f.size[0]):
    line_array = []
    for j in range(f.size[1]):
        pixel = pix[i,j]
        # blue =  pixel & 255
        # green = (pixel >> 8) & 255
        # red =   (pixel >> 16) & 255
        # alpha = (pixel >> 24) & 255
        # print(pixel)
        # print(red, green, blue, alpha)
        # there's only stuff in the "blue" channel, which is the grayscale value
        #line_array.append(0)
        line_array.append(int(pixel * brightness))
        #line_array.append(0)

    array.append('bytes([' + ','.join(str(e) for e in line_array) + '])\n')
        
print("party_pixels = [")
print(', '.join(array))
print("]")




def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

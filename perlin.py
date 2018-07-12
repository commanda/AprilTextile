from PIL import Image
from math import floor
f = Image.open("Figure_grayscale_small.png")
pix = f.load()

brightness = 0.25

array = []

for i in range(f.size[0]):
    for j in range(f.size[1]):
        pixel = pix[i,j]
        array.append(str(int(pixel * brightness)))


long_string = "party_pixels = bytes([" + ','.join(array) + "])"

#print(long_string)

with open('whole_image_party_pixels.py', 'w') as f:
    f.write(long_string)

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

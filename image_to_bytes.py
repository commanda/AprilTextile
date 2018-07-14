from PIL import Image
from math import floor
f = Image.open("strip_something.png")
pix = f.load()

brightness = 1.0

array = []
print(f.size)
for i in range(f.size[0]):
    line_array = []
    for j in range(f.size[1]):
        pixel = pix[i,j]
        print(pixel)
        if isinstance(pixel, tuple):
            line_array.append(pixel[0]) 
            line_array.append(pixel[1])
            line_array.append(pixel[2])
        else:
            line_array.append(int(pixel))

    array.append(','.join(str(e) for e in line_array))

long_string = "party_pixels = bytes([" + ', '.join(array) + "])"

#print(long_string)

with open('whole_image_party_pixels.py', 'w') as f:
    f.write(long_string)

def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

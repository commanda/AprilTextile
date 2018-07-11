from PIL import Image
f = Image.open("grayscale.jpg")
pix = f.load()

print(f.bits, f.size, f.format)

array = []

for i in range(f.size[0]):
    for j in range(f.size[1]):
        pixel = pix[i,j]
        # blue =  pixel & 255
        # green = (pixel >> 8) & 255
        # red =   (pixel >> 16) & 255
        # alpha = (pixel >> 24) & 255
        # print(pixel)
        # print(red, green, blue, alpha)
        # there's only stuff in the "blue" channel, which is the grayscale value
        array.append(pixel)
        

print(array)
print("done")



def normalize(x, old_min, old_max, new_min, new_max):
    return (((x - old_min) / (old_max - old_min)) * (new_max - new_min)) + new_min

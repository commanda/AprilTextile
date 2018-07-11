from PIL import Image
jpgfile = Image.open("grayscale.jpg")

print(jpgfile.bits, jpgfile.size, jpgfile.format)

print("hello")
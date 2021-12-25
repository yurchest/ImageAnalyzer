# from numpy import array
import numpy
from matplotlib import pyplot as plt
from PIL import Image
import os
import sys

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# print('OS PATH : ',os.getcwd())
img_name = input('Введите название BMP картинки : ')

img = Image.open(img_name)
obj = img.load()
width, height = img.size
pixel_values = list(img.getdata())

print('Width = ', width, '\nHeight = ', height)

pixel_values = numpy.array(pixel_values).reshape((height, width))

line_sum_array = []

for line in pixel_values:
    line_sum_array.append(sum(line))

max_sum_line = max(line_sum_array)
index_max_sum_line = line_sum_array.index(max(line_sum_array))

print('Line with max : ', index_max_sum_line)

x = []
y = []
for i, pixel in enumerate(pixel_values[index_max_sum_line]):
    x.append(i)
    y.append(pixel)

print(x)
print(y)

fp = open('file.txt', 'w')
for i in range(width):
    fp.write(f'%{len(str(max(x))) + 1}d%{len(str(max(y))) + 5}d\n' % (x[i], y[i]))
fp.close()

plt.title("Диаграмма направленности")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(x, y)
plt.show()

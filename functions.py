import numpy
from matplotlib import pyplot as plt


def line_with_max_brightness(img):
    width, height = img.size
    pixel_values = list(img.getdata())

    print('Width = ', width, '\nHeight = ', height)

    pixel_values = numpy.array(pixel_values).reshape((height, width))

    line_sum_array = []

    for line in pixel_values:
        line_sum_array.append(sum(line))

    max_sum_line = max(line_sum_array)
    index_max_sum_line = line_sum_array.index(max(line_sum_array))

    return [pixel_values, index_max_sum_line, width]


def get_x_y(pixel_values, index_max_sum_line):
    x = []
    y = []

    for i, pixel in enumerate(pixel_values[index_max_sum_line]):
        x.append(i)
        y.append(pixel)
    return [x, y]


def write_in_file(width, x, y):
    fp = open('file.txt', 'w')
    for i in range(width):
        fp.write(f"%{len(str(max(x))) + 1}d%{len(str(max(y))) + 5}d\n" % (x[i], y[i]))
    fp.close()


def show_plt(x, y):
    plt.title("Диаграмма направленности")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(x, y)
    plt.show()

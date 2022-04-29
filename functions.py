import numpy
from matplotlib import pyplot as plt
from datetime import datetime
from scipy.signal import find_peaks

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

    index_max_y = y.index(max(y))

    for i in range(len(x)):
        x[i] = x[i] - index_max_y

    return [x, y]


def write_in_file(x, y, ugl_size=None):
    fp = open('file.txt', 'w')
    fp.write('Date/Time : ' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + '\n')
    fp.write('Угловой размер пикселя = ' + str(ugl_size) + '\n\n')
    for i in range(len(y)):
        # fp.write(str(x[i]))
        fp.write(f"%{len(str(max(x))) + 1}.6f%{len(str(max(y))) + 10}.5f\n" % (x[i], y[i]))
        # print(x[i])
    fp.close()


def show_plt(x, y, vertline=0):
    y = numpy.array(y)
    y_tomin = numpy.multiply(y, -1)
    plt.title("Диаграмма направленности")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axvline(vertline, color='green', ls=':', lw=2)
    plt.plot(x,y)
    try:
        peaks, _ = find_peaks(y, height=70, distance=10, prominence=10, width=40)
        plt.plot(peaks, y[peaks], "x")
    except:
        pass
    try:
        lows, _ = find_peaks(y_tomin, distance=10, prominence=10, width=20)
        plt.plot(lows, y[lows], "x")
    except:
        pass
    # leng = peaks[1] - peaks[0]
    # print(leng/16.289)



    plt.show()


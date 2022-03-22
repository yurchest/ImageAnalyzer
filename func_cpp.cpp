//#include <iostream>

extern "C"
{

    short index_max_in_array(short *array, int len){
        short max = 0;
        int index_max;

        for (int i = 0; i < len; i++){
            if (array[i] > max){
                max = array[i];
                index_max = i;
            }
        }
        return index_max;
    }

    void get_x(short *x, short *array, int len, int index_max){
        for (int i = 0; i < len; i++){
            x[i] = i - index_max;
        }
    }

    void recalc_x_ugl_size(float *x, int len, float ugl_size){
        for (int i = 0; i < len; i++){
            x[i] = x[i]/ugl_size;
        }
    }

    short sum_in_array(short *array, int len){
        short sum = 0;
        for (int i = 0; i < len; i++){
            sum = sum + array[i];
        }
        return sum;
    }
}
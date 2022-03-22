
extern "C" short index_max_in_array(short *array, int len){
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

//extern "C" short get_x(short *array, int len, int index_max){
//    short *x = new short[index_max];
//    for (int i = 0; i < len; i++){
//        x[i] = i - index_max;
//    }
//    return *x;
//}
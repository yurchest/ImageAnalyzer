#include "func_cpp.cpp"
#include <iostream>

using namespace std;

// short* get_x(short *array, int &len, int &index_max){
//         short *x = new short[4];
//         for (int i = 0; i < len; i++){
//             x[i] = i - index_max;
//         }
// //        delete[] x;
//         return x;
//     }

int main(){
    short a[4] = {2,4,5,6};
    int len = 4;

    short *x = get_x(a, len, len);

    for (int i =0; i < len; i++){
        cout << x[i] << endl;
    }
    
    // delete[] x;
}
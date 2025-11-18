#include <stdio.h>
#include <complex.h>
#define _USE_MATH_DEFINES
#include <math.h>

// -------- COMANDI DI COMPILAZIONE --------
// windows: gcc -shared -o dft.dll dft.c
// linux: gcc -shared -o dft.so -fPIC dft.c
// -----------------------------------------

void dft(float input[], float output[], int numeroCampioni) {
    float complex somma;

    if(input == NULL || output == NULL)
        return;

    for(int k=0; k<numeroCampioni; k++) {
        somma = 0.0;

        for(int n=0; n<numeroCampioni; n++)
            somma += input[n] * cexp(-I * 2 * M_PI * n * k/numeroCampioni);

        output[k] = cabs(somma);
    }
}
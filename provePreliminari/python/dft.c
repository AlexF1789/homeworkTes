#include <stdio.h>
#include <complex.h>
#define _USE_MATH_DEFINES
#include <math.h>

// windows: gcc -shared -o dft.dll dft.c
// linux: gcc -shared -o dft.so -fPIC dft.c

void dft(float input[], float output[], int numeroCampioni) {
    float complex somma;

    printf("Input: ");
    for(int i=0; i<numeroCampioni; i++) {
        printf("%.2f  ", input[i]);
    }

    printf("\nOutput: ");
    for(int i=0; i<numeroCampioni; i++) {
        printf("%.0f  ", output[i]);
    }
    printf("\n");

    if(input == NULL || output == NULL)
        return;

    for(int k=0; k<numeroCampioni; k++) {
        somma = 0.0;

        for(int n=0; n<numeroCampioni; n++)
            somma += input[n] * cexp(-I * 2 * M_PI * n * k/numeroCampioni);

        output[k] = cabs(somma);
    }
}
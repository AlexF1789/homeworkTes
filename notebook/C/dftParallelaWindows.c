#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

#define _USE_MATH_DEFINES
#include <math.h>
#include <complex.h>

struct workerArgs {
    float *input, *output;
    int numeroCampioni, k;
};

static DWORD WINAPI sommaContributo(LPVOID args) {
    float complex somma = 0.0;
    struct workerArgs *argomenti = (struct workerArgs *) args;

    for(int n=0; n<argomenti->numeroCampioni; n++)
        somma += argomenti->input[n] * cexp(-I * 2 * M_PI * n * argomenti->k/argomenti->numeroCampioni);

    argomenti->output[argomenti->k] = cabs(somma);
}

int getNumeroProcessori() {
    SYSTEM_INFO sysInfo;

    GetSystemInfo(&sysInfo);
    return sysInfo.dwNumberOfProcessors;
}

void dft(float input[], float output[], int numeroCampioni) {
    HANDLE *threadAttivi;
    struct workerArgs *workerArgs;
    int numProcessori = getNumeroProcessori(), elementiTotali, iterazioniTotali;

    // determiniamo se ha senso far partire l'elaborazione
    if(input == NULL || output == NULL || numProcessori <= 0)
        return;

    // allochiamo la memoria per i thread
    threadAttivi = (HANDLE *) malloc(numProcessori * sizeof(HANDLE));
    workerArgs = (struct workerArgs *) malloc(numProcessori * sizeof(struct workerArgs));

    if(threadAttivi == NULL || workerArgs == NULL) {
        printf("Errore nell'allocazione della memoria!\n");
        return;
    }

    // prepariamo i parametri fissi dei parametri dei worker
    for(int i=0; i<numProcessori; i++) {
        workerArgs[i].input = input;
        workerArgs[i].output = output;
        workerArgs[i].numeroCampioni = numeroCampioni;
    }

    // determiniamo la dimensione sulla quale dovremo calcolare
    if(numeroCampioni % numProcessori == 0) {
        // in questo caso molto fortunato stiamo elaborando un numero di campioni pari
        // a un multiplo intero del numero del numero di processori della macchina
        elementiTotali = numeroCampioni;
    } else {
        // per troncamento otteniamo l'intero più vicino
        elementiTotali = numeroCampioni / numProcessori;

        while(numeroCampioni > elementiTotali) {
            // finché non superiamo il numero di campioni
            elementiTotali += numProcessori;
        }
    }

    // facciamo partire l'elaborazione
    iterazioniTotali = elementiTotali / numProcessori;
    for(int i=0; i<iterazioniTotali; i++) {

        // creiamo i thread
        for(int j=0; j<numProcessori; j++) {
            workerArgs[j].k = i*numProcessori + j;

            if(workerArgs[j].k >= numeroCampioni)
                break;

            if((threadAttivi[j] = CreateThread(NULL, 0, sommaContributo, &workerArgs[j], 0, NULL)) == NULL) {
                printf("Errore nella creazione del thread %d/%d!\n", workerArgs[j].k, numeroCampioni);
                return;
            }
        }

        // effettuiamo la join dei thread prima di riassegnarli ai valori successivi della somma
        WaitForMultipleObjects(numProcessori, threadAttivi, TRUE, INFINITE);

    }

    // liberiamo la memoria
    free(threadAttivi);
    free(workerArgs);
}
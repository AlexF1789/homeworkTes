#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>

#define _USE_MATH_DEFINES
#include <math.h>
#include <complex.h>

struct workerArgs {
    float *input, *output;
    int numeroCampioni, k;
};

static void *sommaContributo(void *args) {
    float complex somma = 0.0;
    struct workerArgs *argomenti = (struct workerArgs *) args;

    for(int n=0; n<argomenti->numeroCampioni; n++)
        somma += argomenti->input[n] * cexp(-I * 2 * M_PI * n * argomenti->k/argomenti->numeroCampioni);

    argomenti->output[argomenti->k] = cabs(somma);
}

void dft(float input[], float output[], int numeroCampioni) {
    pthread_t *threadAttivi;
    struct workerArgs *workerArgs;
    int numProcessori = sysconf(_SC_NPROCESSORS_CONF), elementiTotali, iterazioniTotali;

    // determiniamo se ha senso far partire l'elaborazione
    if(input == NULL || output == NULL || numProcessori <= 0)
        return;

    // allochiamo la memoria per i thread
    threadAttivi = (pthread_t *) malloc(numProcessori * sizeof(pthread_t));
    workerArgs = (struct workerArgs *) malloc(numProcessori * sizeof(struct workerArgs));

    if(threadAttivi == NULL || workerArgs == NULL) {
        printf("Errore nell'allocazione della memoria!\n");
        return;
    }

    printf("Lavoro su %d processori...\n", numProcessori);

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

            if(pthread_create(&threadAttivi[j], NULL, sommaContributo, &workerArgs[j])) {
                printf("Errore nella creazione del thread %d/%d!\n", workerArgs[j].k, numeroCampioni);
                return;
            }
        }

        // effettuiamo la join dei thread prima di riassegnarli ai valori successivi della somma
        for(int j=0; j<numProcessori; j++)
            pthread_join(threadAttivi[j], NULL);

    }

    // liberiamo la memoria
    free(threadAttivi);
    free(workerArgs);
}
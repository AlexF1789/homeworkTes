clc;
clear;
close all;

[y, Fs] = audioread('prova.oga');

% il y(:,2) indica che prendiamo la seconda colonna di y
% visto che l'audio è campionato su 2 canali
%
% il 50 serve per limitare i punti della trasformata a 50
x = fft(y(:,2), 50);

% usiamo stem per creare il grafico
figure
stem(abs(x))

figure
stem(abs(fftshift(x)))

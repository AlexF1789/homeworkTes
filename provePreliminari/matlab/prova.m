clc;
clear;
close all;

graphics_toolkit('gnuplot');

[y, Fs] = audioread('prova.oga');

% il y(:,2) indica che prendiamo la seconda colonna di y
% visto che l'audio è campionato su 2 canali
%
% il 50 serve per limitare i punti della trasformata a 50
x = dft(y(1:150,2));

% usiamo stem per creare il grafico
figure
plot(abs(x))

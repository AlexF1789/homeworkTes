function fourier = dft(segnale)
  % creiamo il segnale
  dimSegnale = length(segnale);
  fourier = zeros(dimSegnale);

  % facciamo la dft
  for k = 1:dimSegnale
    somma = 0;

    for n = 1:dimSegnale
      somma = somma + segnale(n) * exp(-1i * 2 * pi * n * k / dimSegnale);
    endfor

    fourier(k) = somma;
  endfor
end

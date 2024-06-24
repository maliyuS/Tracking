% Spécifications du filtre
ordre = 8;               % Ordre du filtre
fc = 200e3;              % Fréquence de coupure en Hz (200 kHz)
fs = 10e6;                % Fréquence d'échantillonnage en Hz (1 MHz)

% Normalisation de la fréquence de coupure par rapport à la fréquence d'échantillonnage
Wn = fc / (fs / 2);

% Conception du filtre Butterworth
[b, a] = butter(ordre, Wn, 'low');

% Affichage des coefficients du filtre
disp('Coefficients du numérateur (b):');
disp(b);
disp('Coefficients du dénominateur (a):');
disp(a);

% Calcul et affichage de la réponse en fréquence du filtre
[H, f] = freqz(b, a, 1024, fs);

% Tracé de la réponse en fréquence
figure;
plot(f, 20*log10(abs(H)));
title('Réponse en fréquence du filtre Butterworth');
xlabel('Fréquence (Hz)');
ylabel('Amplitude (dB)');
grid on;

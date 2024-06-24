%% 1) Paramètres d'acquisition
% PlutoSDR
Fs = 30e6; % fréquence d'échantillonnage du convertisseur CNA (en émission) et CAN (en réception) du PlutoSDR
Ne = 262144; % Nombre d'échantillons I/Q (ou taille du buffer circulaire qui contient les échantillons pour l'émission/réception du PlutoSDR)

% Vecteur des fréquences pour affichage -fs/2 à fs/2
f = (-Ne/2:Ne/2-1)*(Fs/Ne);

% Création d'une nouvelle fenêtre
figure;

% Paramètres d'affichage
fontsize = 14;
linewidth = 0.1;


%% 2) Télécharger les signaux avec un chemin relatif
Rx0 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx0_IQSamples_24-06-2024_08h52m.csv');
Rx1 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx1_IQSamples_24-06-2024_08h52m.csv');

%% 3) FFT des composantes In-Phase des signaux émis et reçus
% Appliquer une fenêtre de Hanning
window = hanning(Ne);

fft_rx0 = fftshift(abs(fft(Tx0.I.*window)));
fft_rx1 = fftshift(abs(fft(Rx0.I.*window)));

% Normalisation par la somme des fenêtres pour conserver la puissance
fft_rx0 = fft_rx0 / sum(window);
fft_rx1 = fft_rx1 / sum(window);

%% 4) Visualiser les spectres de Rx et Tx
% Tracé de Rx
subplot(2, 1, 1);
hold on;
plot(f, fft_rx0, 'b', 'LineWidth', linewidth, 'Color','r');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Rx0', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-1e6 1e6]);
grid on;

% Tracé de Tx
subplot(2, 1, 2);
hold on;
plot(f, fft_rx1, 'b', 'LineWidth', linewidth, 'Color','b');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Rx1', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-1e6 1e6]);
grid on;

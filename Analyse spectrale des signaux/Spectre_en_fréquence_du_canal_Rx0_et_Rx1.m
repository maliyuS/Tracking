%% 1) Paramètres d'acquisition
% PlutoSDR
Fs = 30e6; % fréquence d'échantillonnage du convertisseur CNA (en émission) et CAN (en réception) du PlutoSDR
Ne = 262144; % Nombre d'échantillons I/Q (ou taille du buffer circulaire qui contient les échantillons pour l'émission/réception du PlutoSDR)
span = 3e6;

% Vecteur des fréquences pour affichage -fs/2 à fs/2
f = (-Ne/2:Ne/2-1)*(Fs/Ne);

% Création d'une nouvelle fenêtre
figure;

% Paramètres d'affichage
fontsize = 14;
linewidth = 0.1;


%% 2) Télécharger les signaux avec un chemin relatif
Rx0 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx0_IQSamples_24-06-2024_09h13m.csv');
Rx1 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx1_IQSamples_24-06-2024_09h13m.csv');

%% 3) FFT des composantes In-Phase des signaux émis et reçus
% Appliquer une fenêtre de Hanning
window = hanning(Ne);

% FFT et normalisation
fft_rx0 = fftshift(abs(fft(Rx0.I .* window)) / sum(window));
fft_rx1 = fftshift(abs(fft(Rx1.I .* window)) / sum(window));

% Conversion des amplitudes en puissances
power_rx0 = fft_rx0.^2;
power_rx1 = fft_rx1.^2;

% Référence de puissance (1 mW pour conversion en dBm)
P_ref = 1e-3;

% Conversion des puissances en dBm
power_rx0_dBm = 10 * log10(power_rx0 / P_ref);
power_rx1_dBm = 10 * log10(power_rx1 / P_ref);

%% 4) Visualiser les spectres de Rx en dBm
figure;

% Tracé de Rx0
subplot(2, 1, 1);
hold on;
plot(f, power_rx0_dBm, 'LineWidth', linewidth, 'Color','r');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Rx0 (dBm)', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude (dBm)', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-span/2 +span/2]);
grid on;

% Tracé de Rx1
subplot(2, 1, 2);
hold on;
plot(f, power_rx1_dBm, 'LineWidth', linewidth, 'Color','b');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Rx1 (dBm)', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude (dBm)', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-span/2 +span/2]);
grid on;

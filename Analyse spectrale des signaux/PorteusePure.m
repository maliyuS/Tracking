%% 1) Paramètres d'acquisition
% PlutoSDR
Fs = 30e6; % fréquence d'échantillonnage du convertisseur CNA (en émission) et CAN (en réception) du PlutoSDR
Pe = 1/Fs; % Période d'échantillonnage
Ne = 256; % Nombre d'échantillons I/Q (ou taille du buffer circulaire qui contient les échantillons pour l'émission/réception du PlutoSDR)

% Télémesure - Prototype:
c = 3e8; % Vitesse de la lumière
Fb = 2e5; % fréquence du signal en bande de base (Data)
Fm = 2.25e9; % fréquence en espace libre du signal modulé
lambda = c/Fm; % Longueur d'onde
d = lambda/2; % Distance entre les éléments du réseau d'antennes

% Vecteur des fréquences pour affichage -fs/2 à fs/2
f = (-Ne/2:Ne/2-1)*(Fs/Ne);

% Création d'une nouvelle fenêtre
figure;

% Paramètres d'affichage
fontsize = 14;
linewidth = 0.1;


%% 2) Télécharger les signaux avec un chemin relatif
porteusePure_2_2502GHz = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\Porteuse pure\2_2502GHz\45°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_45°_porteusePure_2_2502GHz.csv');
porteusePure_2_25001GHz = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\Porteuse pure\2_25001GHz\45°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_45°_porteusePure_2_25001GHz.csv');
porteusePure_2_25GHz = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\Porteuse pure\2_25GHz\45°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_45°_porteusePure_2_25GHz.csv');

%% 3) FFT des composantes In-Phase des signaux émis et reçus
% Appliquer une fenêtre de Hanning
window = hanning(Ne);

fft_porteusePure_2_2502GHz = fftshift(abs(fft(porteusePure_2_2502GHz.I .* window)));
fft_porteusePure_2_25001GHz = fftshift(abs(fft(porteusePure_2_25001GHz.I .* window)));
fft_porteusePure_2_25GHz = fftshift(abs(fft(porteusePure_2_25GHz.I .* window)));

% Normalisation par la somme des fenêtres pour conserver la puissance
fft_porteusePure_2_2502GHz = fft_porteusePure_2_2502GHz / sum(window);
fft_porteusePure_2_25001GHz = fft_porteusePure_2_25001GHz / sum(window);
fft_porteusePure_2_25GHz = fft_porteusePure_2_25GHz / sum(window);

%% 4) Visualiser les spectres de Rx et Tx
% Tracé pour une porteuse à 2.25GHz
subplot(3, 1, 1);
hold on;
plot(f, fft_porteusePure_2_25GHz, 'b', 'LineWidth', linewidth, 'Color','r');
hold off;

% Titre, légende et labels
title("Spectre en sortie de l'ADC - Porteuse Pure à 2.25 GHz", 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
% xlim([-10000 10000]);
grid on;

% Tracé pour une porteuse à 2.25001 GHz
subplot(3, 1, 2);
hold on;
plot(f, fft_porteusePure_2_25001GHz, 'b', 'LineWidth', linewidth, 'Color','b');
hold off;

% Titre, légende et labels
title("Spectre en sortie de l'ADC - Porteuse Pure à 2.25001 GHz", 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
% xlim([-10000 10000]);
grid on;

% Tracé pour une porteuse à 2.2502 GHz
subplot(3, 1, 3);
hold on;
plot(f, fft_porteusePure_2_2502GHz, 'b', 'LineWidth', linewidth, 'Color','b');
hold off;

% Titre, légende et labels
title("Spectre en sortie de l'ADC - Porteuse Pure à 2.2502 GHz", 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
% xlim([-10000 10000]);
grid on;

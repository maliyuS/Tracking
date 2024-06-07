%% 1) Paramètres d'acquisition
% PlutoSDR
Fs = 1e6; % fréquence d'échantillonnage du convertisseur CNA (en émission) et CAN (en réception) du PlutoSDR
Pe = 1/Fs; % Période d'échantillonnage
Ne = 2^14; % Nombre d'échantillons I/Q (ou taille du buffer circulaire qui contient les échantillons pour l'émission/réception du PlutoSDR)

% Télémesure - Prototype:
c = 3e8; % Vitesse de la lumière
Fb = 200; % fréquence du signal en bande de base (Data)
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
Tx0 = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\-40dB\45°\Tx0_IQSamples_-40dB_BufferSize16384_sample_rate1e6_AoA_45°.csv');
Rx0 = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\-40dB\45°\Rx0_IQSamples_-40dB_BufferSize16384_sample_rate1e6_AoA_45°.csv');

%% 3) FFT des composantes In-Phase des signaux émis et reçus
% Appliquer une fenêtre de Hanning
window = hanning(Ne);

fft_tx = fftshift(abs(fft(Tx0.I.*window)));
fft_rx = fftshift(abs(fft(Rx0.I.*window)));

% Normalisation par la somme des fenêtres pour conserver la puissance
fft_tx = fft_tx / sum(window);
fft_rx = fft_rx / sum(window);

%% 4) Visualiser les spectres de Rx et Tx
% Tracé de Rx
subplot(3, 1, 1);
hold on;
plot(f, fft_tx, 'b', 'LineWidth', linewidth, 'Color','r');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Tx', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-10000 10000]);
grid on;

% Tracé de Tx
subplot(3, 1, 2);
hold on;
plot(f, fft_rx, 'b', 'LineWidth', linewidth, 'Color','b');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Rx', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-10000 10000]);
grid on;

%% 5) Calcul du SNR
% Définir la bande passante autour de la fréquence du signal
bandwidth = 0.85 * Fb; % Bande passante à 85%
idx_band_signal = find(f >= (-Fb - bandwidth) & f <= (Fb + bandwidth));

% Puissance du signal reçu (Rx) dans la bande définie
power_signal_rx = sum(fft_rx(idx_band_signal).^2);

% Puissance du bruit (en considérant une bande hors signal)
% Exclure la bande passante autour du signal
noise_band = setdiff(1:Ne, idx_band_signal);
power_noise = mean(fft_rx(noise_band).^2) * length(idx_band_signal);

% Calculer le SNR en dB
SNR_dB = 10 * log10(power_signal_rx / power_noise);

% Afficher les résultats
disp(['Puissance du signal reçu (Rx) : ', num2str(power_signal_rx)]);
disp(['Puissance du bruit (noise) : ', num2str(power_noise)]);
disp(['SNR (dB) : ', num2str(SNR_dB)]);

%% 6) Visualiser le spectre du signal filtré dans la bande de fréquences définie

% Filtrer le signal reçu dans la bande passante
fft_rx_filtered = zeros(size(fft_rx));
fft_rx_filtered(idx_band_signal) = fft_rx(idx_band_signal);

% Tracer le signal filtré
subplot(3, 1, 3);
hold on;
plot(f, fft_rx_filtered, 'b', 'LineWidth', linewidth, 'Color','g');
hold off;

% Titre, légende et labels
title('Spectre en fréquence du canal Rx filtré', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Fréquence (Hz)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis auto;
xlim([-10000 10000]);
grid on;

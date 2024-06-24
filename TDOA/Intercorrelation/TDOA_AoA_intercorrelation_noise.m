% Dans ce code, nous implémentons différents filtres adaptatifs avant
% d'appliquer l'intercorrélation dans le but d'estimer encore plus  
% la TDOA (et donc l'AoA) en fonction des niveaux de SNR. Parmis ceux essayées (Wiener, SCOT, ML qui ne marche pas, ...), l'algorithme
% PHAT (Phase transformation) semble fournir le plus de résultats. En
% effet, la fonction d'intercorrélation semble moins applatit après
% filtrage.

%% 1) Paramètres d'acquisition
% PlutoSDR
Fs = 30e6; % fréquence d'échantillonnage du convertisseur CNA (en émission) et CAN (en réception) du PlutoSDR
Pe = 1/Fs; % Période d'échantillonnage
Ne = 262144; % Nombre d'échantillons I/Q (ou taille du buffer circulaire qui contient les échantillons pour l'émission/réception du PlutoSDR)

% Télémesure - Prototype:
c = 3e8; % Vitesse de la lumière
Fb = 7e5; % fréquence du signal en bande de base (Data)
Fm = 2.25e9; % fréquence en espace libre du signal modulé
lambda = c/Fm; % Longueur d'onde
d = lambda/2; % Distance entre les éléments du réseau d'antennes

% Vecteur temps
tps = linspace(0, (Ne - 1) * Pe * 1e3, Ne); % en ms

% Création d'une nouvelle fenêtre
figure;

% Paramètres d'affichage
fontsize = 14;
linewidth = 0.1;

%% 2) Télécharger les signaux avec un chemin relatif
Rx0 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx0_IQSamples_24-06-2024_14h19m.csv');
Rx1 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx1_IQSamples_24-06-2024_14h19m.csv');

% Extraire les composantes In-Phase (I)
Rx0 = Rx0.I + 1i * Rx0.Q;
Rx1 = Rx1.I + 1i * Rx1.Q;

%% 3) Visualiser des échantillons In-Phase (I) des signaux en entrée de Rx0 et Rx1
% Tracé de la composante In-Phase
subplot(3, 1, 1);
hold on;
plot(tps, real(Rx0), 'b', 'LineWidth', linewidth);
plot(tps, real(Rx1), 'r', 'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Composantes In-Phase de Rx0 et Rx1', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Rx0', 'Rx1', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 4) Calcul de TDOA entre Rx0 et Rx1

% Calculer l'interspectre
S12 = compute_interspectrum(Rx0, Rx1);

% Corrélation croisée à partir de l'interspectre
[acor, lag] = process_intercorr(S12, length(Rx0));

% Trouver l'indice du maximum de la corrélation (réelle)
[~, I] = max(real(acor));

% Retard en secondes
time_delay = lag(I) / Fs;

% Déphasage angulaire en radians
angular_delay = 2 * pi * Fb * time_delay; % On utilise la fréquence du signal en bande de base (Data)

% Ajuster le déphasage dans l'intervalle [-pi, pi]
if angular_delay > pi
    angular_delay = angular_delay - 2*pi;
elseif angular_delay < -pi
    angular_delay = angular_delay + 2*pi;
end

% Déphasage angulaire en degrés (entre -180° et +180°)
angular_delay_degrees = angular_delay * (180 / pi);

% AoA avec une configuration Monopulse de phase
AoA = asin( c * angular_delay / ( 2 * pi * Fm * d ) ) * ( 180 / pi ); % On utilise la fréquence en espace libre du signal modulé

% Afficher les déphasages calculés
fprintf('Time Delay : %f secondes\n', time_delay);
fprintf('Angular Delay : %f degrees\n', angular_delay_degrees);
fprintf('AoA : %f degrees\n', AoA);

%% 5) Visualiser la fonction d'intercorrélation (partie réelle)
subplot(3, 1, 2);
hold on;
plot(real(acor), 'b', 'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Intercorrélation entre Rx0 et Rx1', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Indice', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 6) Appliquer le déphasage au signal Rx1 en utilisant FFT
% Transformer les signaux en domaine fréquentiel
Rx1_I_fft = fft(real(Rx1));

% Calculer le vecteur de phase pour le décalage
phase_shift = exp(-1i * angular_delay);

% Appliquer le décalage de phase
Rx1_I_fft_shifted = Rx1_I_fft .* phase_shift(:);

% Revenir au domaine temporel
Rx1_I_aligned = ifft(Rx1_I_fft_shifted, 'symmetric');

%% 7) Visualiser les signaux après alignement
subplot(3, 1, 3);
hold on;
plot(tps, real(Rx0), 'b', 'LineWidth', linewidth);
plot(tps, Rx1_I_aligned, 'r', 'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Composantes In-Phase de Rx0 et Rx1 après alignement', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Rx0', 'Rx1 aligné', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

function interspectrum = compute_interspectrum(Rx0_I, Rx1_I)

    % Appliquer une fenêtre de Hanning aux signaux
    n = length(Rx0_I);
    w = blackman(n);
    Rx0_IW = Rx0_I .* w;
    Rx1_IW = Rx1_I .* w;

    % Fonction pour calculer la densité spectrale de puissance croisée
    N = length(Rx0_IW);
    M = length(Rx1_IW);
    nfft = 2^nextpow2(N + M - 1); % Longueur de la FFT

    % Calcul de la FFT des signaux
    Rx0_fft = fft(Rx0_IW, nfft);
    Rx1_fft = fft(Rx1_IW, nfft);

    % Calcul de l'interspectre via le produit des spectres conjugués
    interspectrum = Rx0_fft .* conj(Rx1_fft);
end

function [acor2, lag2] = process_intercorr(interspectrum, N)
    % Fonction pour traiter l'intercorrélation
    acor2 = ifft(interspectrum);

    % Découper l'intercorrélation pour avoir la même longueur que lag1
    acor2 = acor2(1:(2*N-1));

    % Centrer l'intercorrélation
    acor2 = fftshift(acor2);

    % Normalisation des résultats
    acor2 = acor2 / max(abs(acor2));

    % Calcul du décalage (lag) correspondant
    lag2 = -N+1:N-1;
end

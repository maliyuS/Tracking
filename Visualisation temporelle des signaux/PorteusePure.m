%% 1) Paramètres d'acquisition
Fs = 30e6; %fréquence d'échantillonage du convertisseur CNA (en émission) et CAN (en réception) du PlutoSDR
Pe = 1/Fs; %Période d'échantillonnage
Ne = 256; %Nombre d'échantillons I/Q (ou taille du buffer circulaire qui contient les échantillons pour l'émission/réception du PlutoSDR)

%Vecteur temps
tps = linspace(0, (Ne - 1) * Pe * 1e3, Ne); %en ms

% Visualiser des échantillons I/Q du signal en sortie de Tx0 (le signal étalon)
figure;

% Paramètres d'affichage
fontsize = 14;
linewidth = 1.5;

%% 2) Télécharger les signaux avec un chemin relatif

porteusePure_2_2502GHz = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\Porteuse pure\2_2502GHz\0°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_0°_porteusePure_2_2502GHz.csv');
porteusePure_2_25001GHz = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\Porteuse pure\2_25001GHz\0°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_0°_porteusePure_2_25001GHz.csv');
porteusePure_2_25GHz = readtable('C:\Users\MORISSET\OneDrive\Bureau\DATA\COURS\5A\Stage\Travaux\RF\MatLab\recordings\Porteuse pure\2_25GHz\0°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_0°_porteusePure_2_25GHz.csv');


%% 3) Visualiser les échantillons I/Q en sortie du Pluto pour une porteuse pure à 2.25GHz
%Tracé des composantes In-Phase et Q-Phase
subplot(3, 1, 1);
hold on;
plot(tps, porteusePure_2_25GHz.I, 'b', 'LineWidth', linewidth);
plot(tps, porteusePure_2_25GHz.Q, 'r',  'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Porteuse Pure à 2.25 GHz', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 4) Visualiser les échantillons I/Q en sortie du Pluto pour une porteuse pure à 2.25001GHz

%Tracé des composantes In-Phase et Q-Phase
subplot(3, 1, 2);
hold on;
plot(tps, porteusePure_2_25001GHz.I, 'b');
plot(tps, porteusePure_2_25001GHz.Q, 'r');
hold off;

% Titre, légende et labels
title('Porteuse Pure à 2.25001 GHz', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 5) Visualiser les échantillons I/Q en sortie du Pluto pour une porteuse pure à 2.2502GHz

%Tracé des composantes In-Phase et Q-Phase
subplot(3, 1, 3);
hold on;
plot(tps, porteusePure_2_2502GHz.I, 'b');
plot(tps, porteusePure_2_2502GHz.Q, 'r');
hold off;

% Titre, légende et labels
title('Porteuse Pure à 2.2502 GHz', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

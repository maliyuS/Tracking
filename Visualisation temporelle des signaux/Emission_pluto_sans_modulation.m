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
Rx0 = readtable('C:\Users\DEV\Desktop\Samuel\MatLab\recordings\Porteuse pure\2_25GHz\0°\Rx0_IQSamples_-40dBm_BufferSize256_sample_rate30e6_AoA_0°_porteusePure_2_25GHz.csv');
Rx1 = readtable('C:\Users\DEV\Desktop\Samuel\MatLab\recordings\Porteuse pure\');
Tx0 = readtable('C:\Users\DEV\Desktop\Samuel\MatLab\recordings\Fco=200Khz\-3dB\0°\Tx0_IQSamples_-3dB_BufferSize256_sample_rate30e6_AoA_0°.csv');
intercorr = readtable('C:\Users\DEV\Desktop\Samuel\MatLab\recordings\Fco=2MHz\-40dB\45°\Intercorrélation_-40dB_BufferSize16384_sample_rate1e6_AoA_45°.csv');
corr = intercorr.Var1;
lag = intercorr.Var2;

intercorr_apres_filtrage = readtable('C:\Users\DEV\Desktop\Samuel\MatLab\recordings\Fco=2MHz\-80dB\45°\Intercorrelation_apres_filtrage.csv');
corr_apres_filtrage = intercorr_apres_filtrage.acor;
lag_apres_filtrage = intercorr_apres_filtrage.lag;

%% 3) Visualiser des échantillons I/Q du signal en sortie de Tx0 (le signal étalon)
%Tracé des composantes In-Phase et Q-Phase
subplot(3, 2, 1);
hold on;
plot(tps, Tx0.I, 'b', 'LineWidth', linewidth);
plot(tps, Tx0.Q, 'r',  'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Signal Tx0', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 4) Visualiser des échantillons I/Q du signal en sortie de Rx0 (le signal étalon)

%Tracé des composantes In-Phase et Q-Phase
subplot(3, 2, 2);
hold on;
plot(tps, Rx0.I, 'b');
plot(tps, Rx0.Q, 'r');
hold off;

% Titre, légende et labels
title('Signal Rx0', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 5) Visualiser des échantillons I/Q du signal en sortie de Rx1 (le signal étalon)

%Tracé des composantes In-Phase et Q-Phase
subplot(3, 2, 3);
hold on;
plot(tps, Rx1.I, 'b');
plot(tps, Rx1.Q, 'r');
hold off;

% Titre, légende et labels
title('Signal Rx1', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;


%% 6) Visualiser la fonction d'intercorrelation

% Tracé des composantes In-Phase et Q-Phase
subplot(3, 2, 4);
hold on;
plot(lag, corr, 'b');
hold off;

% Titre, légende et labels
title('Fonction d intercorrelation', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%% 7) Visualiser la fonction d'intercorrelation après filtrage

% Tracé des composantes In-Phase et Q-Phase
subplot(3, 2, 5);
hold on;
plot(lag_apres_filtrage, corr_apres_filtrage, 'b');
hold off;

% Titre, légende et labels
title('Fonction d intercorrelation après filtrage passe-bas', 'FontSize', fontsize, 'FontWeight', 'bold');
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

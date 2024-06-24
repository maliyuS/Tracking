%% 1) Paramètres d'acquisition
Fs = 30e6; %fréquence d'échantillonage du convertisseur CAN
Ne = 262144; %Nombre d'échantillons I/Q
Fb = 30e6;
Pe = 1 / Fb;

%Vecteur temps
tps = linspace(0, (Ne - 1) * Pe * 1e3, Ne); %en ms

% Visualiser des échantillons I/Q du signal en sortie de Tx0 (le signal étalon)
figure;

% Paramètres d'affichage
fontsize = 14;
linewidth = 1.5;

%% 2) Télécharger les signaux avec un chemin relatif
Rx0 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx0_IQSamples_24-06-2024_08h52m.csv');
Rx1 = readtable('C:\Users\DEV\Desktop\Samuel\démo3_28_05_2024\recordings_temp\Rx1_IQSamples_24-06-2024_08h52m.csv');

%% 3) Visualiser les échantillons I/Q après le CAN

%ts = timescope('SampleRate', Fs, 'TimeSpan', Ne / Fs , 'AxesScaling', 'auto');
%ts(Rx0.I, Rx0.Q);

% Tracé des composantes In-Phase et Q-Phase
subplot(2, 1, 1);
hold on;
plot(tps, Rx0.I, 'b', 'LineWidth', linewidth);
plot(tps, Rx0.Q, 'r',  'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Signal Rx0', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);
xlim([0 0.02]);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

%Tracé des composantes In-Phase et Q-Phase
subplot(2, 1, 2);
hold on;
plot(tps, Rx1.I, 'b', 'LineWidth', linewidth);
plot(tps, Rx1.Q, 'r',  'LineWidth', linewidth);
hold off;

% Titre, légende et labels
title('Signal Rx1', 'FontSize', fontsize, 'FontWeight', 'bold');
legend('Composante In-Phase', 'Composante Q-Phase', 'FontSize', fontsize);
xlabel('Temps (ms)', 'FontSize', fontsize);
ylabel('Amplitude', 'FontSize', fontsize);
xlim([0 0.02]);

% Ajustement des axes et ajout d'une grille
axis tight;
grid on;

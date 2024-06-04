import numpy as np
import time


########################################################################################################################
########################################### MATHEMATICS Tools ##########################################################
########################################################################################################################
def compute_interspectrum(Rx0, Rx1):
    """
    Fonction pour calculer la densité spectrale de puissance croisée (interspectre).
    Arguments:
    - Rx0_I: Signal 1.
    - Rx1_I: Signal 2.

    Renvoie:
    - interspectrum: L'interspectre des signaux.
    """

    # Appliquer une fenêtre de Blackman aux signaux
    n = len(Rx0)
    w = np.blackman(n)
    Rx0 = Rx0 * w
    Rx1 = Rx1 * w

    # Calculer la longueur de la FFT
    N = len(Rx0)
    M = len(Rx1)
    nfft = 2 ** np.ceil(np.log2(N + M - 1)).astype(int)

    # Calcul de la FFT des signaux
    Rx0_fft = np.fft.fft(Rx0, nfft)
    Rx1_fft = np.fft.fft(Rx1, nfft)

    # Calcul de l'interspectre via le produit des spectres conjugués
    interspectrum = Rx0_fft * np.conj(Rx1_fft)

    return interspectrum


########################################################################################################################
def process_intercorr(interspectrum, N):
    """
    Fonction pour traiter l'intercorrélation.
    Arguments:
    - interspectrum: Le spectre d'intercorrélation.
    - N: La moitié de la longueur de la fenêtre d'observation.

    Renvoie:
    - acor2: L'intercorrélation normalisée.
    - lag2: Les décalages (lags) correspondants.
    """
    # Calculer l'intercorrélation en utilisant la transformée de Fourier inverse
    acor2 = np.fft.ifft(interspectrum)

    # Découper l'intercorrélation pour avoir la même longueur que lag1
    acor2 = acor2[:2 * N - 1]

    # Centrer l'intercorrélation
    acor2 = np.fft.fftshift(acor2)

    # Normalisation des résultats
    acor2 = acor2 / np.max(np.abs(acor2))

    # Calcul du décalage (lag) correspondant
    lag2 = np.arange(-N + 1, N)

    return acor2, lag2


########################################################################################################################
def compute_TDOA(Rx0, Rx1, Fs, Fb, Ne):
    """
    Fonction pour calculer la différence de temps d'arrivée (TDOA) entre deux signaux.
    Arguments:
    - Rx0: Signal 1 (I + jxQ).
    - Rx1: Signal 2 (I + jxQ).
    - Fs: Fréquence d'échantillonnage.
    - Fb: Fréquence du signal en bande de base.
    - Ne: Nombre d'échantillons (ou taille du buffer).

    Renvoie:
    - angular_delay : Le déphasage angulaire entre les signaux en radians.
    """
    # Calcul de l'intercorrélation entre les signaux Rx0 et Rx1 à l'aide de la densité spectrale de puissance croisée
    interspectrum = compute_interspectrum(Rx0, Rx1)
    acor2, lag2 = process_intercorr(interspectrum, Ne)

    # Trouver le décalage (lag) correspondant à la valeur maximale de l'intercorrélation
    max_acor2_index = np.argmax(np.real(acor2))
    max_lag2 = lag2[max_acor2_index]

    # Retard en secondes
    time_delay = max_lag2 / Fs

    # Déphasage angulaire en radians
    angular_delay = 2 * np.pi * Fb * time_delay

    # Ajuster le déphasage dans l'intervalle [-pi, pi]
    if angular_delay > np.pi:
        angular_delay = angular_delay - 2 * np.pi
    elif angular_delay < -np.pi:
        angular_delay = angular_delay + 2 * np.pi

    # Déphasage angulaire en degrés (entre -180° et +180°)
    angular_delay_degrees = angular_delay * (180 / np.pi)

    # Afficher les déphasages calculés
    print(f'Time Delay : {time_delay:.10f} secondes')
    print(f'Angular Delay : {angular_delay_degrees:.6f} degrees')

    return angular_delay


########################################################################################################################
############################################# Time Counter #############################################################
########################################################################################################################
class CallCounter:
    """Cette classe compte le nombre d'appel à une fonction chaque seconde"""

    def __init__(self):
        self.start_time = time.time()  # Mémoriser l'heure de début correctement
        self.count = 0  # Compteur d'appels

    def __call__(self, *args, **kwargs):
        # Appel de la fonction : ici, nous incrémentons juste le compteur
        self.count += 1

        # Calculer le temps écoulé depuis le début
        elapsed_time = time.time() - self.start_time

        # Si plus d'une seconde s'est écoulée, afficher le nombre d'appels et réinitialiser
        if elapsed_time >= 1:
            print(f"Nombre d'appels en une seconde : {self.count}")
            # Réinitialiser le compteur et l'heure de début
            self.start_time = time.time()
            self.count = 0


########################################################################################################################
################################################ AoA estimator for Monopulse Tracking Set Up ###########################
########################################################################################################################

class MonopulseAngleEstimator:
    def __init__(self, phase_cal=0, window_size=25,  fs=None, fb=None, fm=None, d=None, ne=None):
        self.window_size = window_size  # Taille de la fenêtre pour le moyennage
        self.window_values = []  # Liste pour stocker les valeurs de la fenêtre
        self.phase_cal = phase_cal  # Calibration de phase additionnelle
        self.Fs = fs  # Fréquence d'échantillonnage
        self.Fb = fb  # Fréquence du signal en bande de base
        self.Fm = fm  # Fréquence du signal modulé
        self.d = d  # Distance entre les éléments du réseau d'antennes
        self.Ne = ne  # Nombre d'échantillons (ou taille du buffer)

    def add_sample(self, sample_value):
        """Ajoute un échantillon à la fenêtre et gère la taille de la fenêtre."""
        self.window_values.append(sample_value)
        # Maintenir la taille de la fenêtre
        if len(self.window_values) > self.window_size:
            self.window_values.pop(0)  # Supprimer le plus ancien échantillon

    def is_window_full(self):
        """Vérifie si la fenêtre contient assez d'échantillons pour le calcul."""
        return len(self.window_values) == self.window_size

    def get_average(self):
        """Calcule la moyenne des valeurs de la fenêtre si elle est pleine."""
        if self.is_window_full():
            return sum(self.window_values) / len(self.window_values)
        return None  # Fenêtre pas encore pleine, pas de moyenne disponible

    def count_distinct_values(self):
        """Retourne le nombre de valeurs distinctes et leurs occurrences sous forme de tableau 2D."""
        value_counts = {}
        for value in self.window_values:
            if value in value_counts:
                value_counts[value] += 1
            else:
                value_counts[value] = 1
        # Convertir le dictionnaire en tableau 2D
        distinct_table = [[key, value] for key, value in value_counts.items()]
        return distinct_table

    def calcTheta(self, angular_delay, d, Fm, phase_cal):
        """
        Calcule l'angle de direction (theta) pour un signal reçu par un réseau d'antennes,
        basé sur la différence de phase mesurée entre les antennes dans une configuration monopulse de phase.

        Paramètres:
        - angular_delay : La différence de phase en degrés entre les signaux reçus par les antennes.
        - d : La distance entre les éléments du réseau d'antennes (en mètres).
        - Fm : La fréquence du signal modulé reçu par les antennes (en Hz).

        Retourne:
        - L'angle de direction theta en degrés.

        Formule utilisée:
        theta = arcsin(c * deltaphase / (2 * pi * f * d))
        où c est la vitesse de la lumière (approximativement 3E8 m/s).

        Remarques:
        - Le déphasage entre les deux signaux modulés est conservé après la démodulation,
          ce qui permet de mesurer le déphasage en bande de base.
        - La fréquence Fm est utilisée dans la formule pour calculer le retard
          qui s'est produit lorsque l'onde se propageait en espace libre.
        """

        C = 3E8  # Vitesse de la lumière en mètres par seconde

        # Conversion de la différence de phase de degrés en radians pour le calcul
        arcsin_arg = angular_delay * C / (2 * np.pi * Fm * d)

        # Calcul de l'angle theta en degrés à partir de l'argument arcsin
        calc_theta = np.rad2deg(np.arcsin(arcsin_arg)) + phase_cal

        print(f'AoA (Average) : {calc_theta:.6f} degrees')

        return calc_theta

########################################################################################################################
    def scan_for_DOA(self, newRx0, newRx1):
        """
        Fonction pour calculer l'angle de direction (AoA) entre deux signaux reçus par un réseau d'antennes,
        basé sur la différence de temps d'arrivée (TDOA) mesurée entre les signaux.

        Arguments:
        - Rx0: Signal 1 (I + jxQ).
        - Rx1: Signal 2 (I + jxQ).
        - Fs: Fréquence d'échantillonnage.
        - Fb: Fréquence du signal en bande de base.
        - Ne: Nombre d'échantillons (ou taille du buffer).
        - d: Distance entre les éléments du réseau d'antennes (en mètres).
        - Fm: Fréquence du signal modulé reçu par les antennes (en Hz).

        Renvoie:
        - AoA : L'angle de direction entre les signaux en degrés.
        """
        # Calcul de la TDOA entre les signaux Rx0 et Rx1 par corrélation
        angular_delay = compute_TDOA(newRx0, newRx1, self.Fs, self.Fb, self.Ne)

        # Appliquer un moyennage sur les déphasages angulaires
        self.add_sample(angular_delay)
        if not self.is_window_full():
            return None  # Pas de moyenne disponible tant que la fenêtre n'est pas pleine

        else:
            # Calculer la moyenne des déphasages angulaires
            average_angular_delay = self.get_average()

            # AoA avec une configuration Monopulse de phase
            return self.calcTheta(average_angular_delay, self.d, self.Fm, self.phase_cal)

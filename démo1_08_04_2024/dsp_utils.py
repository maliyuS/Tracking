import numpy as np
import time

########################################################################################################################

def calcTheta(deltaphase, d, rx_lo):
    """
    Calcule l'angle de direction (theta) pour un signal reçu par un réseau d'antennes,
    basé sur la différence de phase mesurée entre les antennes.

    Paramètres:
    - deltaphase : La différence de phase en degrés entre les signaux reçus par les antennes.
    - d : La distance entre les éléments du réseau d'antennes (en mètres).
    - rx_lo : La fréquence du signal reçu (en Hz).

    Retourne:
    - L'angle de direction theta en degrés.

    Formule utilisée:
    theta = arcsin(c * deltaphase / (2 * pi * f * d))
    où c est la vitesse de la lumière (approximativement 3E8 m/s).

    Remarques:
    - Le déphasage entre les deux signaux modulés est conservé après la démodulation,
      ce qui permet de mesurer le déphasage en bande de base.
    - La fréquence rx_lo est utilisée dans la formule pour calculer le retard
      qui s'est produit lorsque l'onde se propageait en espace libre.
    """

    C = 3E8  # Vitesse de la lumière en mètres par seconde

    # Conversion de la différence de phase de degrés en radians pour le calcul
    arcsin_arg = np.deg2rad(deltaphase) * C / (2 * np.pi * rx_lo * d)

    # Assurez-vous que l'argument pour arcsin reste entre -1 et 1 pour éviter les erreurs
    arcsin_arg = max(min(1, arcsin_arg), -1)

    # Calcul de l'angle theta en degrés à partir de l'argument arcsin
    calc_theta = np.rad2deg(np.arcsin(arcsin_arg))

    return calc_theta


########################################################################################################################

def fft(raw_data):
    """
    Convertit un tableau d'échantillons IQ en un spectre de fréquence, exprimé en dBFS.

    Paramètres:
    - raw_data (array): Tableau de données IQ complexes.

    Retourne:
    - s_dbfs (array): Spectre de fréquence.
    """
    # Nombre d'échantillons dans les données brutes
    NumSamples = len(raw_data)

    # Fenêtrage Hamming pour réduire les fuites spectrales
    win = np.hamming(NumSamples)

    # Application de la fenêtre aux données
    y = raw_data * win

    # Calcul de la FFT normalisée par la somme de la fenêtre
    s_fft = np.fft.fft(y) / np.sum(win)

    # Décalage zéro-fréquence au centre du spectre
    s_shift = np.fft.fftshift(s_fft)

    return s_shift


########################################################################################################################

def dbfs(s_shift):
    """
    Normalise un spectre par rapport à la pleine échelle (dBFS).

    Arguments:
    s_shift (array) : Spectre de fréquence complexe.

    Retourne:
    s_dbfs (array) : Spectre en dBFS.

    Note:
    Le PlutoSDR intègre un ADC qui quantifie les données sur 12 bits, donc la pleine échelle
    est considérée comme 2^11.
    """
    full_scale = 2 ** 11

    return 20 * np.log10(np.abs(s_shift) / full_scale)


########################################################################################################################
def monopulse_angle(sum_signal, delta_signal):
    """
    Estime la différence d'angle entre deux signaux en utilisant la corrélation temporelle.

    Arguments:
    - sum_signal (array): Le signal somme, représentant la combinaison de deux ou plusieurs signaux.
    - delta_signal (array): Le signal delta, généralement la différence entre les mêmes signaux utilisés dans sum_signal.

    Retourne:
    - angle_diff (float): L'angle de différence estimé entre les signaux, en radians.

    La fonction calcule la corrélation entre les signaux sum et delta dans le domaine temporel.
    La méthode 'valid' de corrélation est utilisée, ce qui signifie que la corrélation est calculée là où les signaux se chevauchent complètement.
    L'angle de la corrélation résultante est ensuite calculé pour estimer la différence d'angle.
    """

    # Calculer la corrélation temporelle entre sum_signal et delta_signal
    # Utilisation de 'valid' pour obtenir la corrélation là où les deux signaux se chevauchent entièrement
    sum_delta_correlation = np.correlate(sum_signal, delta_signal, 'valid')

    # Calculer l'angle de la corrélation résultante
    # np.angle retourne l'angle phase de ce nombre complexe, ici de la valeur complexe résultant de la corrélation
    angle_diff = np.angle(sum_delta_correlation)

    return angle_diff


########################################################################################################################

def scan_for_DOA(Rx_0, Rx_1, phase_cal, d, rx_lo):
    """
    Estime l'angle d'arrivée (DOA) en utilisant la somme et la différence des signaux reçus par deux antennes.

    Arguments:
    - Rx_0 (array): Signal reçu par la première antenne.
    - Rx_1 (array): Signal reçu par la seconde antenne.
    - phase_cal (float): Calibration de phase pour ajuster les erreurs potentielles dans le système de mesure.

    Retourne:
    - delay_phases (array): Les déphasages testés.
    - peak_dbfs (float): La valeur maximale de dBFS obtenue par sommation cohérente des signaux.
    - peak_delay (float): Le déphasage correspondant au pic maximum.
    - steer_angle (int): L'angle estimé d'arrivée en degrés.
    - peak_sum (list): Les valeurs de pic pour chaque sommation de signaux.
    - peak_delta (list): Les valeurs de pic pour chaque différence de signaux.
    - monopulse_phase (list): La phase estimée pour chaque déphasage.
    """

    # Initialisation des listes pour stocker les résultats des pics et des phases
    peak_sum = []
    peak_delta = []
    monopulse_phase = []

    # Création d'une plage de déphasages possibles, de -180 à 178 degrés par pas de 2 degrés
    delay_phases = np.arange(-180, 180, 2)

    for phase_delay in delay_phases:
        # Application du déphasage avec calibration au signal Rx_1
        delayed_Rx_1 = Rx_1 * np.exp(1j * np.deg2rad(phase_delay + phase_cal))

        # Calcul de la somme et de la différence des signaux
        delayed_sum = Rx_0 + delayed_Rx_1
        delayed_delta = Rx_0 - delayed_Rx_1

        # FFT des signaux sommés et différenciés
        delayed_sum_fft = fft(delayed_sum)
        delayed_delta_fft = fft(delayed_delta)

        # Conversion des spectres FFT en dBFS
        delayed_sum_dbfs = dbfs(delayed_sum_fft)
        delayed_delta_dbfs = dbfs(delayed_delta_fft)

        # Estimation de l'angle à partir de la corrélation des signaux sommés et différenciés
        mono_angle = monopulse_angle(delayed_sum, delayed_delta)

        # Stockage des pics et des phases
        peak_sum.append(np.max(delayed_sum_dbfs))
        peak_delta.append(np.max(delayed_delta_dbfs))
        monopulse_phase.append(np.sign(mono_angle))

    # Trouver le déphasage donnant le pic maximal de dBFS pour les signaux sommés
    peak_dbfs = np.max(peak_sum)
    peak_delay_index = np.where(peak_sum == peak_dbfs)
    peak_delay = delay_phases[peak_delay_index[0][0]]

    # Calcul de l'angle de direction basé sur le déphasage optimal
    steer_angle = int(calcTheta(peak_delay, d, rx_lo))

    return {'delay_phases': delay_phases,
            'peak_dbfs': peak_dbfs,
            'peak_delay': peak_delay,
            'steer_angle': steer_angle,
            'peak_sum': peak_sum,
            'peak_delta': peak_delta,
            'monopulse_phase': monopulse_phase
            }

########################################################################################################################
def scan_for_DOAV2(Rx_0, Rx_1, phase_cal, d, rx_lo):
    """
    Estime l'angle d'arrivée (DOA) en utilisant la somme et la différence des signaux reçus par deux antennes.

    Arguments:
    - Rx_0 (array): Signal reçu par la première antenne.
    - Rx_1 (array): Signal reçu par la seconde antenne.
    - phase_cal (float): Calibration de phase pour ajuster les erreurs potentielles dans le système de mesure.

    Retourne:
    - delay_phases (array): Les déphasages testés.
    - peak_dbfs (float): La valeur maximale de dBFS obtenue par sommation cohérente des signaux.
    - peak_delay (float): Le déphasage correspondant au pic maximum.
    - steer_angle (int): L'angle estimé d'arrivée en degrés.
    - peak_sum (list): Les valeurs de pic pour chaque sommation de signaux.
    - peak_delta (list): Les valeurs de pic pour chaque différence de signaux.
    - monopulse_phase (list): La phase estimée pour chaque déphasage.
    """
    print("Rx_0", Rx_0)
    print("Rx_1", Rx_1)
    # Calcul de la fonction d'intercorrélation complète
    Correlation = np.correlate(Rx_0, Rx_1, 'full')
    print("Correlation", Correlation)

    # Calcul de la fonction d'intercorrélation complète
    Correlation = np.correlate(Rx_0, Rx_1, 'full')

    # Trouver l'indice du pic de corrélation en fonction de la magnitude
    peak_index = np.argmax(np.abs(Correlation))

    # Extraire le décalage temporel
    delay = peak_index - (len(Rx_1) - 1)

    # Calculer le déphasage au pic
    peak_correlation_value = Correlation[peak_index]
    phase_difference = np.angle(peak_correlation_value)

    # Convertir de radians en degrés
    phase_difference_degrees = np.degrees(phase_difference)

    print("Décalage temporel :", delay)
    print("Déphasage (en degrés) :", phase_difference_degrees)

    return {'delay_phases': 0,
            'peak_dbfs': 0,
            'peak_delay': 0,
            'steer_angle': 0,
            'peak_sum': 0,
            'peak_delta': 0,
            'monopulse_phase': 0
            }

########################################################################################################################
#Cette classe permet dévaluer le nombre d'itération réalisé chaque seconde pour l'appel à une fonction
class CallCounter:
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
class SlidingWindowAverager:
    def __init__(self):
        self.window_size = 3
        self.window_values = []
        self.is_full = False

    def add_sample(self, sample_values):
        self.window_values.append(sample_values)
        if len(self.window_values) > self.window_size:
            self.window_values = self.window_values[-self.window_size:]
        self.is_full = len(self.window_values) == self.window_size

    def is_window_full(self):
        return self.is_full

    def get_average(self):
        if self.is_full:
            num_samples = len(self.window_values)
            num_dimensions = len(self.window_values[0])  # Nombre de dimensions dans les échantillons
            sums = {key: 0 for key in self.window_values[0]}  # Initialiser la somme pour chaque clé à 0
            # Calculer la somme de chaque dimension pour tous les échantillons
            for values in self.window_values:
                for key, value in values.items():
                    if isinstance(value, list):  # Vérifier si la valeur est une liste
                        sums[key] += sum(value)  # Ajouter la somme des éléments de la liste
                    else:
                        sums[key] += value
            # Calculer la moyenne pour chaque dimension
            averages = {key: sum_value / num_samples for key, sum_value in sums.items()}
            return averages
        else:
            return None  # Fenêtre pas encore pleine, pas de moyenne disponible

########################################################################################################################


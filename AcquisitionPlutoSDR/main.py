import threading
import pyarrow as pa
import pyarrow.parquet as pq
import adi
import datetime
import warnings
import os
import numpy as np
import csv

import pandas as pd

warnings.filterwarnings('default')


class CustomSDR(adi.ad9361):
    def __init__(self, uri):
        # Initialise la classe parente avec l'URI spécifié
        super().__init__(uri=uri)

        # Initialiser la variable de classe qui contiendra les échantillons concaténés
        self.Rx0_combined_samples = np.array([], dtype=complex)
        self.Rx1_combined_samples = np.array([], dtype=complex)

        """ Experience properties """
        # Nous avons un signal utile de largeur de bande 1 MHz centré à 2.25 GHz qui arrive sur le Pluto
        self.bandwidth_signal = 1e6
        self.f0 = 2.25e9  # Fréquence centrale du signal utile
        self.fi = int(7e5)  # Fréquence centrale après hétérodynage

        """Set PlutoSDR Hardware properties"""
        # Rx
        self.rx_lo = int(self.f0 - self.fi)  # use 2.25e9
        self.rx_mode = "manual"  # can be "manual" or "slow_attack"
        self.rx_gain0 = int(40)
        self.rx_gain1 = int(40)
        self.rx_fc = int(self.fi + self.bandwidth_signal / 2)  # Fréquence de coupure du filtrage passe-bas

        # Tx
        self.tx_lo = int(5e8)  # Pour désactiver le Tx, on met la fréquence à 500 MHz
        self.tx_gain0 = -88  # Pour désactiver le Tx, on met le gain à -88
        self.tx_gain1 = -88  # Pour désactiver le Tx, on met le gain à -88
        self.tx_fc = int(2e5)  # Pour désactiver le Tx, on met la fréquence à 200 kHz

        # Sampling
        self.sample_rate = 30e6  # must be <=30.72 MHz if both channels are enabled
        self.buffer_size = 2 ** 18  # (ou nombre d'échantillons) possibilité de 2 ** 18
        self.kernel_buffers_count = 1

    ########################################################################################################################
    ######################################### CONFIGURE SDR PROPERTIES #####################################################

    def configure_rx_properties(self):
        """
        Configures various properties for the Rx (receive) path of the Pluto SDR.
        This includes enabling channels, setting bandwidth, local oscillator frequency,
        gain control mode, and hardware gains for two channels.

        Args:
            fc0 (float): The center frequency to set the bandwidth around.
            rx_lo (float): The local oscillator frequency for the Rx path.
            rx_mode (str): The gain control mode (e.g., 'manual', 'slow_attack').
            rx_gain0 (int): The hardware gain for channel 0.
            rx_gain1 (int): The hardware gain for channel 1.
        """
        # Enable Rx channels 0 and 1
        self.rx_enabled_channels = [0, 1]

        # Set the Rx RF bandwidth, usually around three times the center frequency
        self.rx_rf_bandwidth = int(self.rx_fc * 1.5)  # On rajoute un "roll-off" de 1.5

        # Set the local oscillator frequency for the Rx path
        self.rx_lo = int(self.rx_lo)

        # Set the gain control mode
        self.gain_control_mode = self.rx_mode

        # Set the hardware gain for Rx channel 0
        self.rx_hardwaregain_chan0 = int(self.rx_gain0)

        # Set the hardware gain for Rx channel 1
        self.rx_hardwaregain_chan1 = int(self.rx_gain1)

    def configure_tx_properties(self):
        """
        Configures various properties for the Tx (transmit) path of the Pluto SDR.
        This includes setting the RF bandwidth, local oscillator frequency, cyclic buffer
        activation, hardware gains for two channels, and the buffer size for transmission.

        Args:
            fc0 (float): The center frequency around which to set the bandwidth.
            tx_lo (float): The local oscillator frequency for the Tx path.
            tx_gain (int): The hardware gain for Tx channel 0.
            tx_gain1 (int): The hardware gain for Tx channel 1, default is -88.
            buffer_size (int): The size of the transmission buffer, default is 2^18.
        """

        # Enable Tx channels 0 and 1
        self.tx_enabled_channels = []

        # Set the Tx RF bandwidth, usually around three times the center frequency
        self.tx_rf_bandwidth = int(self.tx_fc * 1.5)

        # Set the local oscillator frequency for the Tx path
        self.tx_lo = int(self.tx_lo)

        # Set the hardware gain for Tx channel 0
        self.tx_hardwaregain_chan0 = int(self.tx_gain0)

        # Set the hardware gain for Tx channel 1
        self.tx_hardwaregain_chan1 = int(self.tx_gain1)

    def configure_sampling_properties(self):
        """Configures various properties for the Sampling of the Pluto SDR.
        This includes setting sampling rate, buffer_size, etc"""

        self.rx_buffer_size = int(self.buffer_size)  # Set the buffer size for the reception buffer
        self.tx_buffer_size = int(self.buffer_size)  # Set the buffer size for the transmission buffer

        self.tx_cyclic_buffer = True  # Enable cyclic buffer for continuous transmission

        self._rxadc.set_kernel_buffers_count(
            self.kernel_buffers_count)  # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto

    def display_parameters(self):
        """
        Displays the parameters of the SDR system including frequencies, bandwidth,
        sampling rate, number of samples, optimized distance between Rx antennas,
        and gains for both Rx and Tx antennas. The output values are formatted in
        human-readable units such as GHz, kHz, MHz, mm, and number of samples.
        """
        print("Fréquence RX et TX: ", int(self.rx_lo / 1_000_000), "GHz")
        print("Bande passante : ", int((self.rx_fc * 3) / 1_000), "kHz")
        print("Echantillonnage : ", int(self.sample_rate / 1_000_000), "MHz")
        print("Nombre d'échantillons : ", int(self.buffer_size))
        print("Start : ", int(self.buffer_size * 1000 * (self.sample_rate / 2 + self.rx_fc / 2) / self.sample_rate),
              "KHz")
        print("Start : ", int(self.buffer_size * 1000 * (self.sample_rate / 2 + self.rx_fc * 2) / self.sample_rate),
              "KHz")
        print("Gain RX0 : ", int(self.rx_gain0))
        print("Gain RX1 : ", int(self.rx_gain1))
        print("Gain TX0 : ", int(self.tx_gain0))

    ########################################################################################################################
    ################################################## RECEIVE DATA ########################################################

    def receive_data(self):
        """
        Recevoir des données du SDR.

        Cette fonction retourne un tableau de données où chaque élément
        est un échantillon de signal discret et complexe (composantes I et Q) sous la forme: Rx = I + jQ.

        Retours:
            tuple: Un tuple contenant les données des deux canaux.
                   Rx_0 représente les données du premier canal,
                   Rx_1 représente les données du second canal.
        """
        # Appel de la méthode Rx() de l'objet SDR pour recevoir des données
        data = self.rx()

        return {'Rx_0': data[0], 'Rx_1': data[1]}

    def calibrate_rx(self):
        """
        Calibrates the SDR receiver by capturing data multiple times.

        Args:
            sdr: An instance of the SDR device (e.g., a PlutoSDR object) with a 'rx' method.
        """
        for i in range(20):
            # Let the SDR device run for a bit to perform all necessary calibrations
            self.receive_data()

    def end_transmission(self):
        """
        Termine la transmission en détruisant le tampon de transmission du SDR.
        """
        try:
            self.tx_destroy_buffer()
            print("Le tampon de transmission a été détruit avec succès.")
        except Exception as e:
            print(f"Erreur lors de la destruction du tampon de transmission : {e}")

########################################################################################################################
################################################## SAVE DATA ###########################################################

    def check_and_save_samples(self, max_size_bytes=500):
        """
        Vérifie si la taille combinée des échantillons Rx0 et Rx1 dépasse max_size_bytes.
        Si oui, sauvegarde les échantillons dans un fichier CSV et réinitialise les tableaux.

        Paramètre:
            max_size_bytes (int): Taille maximale autorisée en octets pour les échantillons combinés.
        """
        # Préparer les données à écrire
        combined_data = np.column_stack((np.real(self.Rx0_combined_samples), np.imag(self.Rx0_combined_samples), np.real(self.Rx1_combined_samples), np.imag(self.Rx1_combined_samples)))
        header = 'Rx0_I, Rx0_Q, Rx1_I, Rx1_Q'

        # Calculer la taille des échantillons combinés en bytes
        current_size = combined_data.nbytes / (1024 ** 2 * 15 / 50) #facteur de correction 15/50
        print(f"Taille des échantillons combinés: {current_size:.2f} Mo")

        if current_size > max_size_bytes:
            TimeStamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_IQSamples_to_csv_thread(combined_data, header, TimeStamp)
            self.Rx0_combined_samples = np.array([], dtype=complex)
            self.Rx1_combined_samples = np.array([], dtype=complex)

    def append_samples(self, Rx0, Rx1):
        """
        Concatène les échantillons des canaux Rx0 et Rx1 et les stocke dans des variables de classe distinctes.

        Paramètres:
            Rx0 (numpy.array): Un tableau numpy contenant les échantillons IQ complexes pour le canal Rx0 sous la forme (I + jQ).
            Rx1 (numpy.array): Un tableau numpy contenant les échantillons IQ complexes pour le canal Rx1 sous la forme (I + jQ).
        """

        # Stocker ou concaténer les échantillons de Rx0
        if self.Rx0_combined_samples.size == 0:
            self.Rx0_combined_samples = Rx0
        else:
            self.Rx0_combined_samples = np.concatenate((self.Rx0_combined_samples, Rx0))

        # Stocker ou concaténer les échantillons de Rx1
        if self.Rx1_combined_samples.size == 0:
            self.Rx1_combined_samples = Rx1
        else:
            self.Rx1_combined_samples = np.concatenate((self.Rx1_combined_samples, Rx1))

    def save_IQSamples_to_csv(self, combined_data, header, TimeStamp=None):
        """
        Sauvegarde les données d'un des canaux de réception du PlutoSDR au format Parquet.

        Paramètres:
            combined_data (numpy array): Un tableau numpy contenant les échantillons IQ complexes sous la forme (I + jQ).
            header (str): L'en-tête pour le fichier CSV.
            TimeStamp (str): Le timestamp pour nommer le fichier.
        """
        # Obtenir le répertoire de travail courant et définir le chemin complet
        current_directory = os.getcwd()
        folder_path = os.path.join(current_directory, "recordings_temp")
        filename = f"IQSamples_{TimeStamp}.parquet"  # Utilisation de l'extension .parquet
        complete_path = os.path.join(folder_path, filename)

        print(f"Enregistrement des signaux IQ à la date {TimeStamp}")

        # Créer le dossier contenant le fichier Parquet, s'il n'existe pas
        os.makedirs(os.path.dirname(complete_path), exist_ok=True)

        # Convertir les données en DataFrame pandas
        df = pd.DataFrame(combined_data, columns=header.split(', '))

        # Convertir le DataFrame pandas en table pyarrow
        table = pa.Table.from_pandas(df)

        # Écrire la table en format Parquet pour que ce soit plus rapide. Il faudra ensuite le décompresser pour le lire.
        pq.write_table(table, complete_path, use_dictionary=True, compression='snappy')

        print(f"Les échantillons IQ ont été enregistrés avec succès dans {complete_path}.")

    def save_IQSamples_to_csv_thread(self, combined_data, header, TimeStamp=None):
        # Créer et démarrer un thread pour exécuter save_IQSamples_to_csv
        save_thread = threading.Thread(target=self.save_IQSamples_to_csv, args=(combined_data, header, TimeStamp))
        save_thread.start()
def main():

    '''Create Radios'''
    my_sdr = CustomSDR(uri='ip:192.168.2.1')
    my_sdr.configure_rx_properties()
    my_sdr.configure_tx_properties()
    my_sdr.configure_sampling_properties()
    my_sdr.display_parameters()

    # Calibrate Rx:
    my_sdr.calibrate_rx()

    while(True):

        # Receive data
        data = my_sdr.receive_data()
        my_sdr.append_samples(data['Rx_0'], data['Rx_1'])
        my_sdr.check_and_save_samples()

main()

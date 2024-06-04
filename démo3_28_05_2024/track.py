########################################################################################################################
######################################### CustomSDR class to manage SDR device #########################################
import asyncio
import os
import ctypes.util
import time

import pandas as pd
import csv
from ctypes import CDLL
import warnings
warnings.filterwarnings('default')
import adi
import matplotlib.pyplot as plt
import numpy as np
import datetime

"""Importation des drivers"""
libiio_path = r'C:\Windows\System32\libiio.dll'
libiio = CDLL(libiio_path)

libad9361_path = r'C:\Windows\System32\libad9361.dll'
libad9361 = CDLL(libad9361_path)

"""Importations personnalisées"""
from dsp_utils import CallCounter, MonopulseAngleEstimator
from ui_utils import CustomSubplot, digitalGyroscope

from enum import Enum

class Channel(Enum):
    Rx_0 = "Rx0"
    Rx_1 = "Rx1"
    Tx_0 = "Tx0"
    Tx_1 = "Tx1"


class CustomSDR(adi.ad9361):
    def __init__(self, uri):

        # Initialise la classe parente avec l'URI spécifié
        super().__init__(uri=uri)

        """Set PlutoSDR Hardware properties"""
        # Rx
        self.rx_lo = int(2.25e9)  # use 2.25e9
        self.rx_mode = "manual"  # can be "manual" or "slow_attack"
        self.rx_gain0 = int(40)
        self.rx_gain1 = int(40)

        # Tx
        self.tx_lo = int(2.25e9)
        self.tx_gain0 = -3
        self.tx_gain1 = -88

        # Sampling
        self.sample_rate = 30e6  # must be <=30.72 MHz if both channels are enabled
        self.buffer_size = 2 ** 14  # (ou nombre d'échantillons) possibilité de 2 ** 18
        self.kernel_buffers_count = 1

        """ Set distance between Rx antennas """
        self.d_wavelength = 0.5  # distance between elements as a fraction of wavelength.  This is normally 0.5
        self.wavelength = 3E8 / self.rx_lo  # wavelength of the RF carrier
        self.d = self.d_wavelength * self.wavelength  # distance between elements in meters

        """Experience properties """
        self.phase_cal = 0  # Phase calibration value for the SDR
        self.fc0 = int(2e3)

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
        self.rx_rf_bandwidth = int(self.fc0 * 3)

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
        self.tx_enabled_channels = [0, 1]

        # Set the Tx RF bandwidth, usually around three times the center frequency
        self.tx_rf_bandwidth = int(self.fc0 * 3)

        # Set the local oscillator frequency for the Tx path
        self.tx_lo = int(self.tx_lo)

        # Set the hardware gain for Tx channel 0
        self.tx_hardwaregain_chan0 = int(self.tx_gain0)

        # Set the hardware gain for Tx channel 1
        self.tx_hardwaregain_chan1 = int(self.tx_gain1)

    def configure_sampling_properties(self):
        """Configures various properties for the Sampling of the Pluto SDR.
        This includes setting sampling rate, buffer_size, etc"""

        self.rx_buffer_size = int(self.buffer_size) # Set the buffer size for the reception buffer
        self.tx_buffer_size = int(self.buffer_size) # Set the buffer size for the transmission buffer

        self.tx_cyclic_buffer = True # Enable cyclic buffer for continuous transmission

        self._rxadc.set_kernel_buffers_count(self.kernel_buffers_count)  # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto

    def display_parameters(self):
        """
        Displays the parameters of the SDR system including frequencies, bandwidth,
        sampling rate, number of samples, optimized distance between Rx antennas,
        and gains for both Rx and Tx antennas. The output values are formatted in
        human-readable units such as GHz, kHz, MHz, mm, and number of samples.
        """
        print("Fréquence RX et TX: ", int(self.rx_lo / 1_000_000), "GHz")
        print("Bande passante : ", int((self.fc0 * 3) / 1_000), "kHz")
        print("Echantillonnage : ", int(self.sample_rate / 1_000_000), "MHz")
        print("Nombre d'échantillons : ", int(self.buffer_size))
        print("Distance optimisée entre les deux antennes Rx : ", int(self.d * 1000), "mm")
        print("Start : ", int(self.buffer_size * 1000 * (self.sample_rate / 2 + self.fc0 / 2) / self.sample_rate), "KHz")
        print("Start : ", int(self.buffer_size * 1000 * (self.sample_rate / 2 + self.fc0 * 2) / self.sample_rate), "KHz")
        print("Gain RX0 : ", int(self.rx_gain0))
        print("Gain RX1 : ", int(self.rx_gain1))
        print("Gain TX0 : ", int(self.tx_gain0))

    ########################################################################################################################
    ########################################### SEND / RECEIVE DATA ########################################################
    def send_tx_data(self, i0, q0):
        """
        Envoie des données en utilisant la modulation IQ.

        Paramètres:
            i0 (array): Tableau contenant les échantillons de la composante en phase (I)
                        d'un signal numérique (ou discret).
            q0 (array): Tableau contenant les échantillons de la composante en quadrature (Q)
                        d'un signal numérique (ou discret).

        Les composantes I et Q sont combinées pour former un signal complexe IQ,
        qui est ensuite transmis par le SDR. Les données sont dupliquées pour deux canaux,
        simulant ainsi une transmission stéréo ou deux voies.
        """
        # Combinaison des composantes I et Q pour former le signal complexe IQ
        iq0 = i0 + 1j * q0

        # Envoi des données.
        self.tx([iq0, iq0])  # Envoi des données Tx sur deux canaux.

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

    def test_send_tx_data(self):
        """Synthétise sous forme I/Q et envoie un signal sinusoidale pure de test à la fréquence fc0.
        On vérifie que la fréquence d'échantillonnage du CNA soit supérieur à la fréquence fc0 du signal"""
        fs = int(self.sample_rate) #fréquence d'échantillonnage
        N = int(self.buffer_size) # Nombre d'échantillons à envoyer
        ts = 1 / float(fs)
        t = np.linspace(0, (N - 1) * ts, N) # Utilisation de np.linspace pour une meilleure précision
        i0 = np.cos(2 * np.pi * t * self.fc0) * 2 ** 14
        q0 = np.sin(2 * np.pi * t * self.fc0) * 2 ** 14
        self.send_tx_data(i0, q0)
        return i0 + 1j * q0

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
############################################## OTHER ###################################################################
    def save_IQSamples_to_csv(self, data, Channel):
        """
        Sauvegarde les données d'un des canaux de réception du PlutoSDR au format CSV.

        Paramètres:
            data (dict): Un tableau numpy contenant les échantillons IQ complexes sous la forme (I + jQ).
            Channel (Enum): Une variable énumérée pour préciser le canal du PlutoSDR enregistré.
        """
        # Obtenir le répertoire de travail courant
        current_directory = os.getcwd()

        # Filename à partir des conditions d'enregistrement (date,heure, channel)
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        current_time = datetime.datetime.now().strftime("%Hh%Mm")
        filename = f"{Channel}_IQSamples_{today}_{current_time}.csv"

        # Répertoire pour enregistrer les échantillons
        current_directory = os.getcwd()
        complete_path = f"{current_directory}\\recordings_temp\\{filename}"
        print(f"Enregistrement des signaux IQ de {Channel} dans {complete_path}")

        # Créer le dossier contenant le fichier CSV, s'il n'existe pas
        os.makedirs(os.path.dirname(complete_path), exist_ok=True)

        # Maintenant, ouvrir le fichier CSV
        with open(complete_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Index', 'I', 'Q'])  # En-tête du CSV

            # Parcourir le tableau numpy des échantillons et les stocker dans le CSV
            for index, sample in enumerate(data):
                i = np.real(sample)  # Partie réelle du nombre complexe
                q = np.imag(sample)  # Partie imaginaire du nombre complexe
                writer.writerow([index, i, q])

########################################################################################################################
############################################### Tracking Program #######################################################

def main():
    '''Create Radios'''
    my_sdr = CustomSDR(uri='ip:192.168.1.100')
    my_sdr.configure_rx_properties()
    my_sdr.configure_tx_properties()
    my_sdr.configure_sampling_properties()
    my_sdr.display_parameters()

    """ Ouvrir une fenetre UI"""
    #fig = CustomSubplot("Poursuite auto SDR")
    app = digitalGyroscope()

    '''Synthèse et transmission d'un signal sinusoidal pure pour tester le module Pluto'''
    # On a configuré le SDR pour utiliser un buffer circulaire à l'émission donc les données reviennent au début une fois que la fin est atteinte.
    # On a donc une émission continue!
    Tx_IQsamples = my_sdr.test_send_tx_data()
    my_sdr.save_IQSamples_to_csv(Tx_IQsamples, Channel.Tx_0.value)

    # Calibrate Rx:
    my_sdr.calibrate_rx()

    #Instancier le compteur
    counter = CallCounter()

    # Création de l'instance de la classe SlidingWindowAverager
    estimator = MonopulseAngleEstimator(my_sdr.phase_cal, 3, my_sdr.sample_rate, my_sdr.fc0, my_sdr.rx_lo, my_sdr.d, my_sdr.buffer_size)

    '''Acquisition unique'''
    data = my_sdr.receive_data()
    my_sdr.save_IQSamples_to_csv(data['Rx_0'], Channel.Rx_0.value)
    my_sdr.save_IQSamples_to_csv(data['Rx_1'], Channel.Rx_1.value)

    '''Acquisition en continue'''

    while (True):
        data = my_sdr.receive_data()
        counter()

        ''' DSP '''
        AoA = estimator.scan_for_DOA(data['Rx_0'], data['Rx_1'])

        if AoA is not None:
            '''Update UI'''
            #fig.update_SCAN_window(scan_DOA)
            app.update_Gyroscope_window(AoA)

            #Ajouter une petite pause pour rafraîchir la figure
            plt.pause(1e-5)

    my_sdr.end_transmission()

main()

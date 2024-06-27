import os
import sys
import threading
from datetime import datetime

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
from acquisition import AcquisitionThread
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication, QTimer


class ZipThread(AcquisitionThread):
    def __init__(self, uri='ip:192.168.2.1', parent=None):
        super().__init__(uri, parent)
        self.Rx0_combined_samples = np.array([], dtype=complex)
        self.Rx1_combined_samples = np.array([], dtype=complex)

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
            TimeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
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

def test_zip_thread():
    app = QCoreApplication(sys.argv)

    zip_thread = ZipThread()

    def print_data(rx0, rx1):
        #print("Data received:")
        #print("Rx_0:", rx0)
        #print("Rx_1:", rx1)
        zip_thread.append_samples(rx0, rx1)
        zip_thread.check_and_save_samples(max_size_bytes=500)  # Adjust size as needed for testing

    zip_thread.data_received.connect(print_data)

    zip_thread.start()

    def stop_thread():
        zip_thread.stop()
        zip_thread.wait()
        print("Acquisition thread stopped.")
        QCoreApplication.quit()

    QTimer.singleShot(50000, stop_thread)

    sys.exit(app.exec_())

test_zip_thread()
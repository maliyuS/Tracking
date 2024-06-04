import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge, Rectangle


class CustomSubplot:
    def __init__(self, title, figsize=(19, 16)):
        """
         Constructeur personnalisé pour créer une figure avec un titre.
        """
        # Création de la figure et du subplot
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.fig.suptitle(title)

        # Initialisation d'un texte pour vérifier l'affichage initial
        self.ax.text(0.5, 0.5, 'Figure Initialisée', horizontalalignment='center',
                     verticalalignment='center', transform=self.ax.transAxes)
        self.fig.canvas.draw()  # Dessiner immédiatement la figure
        plt.show(block=False)  # Afficher la figure sans bloquer le reste du script

    def update_SCAN_window(self, scan_DOA):
        """
        Met à jour la figure avec de nouvelles données.
        """
        self.ax.clear()  # Effacer les dessins précédents

        # Mettre à jour les courbes avec de nouvelles données
        self.ax.plot(scan_DOA['delay_phases'], scan_DOA['peak_sum'], color='g', label='Signal Somme')
        self.ax.plot(scan_DOA['delay_phases'], scan_DOA['peak_delta'], color='b', label='Signal Delta')
        self.ax.plot(scan_DOA['delay_phases'], scan_DOA['monopulse_phase'], color='y', label='Phase Monopulse')

        self.ax.axvline(x=scan_DOA['peak_delay'], color='r', linestyle=':')
        self.ax.text(-180, -21, f"Déphasage = {round(scan_DOA['peak_delay'], 1)} deg")
        self.ax.text(-180, -25, "Signal Somme en vert")
        self.ax.text(-180, -27, "Signal Delta en bleu")
        self.ax.text(-180, -29, f"Angle = {int(scan_DOA['steer_angle'])}")

        self.ax.set_ylim(top=5, bottom=-50)
        self.ax.set_xlabel("Déphasage en degrés")
        self.ax.set_ylabel("Rx0 + Rx1 [dBFS]")

        self.ax.legend()
        self.fig.canvas.draw()  # Redessiner la figure après la mise à jour

class digitalGyroscope:
    def __init__(self, figsize=(19, 16)):
        self.figsize = figsize
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.drow_Gyroscope_window()  # Affiche le gyroscope initial

    def draw_digital_counter(self, position, number):
        counter_width = 0.6
        counter_height = 0.4

        # Dessiner le cadre vert autour du compteur
        rect = Rectangle(position, counter_width, counter_height, linewidth=1, edgecolor='dimgray', facecolor='aliceblue')
        self.ax.add_patch(rect)

        # Afficher le nombre dans le cadre
        self.ax.text(position[0] + counter_width / 2, position[1] + counter_height / 2, str(number),
                     verticalalignment='center', horizontalalignment='center', fontsize=15, color='crimson')

    def set_counter(self, number):
        self.ax.clear()
        self.draw_digital_counter((1.7, -0.5), number)
        self.ax.set_xlim(-1, 5)
        self.ax.set_ylim(-1, 3)
        self.ax.axis('off')

    def draw_rosace(self, center, radius):

        # Supprimer les anciennes instances de rosace
        for patch in self.ax.patches:
            if isinstance(patch, Wedge):
                patch.remove()

        # Utiliser un Wedge pour créer une demi-rosace colorée
        wedge = Wedge(center, radius, 0, 180, facecolor='aliceblue', edgecolor='darkslategray', lw=2)
        self.ax.add_patch(wedge)

        # Ajouter des marques et du texte pour chaque 30 degrés de -90 à +90
        for ang in np.linspace(-90, 90, 13):
            adjusted_angle = np.radians(-ang + 90)
            x = center[0] + radius * np.cos(adjusted_angle)
            y = center[1] + radius * np.sin(adjusted_angle)
            self.ax.plot([center[0], x], [center[1], y], color='gainsboro', lw=1)
            text_x = center[0] + (radius + 0.1) * np.cos(adjusted_angle)
            text_y = center[1] + (radius + 0.1) * np.sin(adjusted_angle)
            self.ax.text(text_x, text_y, f'{int(ang)}°', verticalalignment='center', horizontalalignment='center', fontsize=8,
                         color='dimgray')

    def add_indicator(self, center, radius, current_angle):
        # Dessiner un indicateur en rouge
        adjusted_angle = np.radians(-current_angle + 90)
        end_x = center[0] + radius * np.cos(adjusted_angle)
        end_y = center[1] + radius * np.sin(adjusted_angle)
        self.ax.plot([center[0], end_x], [center[1], end_y], color='crimson', lw=2.5)

    def show(self):
        plt.show()

    def drow_Gyroscope_window(self):
        self.set_counter(0)
        self.draw_rosace((2, 0), 2)
        self.add_indicator((2, 0), 2, 0)

    def update_Gyroscope_window(self, angle):
        self.set_counter(round(angle))
        self.add_indicator((2, 0), 2, round(angle))
        self.draw_rosace((2, 0), 2)  # Redessiner la rosace à chaque mise à jour

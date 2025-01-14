import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from pygame import mixer
from pydub import AudioSegment
from scipy.io import wavfile

class AudioPlayer(QMainWindow):
    def __init__(self, audio_file):
        super().__init__()

        self.audio_file = audio_file
        self.is_paused = False 
        self.init_ui()
        mixer.init()

        # Convertir le fichier MP3 en WAV pour le traitement
        wav_file = self.convert_mp3_to_wav(audio_file)
        mixer.music.load(wav_file)

        # Charger le fichier WAV et afficher le signal
        self.sample_rate, self.data = self.load_audio_signal(wav_file)

        # Configuration du timer pour mettre à jour la position de la lecture
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_playback_position)

    def init_ui(self):
        self.setWindowTitle('Audio Player')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.plot_widget = pg.PlotWidget()     # afficher le signal audio
        layout.addWidget(self.plot_widget)

        self.play_button = QPushButton('Play')
        self.pause_button = QPushButton('Pause')
        self.stop_button = QPushButton('Stop')

        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)

        self.play_button.clicked.connect(self.play_audio)
        self.pause_button.clicked.connect(self.pause_audio)
        self.stop_button.clicked.connect(self.stop_audio)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def convert_mp3_to_wav(self, mp3_file):
        """Convertir le fichier MP3 en WAV"""
        audio = AudioSegment.from_mp3(mp3_file)
        wav_file = "converted_audio.wav"
        audio.export(wav_file, format="wav")
        return wav_file

    def load_audio_signal(self, wav_file):
        """Charger le fichier WAV et afficher le signal audio"""
        sample_rate, data = wavfile.read(wav_file)
        if len(data.shape) > 1:
            data = data[:, 0]  # Si stéréo, prendre le premier canal

        # Créer l'axe du temps
        time_axis = np.linspace(0, len(data) / sample_rate, num=len(data))

        # Afficher le signal sur le graphique
        self.plot_widget.plot(time_axis, data, pen='b')

        # Ajouter une barre verticale pour visualiser la lecture
        self.playback_marker = self.plot_widget.addLine(x=0, pen=pg.mkPen('y', width=2))

        return sample_rate, data

    def play_audio(self):
        """Démarrer ou reprendre la lecture"""
        if self.is_paused:
            mixer.music.unpause()  # Reprendre la lecture si elle est en pause
            self.is_paused = False
        else:
            mixer.music.play()  # Démarrer la lecture si ce n'est pas en pause
        self.timer.start(100)  # Mettre à jour la position toutes les 100 ms

    def pause_audio(self):
        """Mettre en pause la lecture"""
        if not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
            self.timer.stop()  # Arrêter le timer pendant la pause

    def stop_audio(self):
        """Arrêter la lecture"""
        mixer.music.stop()
        self.is_paused = False
        self.timer.stop()
        self.playback_marker.setValue(0)  # Remettre la barre à 0

    def update_playback_position(self):
        """Mettre à jour la position de la barre de lecture"""
        current_time = mixer.music.get_pos() / 1000.0  # Temps écoulé en secondes
        duration = len(self.data) / self.sample_rate  # Durée totale de l'audio en secondes
        if current_time >= duration:
            self.timer.stop()  # Arrêter le timer si la lecture est terminée
        else:
            # Calculer la position actuelle de la barre de lecture
            self.playback_marker.setValue(current_time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    audio_file = 'forester-Commodo.mp3'   # Ton fichier MP3
    player = AudioPlayer(audio_file)
    player.show()
    sys.exit(app.exec_())


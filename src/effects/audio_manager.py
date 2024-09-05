from kivy.core.audio import SoundLoader

from kivy.core.audio import SoundLoader


class AudioManager:
    def __init__(self):
        self.music_queue = []  # Liste de la file d'attente de musiques
        self.current_music = None  # Musique actuellement jouée

    def load_music(self, filename):
        """Charger une musique et retourner l'objet Sound."""
        sound = SoundLoader.load(f"assets/audio/{filename}.wav")
        if sound:
            sound.loop = False
            return sound
        else:
            print(f"Erreur : impossible de charger {filename}")
            return None

    def play_music(self, filename):
        """Jouer une musique et ajouter un écouteur d'événement pour la fin."""
        self.current_music = self.load_music(filename)
        if self.current_music:
            self.current_music.play()
            self.current_music.bind(on_stop=self._on_music_end)  # Lier l'événement de fin de musique

    def play_music_queue(self, filenames):
        if isinstance(filenames, str):
            filenames = [filenames]  # Convertir une chaîne en liste si nécessaire
        elif not isinstance(filenames, list):
            raise ValueError("`filenames` doit être une liste ou une chaîne de caractères.")

        self.music_queue = filenames
        self.play_next_music()


    def play_next_music(self):
        """Jouer la prochaine musique dans la file d'attente."""
        if self.music_queue:
            next_music = self.music_queue.pop(0)  # Récupérer et retirer la première musique de la liste
            self.play_music(next_music)  # Jouer la prochaine musique


    def _on_music_end(self, instance):
        """Fonction appelée lorsque la musique se termine."""
        print("Musique terminée, lecture de la suivante...")
        self.play_next_music()  # Lire la prochaine musique dans la file d'attente


    def stop_music(self):
        """Arrêter la musique en cours."""
        if self.current_music:
            self.current_music.stop()
            self.current_music = None

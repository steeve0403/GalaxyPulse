from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.current_sound = None
        self.music_queue = []

        # Charger les sons
        self.load_sound('begin', 'assets/audio/begin.wav')
        self.load_sound('galaxy', 'assets/audio/galaxy.wav')
        self.load_sound('game_over_impact', 'assets/audio/gameover_impact.wav')
        self.load_sound('game_over_voice', 'assets/audio/gameover_voice.wav')
        self.load_sound('music1', 'assets/audio/music1.wav')
        self.load_sound('restart', 'assets/audio/restart.wav')

    def load_sound(self, name, filepath):
        """
        Loads a sound and adds it to the dictionary.
        :param name: The key to reference the sound.
        :param filepath: The path to the sound file.
        """
        sound = SoundLoader.load(filepath)
        if sound:
            self.sounds[name] = sound

    def play_music_queue(self, music_list):
        """
        Plays a list of music tracks one after the other.
        If a single music name is provided, it converts it into a list.
        :param music_list: A list of music names to play, or a single music name as a string.
        """
        if isinstance(music_list, str):
            music_list = [music_list]

        self.music_queue = music_list
        self._play_next_in_queue()

    def _play_next_in_queue(self):
        """
        Plays the next music track in the queue.
        If there are tracks left in the queue, it retrieves and removes the first one,
        plays it, and schedules a callback to play the next track when the current one ends.
        """
        if self.music_queue:
            next_music = self.music_queue.pop(0)
            if next_music in self.sounds:
                self.current_sound = self.sounds[next_music]
                self.current_sound.play()

                Clock.schedule_once(self._on_music_end, self.current_sound.length)

    def _on_music_end(self, dt):
        """
        Callback triggered when the current music ends, to play the next track in the queue.
        :param dt: Time delay, automatically passed by the scheduler.
        """
        self._play_next_in_queue()

    def stop_current(self):
        """
        Stops the currently playing music track.
        """
        if self.current_sound:
            self.current_sound.stop()

    def stop_music(self):
        """
        Stops the current music and clears the music queue to prevent any further tracks from playing.
        """
        self.stop_current()

        self.music_queue = []

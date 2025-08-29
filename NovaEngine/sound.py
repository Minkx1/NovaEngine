"""===== sound.py ====="""

import pygame


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False

    def load_sound(self, name, path):
        """Load sounds and give it a name"""
        self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name, volume=1.0, count=1):
        """Play short sound"""
        if name in self.sounds:
            snd = self.sounds[name]
            snd.set_volume(volume)
            snd.play(count)
        else:
            from .engine import log

            log(f"Sound '{name}' not found", "SoundManager", True)

    def play_music(self, path, volume=1.0, loop=-1):
        """Play music in background"""
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop)
        self.music_playing = True

    def stop_music(self):
        """Stops music, that is currently playing"""
        pygame.mixer.music.stop()
        self.music_playing = False

    def pause_music(self):
        """Pauses music"""
        pygame.mixer.music.pause()

    def continue_music(self):
        """Continues playing music"""
        pygame.mixer.music.unpause()

    def stop_all(self):
        """Stops all playing sounds"""
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.music_playing = False

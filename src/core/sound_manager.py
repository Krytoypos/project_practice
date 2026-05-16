import pygame


class SoundManager:

    def __init__(self):

        pygame.mixer.init()

        self.sounds = {

            "jump": pygame.mixer.Sound(
                "../assets/music/footsteps/jump.wav"
            ),

            "button": pygame.mixer.Sound(
                "../assets/music/button/press-button.wav"
            ),

            "door": pygame.mixer.Sound(
                "../assets/music/door/Door-opening.wav"
            ),

            "lamp_on": pygame.mixer.Sound(
                "../assets/music/lamp/Flashlight-Clicking-1.wav"
            ),

            "lamp_off": pygame.mixer.Sound(
                "../assets/music/lamp/Flashlight-Clicking-2.wav"
            ),

            "electric_hum": pygame.mixer.Sound(
                "../assets/music/lamp/Electric-hum.wav"
            )
        }

        self.footsteps = [

            pygame.mixer.Sound(
                "../assets/music/footsteps/step1.wav"
            ),

            pygame.mixer.Sound(
                "../assets/music/footsteps/step2.wav"
            ),

            pygame.mixer.Sound(
                "../assets/music/footsteps/step3.wav"
            ),

            pygame.mixer.Sound(
                "../assets/music/footsteps/step4.wav"
            )
        ]

        self.sounds["jump"].set_volume(0.6)

        for step in self.footsteps:
            step.set_volume(1)

    def play(self, sound_name):

        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_footstep(self):
        print("STEP")
        import random

        random.choice(self.footsteps).play()

    def play_music(self):

        pygame.mixer.music.load(
            "../assets/music/Background-music/Background-music.ogg"
        )

        pygame.mixer.music.set_volume(0.2)

        pygame.mixer.music.play(-1)
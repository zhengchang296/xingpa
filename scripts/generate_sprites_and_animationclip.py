import os
import sys

class SpriteGenerator:
    def __init__(self, sprite_folder):
        self.sprite_folder = sprite_folder
        self.sprites = []

    def generate_sprites(self):
        # Generation logic here
        if not os.path.exists(self.sprite_folder):
            os.makedirs(self.sprite_folder)
        # Add sprite generation code
        print(f"Sprites generated in {self.sprite_folder}")

class AnimationClip:
    def __init__(self, duration):
        self.duration = duration
        self.clips = []

    def create_clip(self):
        # Clip creation logic here
        print(f"Animation clip created with duration: {self.duration}")

if __name__ == '__main__':
    while True:
        print("Welcome to Sprite and AnimationClip Generator")
        folder = input("Enter the sprite folder name: ")
        sprite_generator = SpriteGenerator(folder)
        sprite_generator.generate_sprites()
        duration = input("Enter animation clip duration: ")
        animation_clip = AnimationClip(duration)
        animation_clip.create_clip()
        rerun = input("Would you like to rerun the script? (yes/no): ")
        if rerun.lower() != 'yes':
            print("Exiting the script.")
            break

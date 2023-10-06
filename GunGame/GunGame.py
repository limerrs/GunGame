import tkinter as tk
from tkinter import ttk
import pygame
import random
from playsound import playsound
import os

path = os.getcwd()
class ModeSelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Mode Selection")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12))

        self.label = ttk.Label(root, text="Choose a mode:", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.easy_button = ttk.Button(root, text="Easy Mode", command=lambda: self.start_mode(True))
        self.easy_button.pack(pady=10)

        self.hard_button = ttk.Button(root, text="Hard Mode", command=lambda: self.start_mode(False))
        self.hard_button.pack()

    def start_mode(self, easy_mode):
        self.root.destroy()
        root = tk.Tk()
        root.title("Fortnite Gun Sound Guessing Game")
        game = FortniteGunSoundGame(root, easy_mode)
        root.mainloop()


class FortniteGunSoundGame:
    def __init__(self, root, easy_mode=True):
        self.root = root
        self.root.title("Fortnite Gun Sound Guessing Game")
        self.root.geometry("725x700")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12))

        self.gun_options = [
            ("Assault Rifle", f"{path}"+r"\GunGameTextures\AR.png", f"{path}"+r"\GunGameSounds\ar_full.mp3"),
            ("Pump Shotgun", f"{path}"+r"\GunGameTextures\pump.png", f"{path}"+r"\GunGameSounds\pump-shotgun_full.mp3"),
            ("Bolt Sniper Rifle", f"{path}"+r"\GunGameTextures\bolt_action_sniper.png", f"{path}"+r"\GunGameSounds\bolt_sniper_full.mp3"),
            ("Silenced SMG", f"{path}"+r"\GunGameTextures\silenced_smg.png", f"{path}"+r"\GunGameSounds\silenced-smg_full.mp3"),
            ("Silenced AR", f"{path}"+r"\GunGameTextures\silenced_ar.png", f"{path}"+r"\GunGameSounds\Silenced_ar_full.mp3"),
            ("Thermal AR", f"{path}"+r"\GunGameTextures\thermal_ar.png", f"{path}"+r"\GunGameSounds\Thermal_ar_full.mp3"),
            ("FN Scar", f"{path}"+r"\GunGameTextures\scar.png", f"{path}"+r"\GunGameSounds\scar_sound_full.mp3"),
            ("Rocket Launcher", f"{path}"+r"\GunGameTextures\rocket_launcher.png", f"{path}"+r"\GunGameSounds\rocket-launcher_full.mp3"),
            ("Pumpkin Launcher", f"{path}"+r"\GunGameTextures\pumpkin_launcher.png", f"{path}"+r"\GunGameSounds\pumpkin-rocket-launcher_full.mp3"),
            ("Pistol", f"{path}"+r"\GunGameTextures\pistol.png", f"{path}"+r"\GunGameSounds\pistol_full.mp3"),
            ("Burst AR", f"{path}"+r"\GunGameTextures\burst_ar.png", f"{path}"+r"\GunGameSounds\burst_full.mp3"),
            ("Heavy Sniper", f"{path}"+r"\GunGameTextures\heavy_sniper.png", f"{path}"+r"\GunGameSounds\heavy-sniper_full.mp3")
        ]
        self.correct_gun = ""
        self.sound_label = ttk.Label(root, text="", font=("Helvetica", 16))
        self.sound_label.grid(row=0, column=0, columnspan=3, pady=20)

        self.correct_counter = ttk.Label(root, text="Correct answers: 0", font=("Helvetica", 12))
        self.correct_counter.grid(row=0, column=3, padx=20, pady=10)

        self.lives_counter = ttk.Label(root, text="Lives: 2", font=("Helvetica", 12))
        self.lives_counter.grid(row=0, column=4, padx=20, pady=10)

        self.button_frame = ttk.Frame(root)
        self.button_frame.grid(row=1, column=0, columnspan=5)

        self.play_button = ttk.Button(self.button_frame, text="Play", command=self.play_sound)
        self.play_button.grid(row=0, column=1, padx=10, pady=10)

        self.restart_button = ttk.Button(self.button_frame, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=0, column=2, padx=10, pady=10)

        self.buttons = []  # Initialize an empty list to store the gun buttons

        # Gun buttons
        for index, (gun, image_path, _) in enumerate(self.gun_options):
            image = tk.PhotoImage(file=image_path)
            button = ttk.Button(self.button_frame, image=image, command=lambda gun=gun: self.check_answer(gun))
            button.image = image  # Keep a reference to the image to prevent it from being garbage collected
            button.gun_name = gun  # Store the gun name as an attribute of the button
            button.grid(row=1 + index // 4, column=index % 4, padx=10, pady=10)
            self.buttons.append(button)  # Add the button to the list


        pygame.init()
        self.playing = False
        self.current_sound = None
        self.correct_answers = 0
        self.easy_mode = easy_mode
        self.play_game()

    def play_sound(self):
        if not self.playing:
            self.playing = True
            gun_name, _, sound_file = self.gun_options[0]
            self.current_sound = pygame.mixer.Sound(sound_file)
            if self.easy_mode:
                self.current_sound.play()
            else:
                self.current_sound.play(maxtime=int(0.5 * 1000))  # Play for 0.5 seconds in hard mode
            self.play_button.config(text="Playing...", state="disabled")
            self.restart_button.config(state="disabled")
            for button in self.buttons:
                button.config(state="disabled")
            self.root.after(int(self.current_sound.get_length() * 1000), self.enable_play_button)
            return self.playing
        
    def enable_play_button(self):
        self.playing = False
        self.play_button.config(text="Play", state="normal")
        self.restart_button.config(state="normal")
        for button in self.buttons:
            button.config(state="normal")

    def play_game(self):
        self.guess_attempts = 0
        self.lives = 2
        if self.gun_options:
            random.shuffle(self.gun_options)
            self.correct_gun, _, _ = self.gun_options[0]
            self.sound_label.config(text="Listen to the sound:")
        else:
            self.sound_label.config(text="Congratulations! You've guessed all the guns.")
            self.play_button.config(state="disabled")

    def check_answer(self, selected_gun):
        if selected_gun == self.correct_gun:
            self.sound_label.config(text="Correct! You guessed the gun.")
            playsound(f"{path}"+r"\GunGameSounds\Ding.mp3")
            self.correct_answers += 1
            self.correct_counter.config(text=f"Correct answers: {self.correct_answers}")
            # Disable the button of the correct gun
            for button in self.buttons:
                if button['text'] == self.correct_gun:
                    button.config(state="disabled")

            self.gun_options.remove((self.correct_gun, self.gun_options[0][1], self.gun_options[0][2]))  # Remove the correct gun
            self.root.after(1500, self.play_game)
        else:
            self.guess_attempts += 1
            self.lives -= 1 
            if self.guess_attempts == 1 and self.lives == 1:
                self.sound_label.config(text="Incorrect. Try again.")
                self.lives_counter.config(text=f"Lives: {self.lives}")
                for button in self.buttons:
                    button.config(state="disabled")
                playsound(f"{path}"+r"\GunGameSounds\wrong.mp3")
            elif self.guess_attempts == 2 and self.lives == 0:
                playsound(f"{path}"+r"\GunGameSounds\wrong.mp3")
                self.sound_label.config(text="Incorrect. Thanks for playing.")
                self.lives_counter.config(text=f"Lives: {self.lives}")
                self.play_button.config(state="disabled")
                for button in self.buttons:
                    button.config(state="disabled")
            else:
                self.root.after(1500, self.play_game)
    
    def restart_game(self):
        self.correct_answers = 0
        self.correct_counter.config(text="Correct answers: 0")
        self.lives = 2
        self.lives_counter.config(text="Lives: 2")
        self.play_button.config(state="normal")
        self.restart_button.config(state="disabled")
        for button in self.buttons:
            button.config(state="normal")
        self.play_game()

if __name__ == "__main__":
    root = tk.Tk()
    mode_selection = ModeSelection(root)
    root.mainloop()
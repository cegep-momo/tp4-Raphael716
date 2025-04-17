from model.platine import Platine
from model.mesure import Mesure
from view import LCD1602
from threading import Thread
import time
from datetime import datetime
import json
class Controller:
    def __init__(self):
        self.platine = Platine()
        
        self.lcd_message = "En attente"
        self.lcd_message_old = ""
        self.lcd_wait = "Aucun mouvement"
        self.en_cour = False
        
        self.platine.on_motion_callback = self.on_motion
        self.platine.on_no_motion_callback = self.on_no_motion
        self.platine.on_capte_pressed_callback = self.button_handler
        self.platine.on_start_pressed_callback = self.on_start_button_pressed
        
        Thread(target=self.lcd_loop, daemon=True).start()
        Thread(target=self.check_motion, daemon=True).start()
    
    def lcd_loop(self):
        while True:
            if self.lcd_message != self.lcd_message_old:
                if not self.platine.force_display:
                    LCD1602.clear()
                    LCD1602.write(0, 0, self.lcd_message)
                    self.lcd_message_old = self.lcd_message
            time.sleep(1)
    
    def check_motion(self):
        while True:
            if self.platine.program_active and not self.en_cour:
                self.en_cour = True
                self.lcd_message = self.lcd_wait
                time.sleep(1)
                self.lcd_message = "En attente"
                time.sleep(4)
                self.en_cour = False
    
    def on_motion(self):
        #mesure = Mesure(datetime.now(), ["Mouvement detecte"])
        self.lcd_wait = "Mouvement detecte"
    
    def on_no_motion(self):
        #mesure = Mesure(datetime.now(), ["Aucun mouvement"])
        self.lcd_wait = "Aucun mouvement"
    
    def button_handler(self):
        if self.platine.force_display:
            return
        
        self.platine.force_display = True
        self.lcd_message = "Mouvement detecte" if self.platine.motion_detected else "Aucun mouvement"
        LCD1602.clear()
        LCD1602.write(0, 0, self.lcd_message.ljust(16))
        LCD1602.write(0, 1, "Verification".ljust(16))
        self.lcd_message_old = self.lcd_message
        evenement = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Format : YYYY-MM-DD HH:MM:SS
        "valeur_capteur": self.lcd_message
        }

        try:
            with open("donnees.json", "r", encoding="utf-8") as fichier:
                donnees_existantes = json.load(fichier)
        except (FileNotFoundError, json.JSONDecodeError):
            donnees_existantes = []

        donnees_existantes.append(evenement)

        with open("donnees.json", "w", encoding="utf-8") as fichier:
            json.dump(donnees_existantes, fichier, indent=4)

        time.sleep(2)
        self.lcd_message = "En attente"
        LCD1602.clear()
        LCD1602.write(0, 0, self.lcd_message.ljust(16))
        self.platine.force_display = False
    
    def on_start_button_pressed(self):
        if not self.platine.program_active:
            self.lcd_message = "En attente"
    
    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.platine.cleanup()
            LCD1602.clear()
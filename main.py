from gpiozero import MotionSensor, Button
from threading import Thread
import time
from datetime import datetime
from model.mesure import Mesure
from view import LCD1602

pir = MotionSensor(21)
buttonCapte = Button(16)
buttonStart = Button(20)

motion_detected = False
lcd_message = "En attente"
lcd_message_old = ""
is_running = False
last_button_press_time = 0
button_press_interval = 0.5

LCD1602.init(0x27, 1)
print("[DEBUG] LCD prêt")

def lcd_loop():
    global lcd_message
    global lcd_message_old
    while True:
        if lcd_message != lcd_message_old:
            LCD1602.clear()
            LCD1602.write(0, 0, lcd_message)
            lcd_message_old = lcd_message
            print(f"[DEBUG] LCD msg: {lcd_message}")
        time.sleep(1)

def check_motion():
    global motion_detected, lcd_message, is_running
    while True:
        if is_running:
            print("[DEBUG] Verification des mouvements")
            if motion_detected:
                lcd_message = "Mouvement detecte"
            else:
                lcd_message = "Aucun mouvement"
            time.sleep(5)

def on_motion():
    global motion_detected, lcd_message
    motion_detected = True
    mesure = Mesure(datetime.now(), ["Mouvement detecte"])
    print(mesure.afficherMesure())
    lcd_message = "Mouvement detecte"


def on_no_motion():
    global motion_detected, lcd_message
    motion_detected = False
    mesure = Mesure(datetime.now(), ["Aucun mouvement"])
    print(mesure.afficherMesure())
    lcd_message = "Aucun mouvement"

pir.when_motion = on_motion
pir.when_no_motion = on_no_motion

def on_button_press():
    global lcd_message, last_button_press_time, lcd_message_old
    current_time = time.time()

    if current_time - last_button_press_time < button_press_interval:
        return
    last_button_press_time = current_time

    if motion_detected:
        lcd_message = "Mouvement detecte"
    else:
        lcd_message = "Aucun mouvement"

    LCD1602.clear()
    if lcd_message != lcd_message_old:
        LCD1602.clear()
        LCD1602.write(0, 0, lcd_message)
        lcd_message_old = lcd_message
        print(f"[DEBUG] Bouton : {lcd_message}")

    time.sleep(2)
    LCD1602.clear()
    print("[DEBUG] LCD efface après 2 secondes")

buttonCapte.when_pressed = on_button_press

def on_start_button_pressed():
    global is_running
    global lcd_message
    is_running = not is_running
    if is_running:
        print("[DEBUG] Verification des mouvements activee.")
    else:
        lcd_message = "En attente"
        print("[DEBUG] Verification des mouvements desactivee.")

buttonStart.when_pressed = on_start_button_pressed

Thread(target=lcd_loop, daemon=True).start()
Thread(target=check_motion, daemon=True).start()

while True:
    time.sleep(1)

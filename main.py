from view import LCD1602
from controler.controler import Controller
import signal
import sys
import time
def signal_handler(sig, frame):
    print("\nArrêt du programme en cours...")
    LCD1602.clear()
    LCD1602.write(0,0,"Arret en cour")
    time.sleep(1.5)
    LCD1602.clear()
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    LCD1602.init(0x27, 1)
    
    try:
        controller = Controller()
        controller.run()
    except Exception as e:
        print(f"Erreur lors de l'exécution: {str(e)}")
        LCD1602.clear()
        sys.exit(1)
from gpiozero import MotionSensor, Button
import threading
import time
class Platine:
    def __init__(self):
        self.pir = MotionSensor(21)
        self.button_capte = Button(16, bounce_time=0.5)
        self.button_start = Button(20)
        
        self.motion_detected = False
        self.program_active = False
        self.force_display = False
        
        self.motion_lock = threading.Lock()
        self.no_motion_lock = threading.Lock()
        self.last_motion_time = 0
        self.no_motion_id = 1
        self.checking_no_motion = False
        
        self.on_motion_callback = None
        self.on_no_motion_callback = None
        self.on_capte_pressed_callback = None
        self.on_start_pressed_callback = None
        
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        self.pir.when_motion = self._handle_motion
        self.pir.when_no_motion = self._handle_no_motion
        self.button_capte.when_pressed = self._handle_capte_press
        self.button_start.when_pressed = self._handle_start_press
    
    def _handle_motion(self):
        with self.no_motion_lock:
            self.motion_detected = True
            self.last_motion_time = time.time()
            self.no_motion_id += 1
            self.checking_no_motion = False
        
        if self.on_motion_callback:
            self.on_motion_callback()
    
    def _handle_no_motion(self):
        with self.no_motion_lock:
            if self.checking_no_motion:
                return
            
            current_id = self.no_motion_id
            self.checking_no_motion = True
        
        def delayed_check(my_id):
            time.sleep(1.5)
            with self.no_motion_lock:
                self.checking_no_motion = False
                if my_id != self.no_motion_id:
                    return
                
                elapsed = time.time() - self.last_motion_time
                if elapsed >= 1.5:
                    self.motion_detected = False
                    if self.on_no_motion_callback:
                        self.on_no_motion_callback()
        
        threading.Thread(target=delayed_check, args=(current_id,)).start()
    
    def _handle_capte_press(self):
        if self.on_capte_pressed_callback:
            threading.Thread(target=self.on_capte_pressed_callback).start()
    
    def _handle_start_press(self):
        self.program_active = not self.program_active
        if self.on_start_pressed_callback:
            self.on_start_pressed_callback()
    
    def cleanup(self):
        self.pir.close()
        self.button_capte.close()
        self.button_start.close()
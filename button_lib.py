from machine import Pin
import time

class ButtonHandler:
    def __init__(self, pin_num, mode, callback=None, callback1=None, callback2=None, debug=0, debounce_time=15):
        """
        Initialize the button handler with the given pin and mode.
        
        :param pin_num: The GPIO pin number where the button is connected.
        :param mode: The mode of the button. 
                     0 = press (detects button press),
                     1 = press (calls callback on press),
                     2 = release (calls callback on release),
                     3 = press/release (callback1 on press, callback2 on release).
        :param callback: Function to call in modes 0, 1, or 2.
        :param callback1: Function to call on press in mode 3.
        :param callback2: Function to call on release in mode 3.
        :param debug: Debug mode. If set to 1, prints debug messages. Default is 0 (no messages).
        :param debounce_time: Debouncing time in milliseconds to prevent multiple triggers. Default is 15ms.
        """
        self.button = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.mode = mode
        self.callback = callback
        self.callback1 = callback1
        self.callback2 = callback2
        self.pin_num = pin_num
        self.debug = debug
        self.debounce_time = debounce_time  # Debouncing time in milliseconds
        self.last_triggered = time.ticks_ms()  # Last time the interrupt was triggered
        
        if self.debug:
            print(f"DEBUG: Initializing ButtonHandler on pin {pin_num}, mode {mode}, debounce_time {debounce_time}ms")
        
        # Set up interrupts based on mode
        if mode == 0:  # Trigger callback on button press (falling edge)
            if self.debug:
                print(f"DEBUG: Mode 0 (Pin {pin_num}): Triggering on button press (falling edge)")
            self.button.irq(trigger=Pin.IRQ_FALLING, handler=self._debounced_callback)
        elif mode == 1:  # Callback on press (falling edge)
            if self.debug:
                print(f"DEBUG: Mode 1 (Pin {pin_num}): Triggering callback on press (falling edge)")
            self.button.irq(trigger=Pin.IRQ_FALLING, handler=self._debounced_callback)
        elif mode == 2:  # Callback on release (rising edge)
            if self.debug:
                print(f"DEBUG: Mode 2 (Pin {pin_num}): Triggering callback on release (rising edge)")
            self.button.irq(trigger=Pin.IRQ_RISING, handler=self._debounced_callback)
        elif mode == 3:  # Callback1 on press, callback2 on release
            if self.debug:
                print(f"DEBUG: Mode 3 (Pin {pin_num}): Triggering callback1 on press, callback2 on release")
            self.button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self._debounced_dual_callback)

    def _debounced_callback(self, pin):
        """Debounced callback function for modes 0, 1, and 2."""
        current_time = time.ticks_ms()
        # Check if enough time has passed since the last trigger (debounce check)
        if time.ticks_diff(current_time, self.last_triggered) > self.debounce_time:
            self.last_triggered = current_time  # Update the last triggered time
            if self.debug:
                if pin.value() == 0:
                    print(f"DEBUG: Pin {self.pin_num}, Mode {self.mode}: Button pressed (falling edge)")
                else:
                    print(f"DEBUG: Pin {self.pin_num}, Mode {self.mode}: Button released (rising edge)")

            if self.callback:
                try:
                    if self.debug:
                        print(f"DEBUG: Pin {self.pin_num}, Mode {self.mode}: Executing callback {self.callback.__name__}")
                    self.callback()
                except Exception as e:
                    print(f"ERROR in callback: {e}")
        elif self.debug:
            print(f"DEBUG: Pin {self.pin_num}: Ignoring trigger due to debounce")

    def _debounced_dual_callback(self, pin):
        """Debounced callback function for mode 3: press and release."""
        current_time = time.ticks_ms()
        # Check if enough time has passed since the last trigger (debounce check)
        if time.ticks_diff(current_time, self.last_triggered) > self.debounce_time:
            self.last_triggered = current_time  # Update the last triggered time
            if pin.value() == 0:  # Button pressed (falling edge)
                if self.debug:
                    print(f"DEBUG: Pin {self.pin_num}, Mode 3: Button pressed (falling edge)")
                if self.callback1:
                    try:
                        if self.debug:
                            print(f"DEBUG: Pin {self.pin_num}, Mode 3: Executing callback1 {self.callback1.__name__}")
                        self.callback1()
                    except Exception as e:
                        print(f"ERROR in callback1: {e}")
            else:  # Button released (rising edge)
                if self.debug:
                    print(f"DEBUG: Pin {self.pin_num}, Mode 3: Button released (rising edge)")
                if self.callback2:
                    try:
                        if self.debug:
                            print(f"DEBUG: Pin {self.pin_num}, Mode 3: Executing callback2 {self.callback2.__name__}")
                        self.callback2()
                    except Exception as e:
                        print(f"ERROR in callback2: {e}")
        elif self.debug:
            print(f"DEBUG: Pin {self.pin_num}: Ignoring trigger due to debounce")

    def wait(self):
        """Keep the program running, allowing interrupts to handle button events."""
        if self.debug:
            print(f"DEBUG: Pin {self.pin_num}: Waiting for button events (interrupts)")
        while True:
            time.sleep(1)  # Keep the loop alive, but not busy


Initialize the button handler with the given pin and mode.
        
param pin_num: The GPIO pin number where the button is connected.

param mode: The mode of the button. 
               0 = press (detects button press),
               
               1 = press (calls callback on press),
               
               2 = release (calls callback on release),
               
               3 = press/release (callback1 on press, callback2 on release).
               
param callback: Function to call in modes 0, 1, or 2.

param callback1: Function to call on press in mode 3.

param callback2: Function to call on release in mode 3.

param debug: Debug mode. If set to 1, prints debug messages. Default is 0 (no messages).

param debounce_time: Debouncing time in milliseconds to prevent multiple triggers. Default is 15ms.

```
from button_lib import ButtonHandler

def hello():
    print("Button was pressed!")
def hello1():
    print("Button was release!")

button1 = ButtonHandler(pin_num=14, mode=0, callback=hello, debug=0, debounce_time=15)

button2 = ButtonHandler(pin_num=16, mode=1, callback=hello, debug=0)

button2 = ButtonHandler(pin_num=17, mode=2, callback=hello, debug=0)

button2 = ButtonHandler(pin_num=18, mode=3, callback1=hello, callback2=hello1, debug=0, debounce_time=15)

button1.wait()
```

import keyboard
import time


isListetning = False
def hotkeyPress(event):
    isListetning=True
    print(event)
    pass

def hotkeyRelease(event):
    isListetning=False
    print(event)
    pass

keyboard.on_release_key("v",hotkeyRelease)
keyboard.on_press_key("v",hotkeyPress)

while True:
    time.sleep(0.1)
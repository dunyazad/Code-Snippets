from pynput.mouse import Button, Controller
from pynput import keyboard

mouse = Controller()

# def on_press(key):
#     try:
#         print('Alphanumeric key pressed: {0} '.format(
#             key.char))
#     except AttributeError:
#         print('special key pressed: {0}'.format(
#             key))

# def on_release(key):
#     print('Key released: {0}'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()

# while True:
#     print ("Current position: " + str(mouse.position))
#     # mouse.position = (-216, 256)
#     # mouse.click(Button.left, 1)



from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

do_click = False
pos_x = 0
pos_y = 0

def on_press(key):
    global do_click


    print("Key pressed: {0}".format(key))
    if key == key.enter:
        if do_click == False:
            print("start")
            do_click = True
        elif do_click == True:
            print("stop")
            do_click = False
            

def on_release(key):
    print("Key released: {0}".format(key))

def on_move(x, y):
    print("Mouse moved to ({0}, {1})".format(x, y))

def on_click(x, y, button, pressed):
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


# Setup the listener threads
keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
mouse_listener.start()
# keyboard_listener.join()
# mouse_listener.join()

while True:
    pos_x, pos_y = mouse.position
    
    # print ("Current position: " + str(pos_x) + " " + str(pos_y))
    
    if do_click == True:
        mouse.click(Button.left, 1)

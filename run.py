import time
import math
import pygame
import threading
import subprocess

from pymouse import PyMouse


MAX_MOUSE_SPEED = 15
MAX_SCROLL_SPEED = 3
DEAD_PERCENTAGE = .05

value_counter = 0

previous_values = None
previous_axes = None
keyboard_visible = False


def _initialize_joystick():
    joysticks = []

    pygame.init()
    pygame.joystick.init()

    for i in range(pygame.joystick.get_count()):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print(f"Found joystick {i}: ", joysticks[-1].get_name())

    return joysticks


def _initialize_py_mouse():
    mouse = PyMouse()

    return mouse


def _read_from_joysticks(joysticks, mouse):
    threads = []

    thread = threading.Thread(
        target=_mouse_movement_loop, args=(mouse,)
    )
    thread.daemon = True
    thread.start()
    threads.append(thread)

    for joystick in joysticks:
        thread = threading.Thread(
            target=_joystick_event_loop, args=(joystick, mouse,)
        )
        thread.daemon = True
        thread.start()
        
        threads.append(thread)

    return threads


def _wait_on_threads(threads):
    for thread in threads:
        thread.join()


def _joystick_event_loop(joystick, mouse):
    axes = [ 0.0 ] * joystick.get_numaxes()
    buttons = [ False ] * joystick.get_numbuttons()

    keep_alive = True
    while keep_alive:
        try:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                keep_alive = False
            elif event.type == pygame.JOYAXISMOTION:
                axes[event.dict['axis']] = event.dict['value']
            elif event.type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
                buttons[event.dict['button']] ^= True

            _print_values(axes, buttons)
        except KeyboardInterrupt:
            keep_alive = False


def _mouse_movement_loop(mouse):
    global previous_axes

    while True:
        print(previous_axes)
        if previous_axes is not None:
            if abs(previous_axes[0]) > DEAD_PERCENTAGE:
                position = mouse.position()
                delta = MAX_MOUSE_SPEED * (previous_axes[0] ** 5)
                # delta = delta * -1 if previous_axes[0] < 0 else delta
                x = int(position[0] + delta)
                mouse.move(x, position[1])

                # print(delta, x)

            if abs(previous_axes[1]) > DEAD_PERCENTAGE:
                position = mouse.position()
                delta = MAX_MOUSE_SPEED * (previous_axes[1] ** 5)
                # delta = delta * -1 if previous_axes[1] < 0 else delta
                y = int(position[1] + delta)
                mouse.move(position[0], y)

                # print(delta, y)

            if abs(previous_axes[4]) > DEAD_PERCENTAGE:
                position = mouse.position()
                delta = MAX_SCROLL_SPEED * (previous_axes[4] ** 5)
                # delta = delta * -1 if previous_axes[1] < 0 else delta
                if delta < 0:
                    mouse.click(*position, 4, int(abs(delta)))
                else:
                    mouse.click(*position, 5, int(abs(delta)))

                print(delta)

            # if abs(previous_axes[5]) > DEAD_PERCENTAGE:
            #     position = mouse.position()
            #     delta = MAX_SCROLL_SPEED * (previous_axes[5] ** 5)
            #     # delta = delta * -1 if previous_axes[1] < 0 else delta
            #     mouse.click(*position, 5, int(delta))

            #     print(delta)

        time.sleep(.01)


def _print_values(axes, buttons):
    global value_counter
    global previous_values
    global previous_axes
    global keyboard_visible

    if previous_values is None:
        previous_values = buttons.copy()
        previous_axes = axes.copy()

    axes_string = " ".join(
        ["{:.3f}".format(axe_value) for axe_value in axes]
    )

    buttons_string = " ".join(
        ["Down" if button_value else "Up" for button_value in buttons]
    )

    if buttons[0] != previous_values[0]:
        print("button 0")
        if buttons[0]:
            position = mouse.position()
            mouse.press(*position)
            print("press")
        else:
            position = mouse.position()
            mouse.release(*position)
            print("release")
    elif buttons[1] != previous_values[1]:
        if buttons[1]:
            position = mouse.position()
            mouse.press(*position, 2)
        else:
            position = mouse.position()
            mouse.release(*position, 2)
    elif buttons[2]:
        position = mouse.position()
        mouse.click(*position)
        time.sleep(.005)
        position = mouse.position()
        mouse.click(*position)
    elif buttons[3]:
        position = mouse.position()
        mouse.click(*position, 2)
        time.sleep(.005)
        position = mouse.position()
        mouse.click(*position, 2)
    elif buttons[7]:
        if keyboard_visible:
            subprocess.Popen(["pkill", "onboard"])
            keyboard_visible = False
        else:
            subprocess.Popen("onboard")
            keyboard_visible = True

        
        # print(position)

        # mouse.move(600, 600)
        # # mouse.click(x, y)
        # time.sleep(1)
        # mouse.press(600, 600)
        # time.sleep(1)
        # mouse.move(700, 700)
        # time.sleep(1)
        # mouse.release(700, 700)

    previous_values = buttons.copy()
    previous_axes = axes.copy()

    # print("Response: {} \nAnalog sticks: {} \nButtons: {}\n".format(
    #         value_counter, axes_string, buttons_string
    #     )
    # )

    value_counter += 1


if __name__ == "__main__":
    joysticks = _initialize_joystick()

    mouse = _initialize_py_mouse()

    threads = _read_from_joysticks(joysticks, mouse)

    _wait_on_threads(threads)

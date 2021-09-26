import time

from pymouse import PyMouse


mouse = PyMouse()
position = mouse.position()
print(position)

mouse.move(600, 600)
# mouse.click(x, y)
time.sleep(1)
mouse.press(600, 600)
time.sleep(1)
mouse.move(700, 700)
time.sleep(1)
mouse.release(700, 700)

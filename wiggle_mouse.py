# MODULES
import pyautogui
import datetime
import time
# TIME PARAMETERS
now = datetime.datetime.now()
current_time = now.time()
begin = datetime.time(9, 0, 0)
end = datetime.time(17, 0, 0)
# WIGGLE LOOP
while current_time > begin and current_time < end:
    now = datetime.datetime.now()
    current_time = now.time()
    pyautogui.moveRel(0, 75, duration = 1)
    pyautogui.moveRel(-75, 0, duration = 1)
    pyautogui.moveRel(0, -75, duration = 1)
    pyautogui.moveRel(75, 0, duration = 1)
    time.sleep(5)

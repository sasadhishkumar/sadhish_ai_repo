import pyautogui
import time

time.sleep(3)

x,y=pyautogui.position()
print(f'{x} {y}')

pyautogui.click(x,y)

#pyautogui.typewrite("hello \n")
#print('\n')
pyautogui.write("python3 Enter_cmd.py")
pyautogui.press('enter')
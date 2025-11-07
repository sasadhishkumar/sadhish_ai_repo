import pyautogui
import time
print ("muruga")
#pyautogui.click(500,500)
time.sleep(2)
#pyautogui.rightClick(200,200)


(x,y)=pyautogui.displayMousePosition()
print(f'{x},{y}')
(x,y)= pyautogui.position()
print(f'{x},{y}')
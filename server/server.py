from flask import Flask 
import pyautogui
import time
  
app = Flask(__name__) 
  
@app.route('/') 
def mouse_movement(x,y): 
    screenWidth, screenHeight = pyautogui.size()
    currentMouseX, currentMouseY = pyautogui.position()
    pyautogui.click(x,y)


if __name__ == '__main__': 
    app.run() 




# # Click the mouse.
# pyautogui.click()   
# # Move the mouse to XY coordinates and click it. 
   
# pyautogui.doubleClick()

# # Move mouse to given XY coordinates
# pyautogui.moveTo(X, Y)
# # Move mouse Y pixels down from its current position (Relative)
# pyautogui.move(0, Y)      
# pyautogui.moveTo(500, 500, duration=2)  

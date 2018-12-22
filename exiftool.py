#python  script to enter necessary cmd to command prompt
# image name -> latitude -> longitude available in out.txt
#exiftool has to be installed and exe file here is kept is C:/Users/Siddharth
#here out7.txt is made in C:/Users/Siddharth or the same location where exiftool.exe is kept

import os
import pyautogui
import time


os.system("start cmd")
time.sleep(2)#pause the code a bit so that code resumes only after cmd window is open
pyautogui.typewrite("cd ..\n")#i am currently in C:\Users\Siddharth\Desktop\pyy, so i had to move up to 2 parent directories
pyautogui.typewrite("cd ..\n")

#command to execute exif tool, it returns imgid, longitude and latitude and stores them in out7.txt
#if out7.txt isn't available a new file would be created in the same location where exiftool is kept
pyautogui.typewrite('exiftool -filename -gpslongitude -gpslatitude -T -n C:\\Users\\Siddharth\\Desktop\\skylark\\software_dev\\images > out7.txt\n', interval=0.01)

#autocloasing the cmd window after exiftool has completed it's job
pyautogui.typewrite('exit\n', interval=0.01)



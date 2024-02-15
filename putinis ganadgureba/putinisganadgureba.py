import os

shutdown = input ("shutdown? (yes / no ) :")

if shutdown == "no":
    exit()
else :
    os.system("shutdown /s /t 1")


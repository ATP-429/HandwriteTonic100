import os
import time

# Keep calling draw.py to update exmaple.svg
while True:
    os.system("python draw.py")
    time.sleep(2)
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from py532lib.mifare import *
import time
import os
from threading import Thread
import cv2
import numpy as np
import ndef

#OpenCV Implementation
def open_img():
    img = cv2.imread("/home/pi/Desktop/hatch3/recycling_home.png")

    cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    cv2.imshow("window", img)
    
    cv2.waitKey()
    cv2.destroyAllWindows()
    
#display video after scanning
def open_vid(vid):
    command = "omxplayer " + vid
    os.system(command)
    
#listen for nfc cards    
def read_card():
    while True:
        try:
            card = Mifare()
            card.SAMconfigure()
            card.set_max_retries(MIFARE_SAFE_RETRIES)
            uid = card.scan_field()
            if uid:
                blocksToExplore = [0,1,2,3]
                dataArray = []
                for block in blocksToExplore:
                    address = card.mifare_address(1,block)
                    card.mifare_auth_b(address,MIFARE_FACTORY_KEY)
                    data = card.mifare_read(address)
                    card.in_deselect()
                    dataArray.extend([hex(x) for x in data]) #data in array form
                
                try:
                    fiftyFourlocation = dataArray.index('0x6e')+1
                    felocation = dataArray.index('0xfe')
                    dataArray = dataArray[fiftyFourlocation:felocation]
                    newArray = []
                    fatToTrim = "0x"
                    for thoseGuys in dataArray: 
                        newHex = thoseGuys.replace(fatToTrim,"")
                        newArray.extend(newHex)
                    s = ""
                    s = s.join(newArray)
                    s = bytes.fromhex(s).decode('ascii')
                except ValueError:
                    s = "invalid"
                    
                if s == "cardOne":
                    print("card 1")
                    open_vid("/home/pi/Desktop/hatch3/sample.mp4")
                    card = ""

                elif s == "cardTwo":
                    print("card 2")
                    open_vid("/home/pi/Desktop/hatch3/trash.mp4")
                    card = ""
                
                elif s == "invalid":
                    print("Invalid card")
                    card = ""
                    time.sleep(2)
                    
                else:
                    print("Card not recognized")
                    card = ""
                    time.sleep(2)
        except Exception as e:
            print("whoops: " + str(e))


if __name__ == '__main__':
    Thread(target = open_img).start()
    Thread(target = read_card).start()
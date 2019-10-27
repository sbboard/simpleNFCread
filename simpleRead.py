from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import os
from threading import Thread
import cv2
import numpy as np
import ndef

#listen for nfc cards    
def read_card():
    while True:
        pn532 = Pn532_i2c()
        pn532.SAMconfigure()
        card_data = pn532.read_mifare().get_data()
        print(card_data.decode())


if __name__ == '__main__':
    Thread(target = read_card).start()
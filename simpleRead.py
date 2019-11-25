from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
from py532lib.mifare import *
import time
import os
from threading import Thread
import numpy as np
import ndef

def read_card():
    while True:
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
            print(s)
            time.sleep(5)

if __name__ == '__main__':
    Thread(target = read_card).start()
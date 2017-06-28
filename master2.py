#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio link
#

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import sys



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
time.sleep(1)
# radio2.openReadingPipe(1, pipes[1])
radio.printDetails()

# radio2.startListening()

try:
    while True:
        try:
            buf = list(str(sys.argv[1]))
        except:
            buf = list('Yo yo honey singh')
        # send a packet to receiver
        radio.write(buf)
        print ("Sent:"),
        print (buf)
    
        now = time.time()
        while not radio.isAckPayloadAvailable() and time.time()<now+3:
            time.sleep(1/100.0)
        ack = []
        radio.read(ack, radio.getDynamicPayloadSize())
        if ack:
            print('slave:'),
            print(''.join([chr(n) for n in ack if n >= 32 and n <= 126]))
        time.sleep(5)

        # time.sleep(2)
        # if radio.isAckPayloadAvailable():
        #     ack = []
        #     radio.read(ack, radio.getDynamicPayloadSize())
        #     if ack:
        #         print('slave:'),
        #         print(''.join([chr(n) for n in ack if n >= 32 and n <= 126]))
        # time.sleep(5)
except:
    radio.end()


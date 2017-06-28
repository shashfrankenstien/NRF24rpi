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
radio.openReadingPipe(1, pipes[0])
radio.printDetails()

def listenForResp(timeout=4):
    radio.startListening()
    now = time.time()
    while not radio.available(0) and time.time()<now+timeout:
        time.sleep(1/100)
    resp = []
    radio.read(resp, radio.getDynamicPayloadSize())
    print('Resp:'),
    print(''.join([chr(n) for n in resp if n >= 32 and n <= 126]))
    radio.stopListening()

try:
    while True:
        try:
            buf = list(str(sys.argv[1]))
        except:
            buf = list('mhyg')
        # send a packet to receiver
        radio.write(buf)
        print ("Sent:"),
        print (buf)

        if radio.isAckPayloadAvailable():
            ack = []
            radio.read(ack, radio.getDynamicPayloadSize())
            print('slave:'),
            print(''.join([chr(n) for n in ack if n >= 32 and n <= 126]))
            listenForResp()
        time.sleep(5)
except:
    radio.end()


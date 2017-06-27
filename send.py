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



pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio2.setPayloadSize(32)
radio2.setChannel(0x60)

radio2.setDataRate(NRF24.BR_2MBPS)
radio2.setPALevel(NRF24.PA_MAX)
radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[1])
# radio2.openReadingPipe(1, pipes[1])
radio2.printDetails()

# radio2.startListening()


while True:
    buf = ['H', 'E', 'L', 'O']
    # send a packet to receiver
    radio.write(buf)
    print ("Sent:"),
    print (buf)
    # did it return with a payload?
    # if radio.isAckPayloadAvailable():
    #     pl_buffer=[]
    #     radio.read(, radio.getDynamicPayloadSize())
    #     print ("Received back:"),
    #     print (pl_buffer)
    # else:
    #     print ("Received: no payload")
    time.sleep(5)

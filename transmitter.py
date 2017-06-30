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


class NRF_Master(object):

    def __init__(self):
        self.radio = None

    def build(self):
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 17)
        time.sleep(1)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x60)

        self.radio.setDataRate(NRF24.BR_250KBPS)
        self.radio.setPALevel(NRF24.PA_MAX)
        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()

        self.radio.openWritingPipe(pipes[1])
        time.sleep(1)
        self.radio.printDetails()


    try:
        while True:
            try:
                buf = list(str(sys.argv[1]))
            except:
                buf = list('Yo yo honey singh')
            # send a packet to receiver
            self.radio.write(buf)
            print ("Sent:"),
            print (buf)

            if self.radio.isAckPayloadAvailable():
                ack = []
                self.radio.read(ack, self.radio.getDynamicPayloadSize())
                print('slave:'),
                print(''.join([chr(n) for n in ack if n >= 32 and n <= 126]))
            time.sleep(5)
    except:
        self.radio.powerDown()


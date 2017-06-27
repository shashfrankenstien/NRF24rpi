#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
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

# radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])
radio2.printDetails()

radio2.startListening()


while True:

	while not radio2.available(0):
		time.sleep(1/100.0)

	recv_buffer = []
	radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
	# print("Received: {}".format(str(recv_buffer)))

	# print("Translating..")
	print(''.join([chr(n) for n in recv_buffer if n >= 32 and n <= 126]))

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
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

# radio2.openWritingPipe(pipes[0])
radio.openReadingPipe(1, pipes[1])
time.sleep(1)
radio.printDetails()

radio.startListening()

try:
	flush = 1
	while True:

		while not radio.available(0):
			time.sleep(1/100.0)

		recv_buffer = []
		radio.read(recv_buffer, radio.getDynamicPayloadSize())
		# print("Received: {}".format(str(recv_buffer)))

		# print("Translating..")
		print(''.join([chr(n) for n in recv_buffer if n >= 32 and n <= 126]))
		if flush > 3:
			print('calculating..')
			time.sleep(5)
			ack = [ord(x) for x in 'recvd']
			radio.writeAckPayload(1, ack, len(ack))
		flush+=1

except Exception as e:
	print (e)
	radio.closeReadingPipe(1)
	radio.end()
	
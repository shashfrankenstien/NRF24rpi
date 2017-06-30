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
import sys, os


pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

def error(e):
		print((e, sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno))

class NRF_Receiver(object):

	def __init__(self):
		print('Begining radio')
		self.radio = NRF24(GPIO, spidev.SpiDev())
		self.radio.begin(0, 17)
		time.sleep(1)
		self.radio.setPayloadSize(32)
		self.radio.setChannel(0x60)

		self.radio.setDataRate(NRF24.BR_1MBPS)
		self.radio.setPALevel(NRF24.PA_MAX)
		self.radio.setAutoAck(True)
		self.radio.enableDynamicPayloads()
		self.radio.enableAckPayload()

		# radio2.openWritingPipe(pipes[0])
		self.radio.openReadingPipe(1, pipes[1])
		time.sleep(1)
		self.radio.printDetails()

	def run(self):
		self.radio.startListening()
		while True:
			start_time = time.time()
			while not self.radio.available(0):
				if time.time()-start_time>30:
					self.radio.closeReadingPipe(1)
					# self.radio.end()
					# self.radio.powerDown()
					self.radio = None
					return
				time.sleep(1/100.0)

			recv_buffer = []
			self.radio.read(recv_buffer, self.radio.getDynamicPayloadSize())
			# print("Received: {}".format(str(recv_buffer)))

			# print("Translating..")
			print(''.join([chr(n) for n in recv_buffer if n >= 32 and n <= 126]))
			ack = [ord(x) for x in 'recvd']
			self.radio.writeAckPayload(1, ack, len(ack))

try:
	while True:
		receiver = NRF_Receiver()
		receiver.run()
		receiver = None
		print('Restarting')
except Exception as e:
	print (e)
	error(e)
	
	
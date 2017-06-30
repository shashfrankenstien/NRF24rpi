#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
import time
import spidev
import sys, os


pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

def error(e):
		print((e, sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno))

class NRFtxrxBase(object):

	def __init__(self):
		self.radio = None
		self.built = False


	def build(self):
		# print('Beginning Radio')
		self.radio = NRF24(GPIO, spidev.SpiDev())
		self.radio.begin(0, 17)
		time.sleep(0.4)
		self.radio.setPayloadSize(32)
		self.radio.setChannel(0x60)
		self.radio.setDataRate(NRF24.BR_250KBPS)
		self.radio.setPALevel(NRF24.PA_MAX)
		self.radio.setAutoAck(True)
		self.radio.enableDynamicPayloads()
		self.radio.enableAckPayload()

	def setup_as_reader(self):
		self.build()
		# radio2.openWritingPipe(pipes[0])
		self.radio.openReadingPipe(1, pipes[1])
		self.built = True

	def setup_as_writer(self):
		self.build()
		self.radio.openWritingPipe(pipes[1])
		self.built = True


	def kill(self):
		if self.built and self.radio:
			# print('Killing')
			self.radio.flush_rx()
			self.radio.flush_tx()
			self.radio.closeReadingPipe(1)
			self.radio.powerDown()
			self.radio = None
			self.built = False


if __name__ == '__main__':
	r = NRFtxrxBase()
	r.build()
	r.setup_as_writer()
	r.kill()
	
	
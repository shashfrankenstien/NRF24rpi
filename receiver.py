#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to receive packets from the radio link
#

from nrftxrx import NRFtxrxBase
import time
import sys, os


pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

def error(e):
		print((e, sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno))

class NRF_Receiver(NRFtxrxBase):

	def __init__(self):
		super(self.__class__, self).__init__()
		self.subscriptions = [self._default_trigger]
		self.build_receiver()
		self.radio.printDetails()

	def build_receiver(self):
		self.build()
		self.setup_as_reader()

	def _default_trigger(self, msg):
		print('InSubscribed'),
		print(str(msg))

	def subscribe(self, func):
		self.subscriptions.append(func)


	def _run(self):
		self.radio.startListening()
		start_time = time.time()
		while True:
			quiet_time = time.time()
			while not self.radio.available(0):
				if time.time()-start_time>60 or time.time()-quiet_time>15:
					self.kill()
					return
				time.sleep(1/100.0)

			recv_buffer = []
			self.radio.read(recv_buffer, self.radio.getDynamicPayloadSize())
			# print("Received: {}".format(str(recv_buffer)))

			# print("Translating..")
			command = ''.join([chr(n) for n in recv_buffer if n >= 32 and n <= 126])
			for func in self.subscriptions:
				try:
					func(command)
				except Exception as e:
					print(e)

			print(command)
			ack = [ord(x) for x in 'recvd']
			self.radio.writeAckPayload(1, ack, len(ack))

	def run(self):
		try:
			while True:
				if not self.built: 
					print('Restarting')
					self.build_receiver()
				self._run()
		except Exception as e:
			self.kill()
			error(e)




if __name__ == '__main__':
	r = NRF_Receiver()
	r.run()
	
	
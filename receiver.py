#!/usr/bin/python
# -*- coding: utf-8 -*-

from nrftxrx import NRFtxrxBase
import time
import sys, os


def error(e):
	print((e, sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno))

class NRF_Slave(NRFtxrxBase):

	def __init__(self):
		super(self.__class__, self).__init__()
		self.subscriptions = [self._default_trigger]
		self.setup_as_reader()
		self.radio.printDetails()
		self.message_tracker = {}
		

	def _default_trigger(self, msg, ID):
		print('Built-in >'),
		print(str(msg))
		if msg=='PING':
			return 'PONG'
		

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

			string = ''.join([chr(n) for n in recv_buffer if n >= 32 and n <= 126])
			ID, msg = string.split('|')
			
			if ID not in self.message_tracker:
				ack = [ord(x) for x in '{}|WAIT'.format(ID)]
				self.radio.writeAckPayload(1, ack, len(ack))
				self.message_tracker[ID]=None
			elif self.message_tracker[ID]:
				ack = [ord(x) for x in '{}|{}'.format(ID, str(self.message_tracker[ID]))]
				self.radio.writeAckPayload(1, ack, len(ack))

			for func in self.subscriptions:
				try:
					self.message_tracker[ID] = func(msg, ID)
				except Exception as e:
					print(e)
					self.message_tracker[ID] = str(e)

			

	def run(self):
		try:
			while True:
				if not self.built: 
					print('Restarting')
					self.setup_as_reader()
				self._run()
		except Exception as e:
			self.kill()
			error(e)




if __name__ == '__main__':
	r = NRF_Slave()
	r.run()
	
	
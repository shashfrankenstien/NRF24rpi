#!/usr/bin/python
# -*- coding: utf-8 -*-

from nrftxrx import NRFtxrxBase
import time
import sys



class NRF_Master(NRFtxrxBase):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setup_as_writer()
        self.radio.printDetails()
        self.msg_id = 0
        self.message_tracker = {}

    def _send(self, msg):
        ID = str(self.msg_id).zfill(3)
        buf = list('{}|{}'.format(ID, str(msg)))

        # send a packet to receiver
        self.radio.write(buf)
        print ("Sent:"),
        print (buf)
        self.message_tracker[ID] = msg

        if self.radio.isAckPayloadAvailable():
            ack = []
            self.radio.read(ack, self.radio.getDynamicPayloadSize())
            ack = ''.join([chr(n) for n in ack if n >= 32 and n <= 126])

            print('slave:'),
            print(ack)
            return ack
        return None

    def _incrMsgId(self):
        self.msg_id = (self.msg_id+1)%1000


    def ping(self, n=4, msg='PING', ack='PONG'):
        ID = None
        try:
            count = 1
            while True:
                ack = self._send(msg)
                if ack:
                    try:
                        ID, ACK = ack.split('|')
                    except Exception as e:
                        print(e)
                    if ID and ID in self.message_tracker and self.message_tracker[ID]==msg and ACK == ack: 
                        self._incrMsgId()
                        del self.message_tracker[ID]
                time.sleep(1)
                count += 1
                if count > n:
                    raise Exception('Ping complete')
        except Exception as e:
            print(e)
            self.kill()
            self.setup_as_writer()


    def send(self, msg, n=3):
        resp = self._send(str(msg))



if __name__ == '__main__':
    t = NRF_Master()
    t.ping(50)
    t.kill()

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
        ID = self._getCurrentMsgId()
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

    def _getCurrentMsgId(self):
        return str(self.msg_id).zfill(3)

        
    def ping(self, n=4, msg='PING', ack='PONG'):
        try:
            count = 1
            while True:
                ID=None
                resp=None
                ACK=None
                resp = self._send(msg)
                if resp:
                    try:
                        ID, ACK = resp.split('|')
                        # print (self.message_tracker)
                        # print(ID!=None, ID in self.message_tracker, self.message_tracker[ID]==msg, ACK == ack)
                    except Exception as e:
                        print(e)
                    if ID!=None:
                        if ID in self.message_tracker and self.message_tracker[ID]==msg and ACK == ack: 
                            self._incrMsgId()
                            del self.message_tracker[ID]
                        else:
                            self.message_tracker[ID]=msg

                time.sleep(1)
                count += 1
                if count > n:
                    raise Exception('Ping complete')
        except Exception as e:
            print(e)
            self.kill()
            self.setup_as_writer()


    def send(self, msg, n=3):
        self._incrMsgId()
        ID = self._getCurrentMsgId()
        i=0
        while i<n:
            resp = self._send(str(msg))
            if resp:
                try:
                    ack_ID,ACK = resp.split('|')
                    if ID == ack_ID:
                        return ACK
                except Exception as e:
                    print (e)
            i+=1
            time.sleep(1)
        return None



if __name__ == '__main__':
    t = NRF_Master()
    t.ping(5)
    raw_input()
    print(t.send('Hello', 5))
    t.kill()

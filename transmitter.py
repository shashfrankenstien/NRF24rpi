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


    def ping(self, n=4):
        try:
            count = 1
            while True:
                try:
                    buf = list(str(sys.argv[1]))
                except:
                    buf = list('Yo yo honey singh')
                # send a packet to receiver
                buf.append(str(count))
                self.radio.write(buf)
                print ("Sent:"),
                print (buf)

                if self.radio.isAckPayloadAvailable():
                    ack = []
                    self.radio.read(ack, self.radio.getDynamicPayloadSize())
                    print('slave:'),
                    print(''.join([chr(n) for n in ack if n >= 32 and n <= 126]))
                time.sleep(5)
                count += 1
                if count > n:
                    raise Exception('Ping complete')
        except Exception as e:
            print(e)
            self.kill()

if __name__ == '__main__':
    t = NRF_Master()
    t.ping(50)


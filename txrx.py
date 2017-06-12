# from lib_nrf24 import NRF24
# import spidev
# import RPi.GPIO as gpio

# gpio.setmode(gpio.BOARD)

# pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]
# radio = NRF24(gpio, spidev.SpiDev())
# radio.begin(1, 11)

# radio.setPayloadSize(32)
# radio.setChannel(0x76)
# radio.setDataRate(NRF24.BR_250KBPS)

# radio.setPALevel(NRF24.PA_MIN)
# radio.setAutoAck(True)
# radio.enableDynamicPayloads()
# radio.enableAckPayload()


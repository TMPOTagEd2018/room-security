from smbus import SMBus
import time

bus = SMBus(1)

addr = 0x06


def send(num):
    bus.write_byte(addr, int(num))
    return -1


def recv():
    return bus.read_byte(addr)


while True:
    var = input("Num 1-9: ")
    if not var:
        continue

    send(var)
    print("Sending: ", var)
    time.sleep(1)

    ret = recv()
    print("Recieving: ", ret)

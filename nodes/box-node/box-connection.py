from node import Node

box = Node("box", "/dev/ttyACM0")
box.input("server", "alarm", 0x1)
box.start()

from node import Node

box = Node("box", "/dev/ttyACM0")
box.input("server", "alarm")
box.start()

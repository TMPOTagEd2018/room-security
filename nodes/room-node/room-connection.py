from node import Node

room = Node("room", 0x06)
room.register("pir", 0, lambda x: x)
room.register("lux", 1, lambda x: x)
room.start()

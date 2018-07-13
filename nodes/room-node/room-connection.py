import node

room = node.Node("room", 0x06)
room.register("pir", 0, lambda x: x)
room.register("lux", 1, lambda x: x)
room.start()

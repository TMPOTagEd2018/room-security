from node import Node

door = Node("door", 0x06)
door.register("contact", 0, lambda x: x)
door.register("imu", 1, lambda x: x if x < 128 else x-256)
door.start()

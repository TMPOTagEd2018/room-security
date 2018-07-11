from node import Node

box = Node("box", 0x06)
box.register("contact", 0, lambda x: x)
box.register("accel", 1, lambda x: x if x < 128 else x - 256)
box.pipe("server", "alarm", lambda m: box.bus.write_byte(box.ADDR, int(m.payload)))
box.start()

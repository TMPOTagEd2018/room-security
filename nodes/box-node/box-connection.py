import node

box = node.Node("box", 0x06)
box.register("contact", 0, lambda x: x)
box.register("accel", 1, lambda x: x if x < 128 else x - 256)
box.send()


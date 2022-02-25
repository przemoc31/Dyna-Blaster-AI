class NodeA:

    parent = None
    fx = 0
    gx = 0
    hx = 0
    direction = 1

    def __init__(self, px, py, reach, prio):
        self.x = px
        self.y = py
        self.reach = reach
        self.prio = prio

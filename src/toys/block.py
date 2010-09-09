
class block(object):
    def __init__(self, point, state):
        self.point, self.state = point, state
        
    def evolve(self, world):
        world.set(self.point, self.state)
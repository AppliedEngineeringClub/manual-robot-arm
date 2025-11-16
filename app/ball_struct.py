# struct.py
class FloatingBall:
    def __init__(self, x, y, radius=10, speed=5):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed


class RobotClaw:
    def __init__(self, x, y, radius=20, growth_speed=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.growth_speed = growth_speed

    def grow(self):
        self.radius += self.growth_speed

    def shrink(self):
        # avoid going negative or disappearing
        if self.radius > 5:
            self.radius -= self.growth_speed

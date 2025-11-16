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

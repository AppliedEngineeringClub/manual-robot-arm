# input.py
import pygame

def get_input():
    keys = pygame.key.get_pressed()

    dx = 0
    dy = 0

    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    return dx, dy

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

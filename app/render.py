
import pygame

def render_ball(screen, ball, color=(255, 0, 0)):
    pygame.draw.circle(screen, color, (ball.x, ball.y), ball.radius)

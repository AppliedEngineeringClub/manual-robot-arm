# render.py
import pygame

def render_ball(screen, ball):
    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.radius)

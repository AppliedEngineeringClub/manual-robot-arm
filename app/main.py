# main.py
import pygame
from struct import FloatingBall
from render import render_ball
from input import get_input

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 400))
    clock = pygame.time.Clock()

    ball = FloatingBall(320, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx, dy = get_input()
        ball.move(dx, dy)

        screen.fill((0, 0, 0))
        render_ball(screen, ball)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


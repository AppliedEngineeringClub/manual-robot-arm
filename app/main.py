# main.py
import pygame
from ball_struct import FloatingBall, RobotClaw
from render import render_ball
from input import get_input

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 400))
    clock = pygame.time.Clock()

    ball = FloatingBall(320, 200)
    claw = RobotClaw(500, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dx, dy, grow, shrink = get_input()

        ball.move(dx, dy)

        if grow:
            claw.grow()
        if shrink:
            claw.shrink()

        screen.fill((0, 0, 0))
        render_ball(screen, ball, (255, 0, 0))
        render_ball(screen, claw, (0, 150, 255))  # bluish claw

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

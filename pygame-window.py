#!/usr/bin/env python3


import pygame
import sys
from pygame.locals import *
 
class App:
    def __init__(self):
        ##displays the window
        self._running = True
        self._display_surf = None

        ##sets size of window
        self.size = self.width, self.height = 640, 400
        ##sets position of dot upon opening
        self.dot_x = self.width // 2
        self.dot_y = self.height // 2

        ##sets color of dot
        self.dot_color = (255, 0, 0)
        ##sets radius of dot/size
        self.dot_radius = 10
        #sets max/min "height" of dot
        self.min_radius = 2
        self.max_radius = 40
        ##sets speed of dot(half of width per click) 2D
        self.speed = 5
        ##sets up and down "speed" 3rd dimension
        self.radius_step = 1

        ##create clock to limit FPS movement
        self.clock = pygame.time.Clock()
        self.position_speed = 10
        self.radius_speed = 1

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
 ##checks to see if arrow keys are pressed and adjusts based on speed of 5 pixels(half of dot width) 
 ##Since it is on_event() it only takes individual key presses, we will need to implement this in on_loop() for smooth functionality. 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        
    ##checks for continuous input
    def on_loop(self):
        ##continuous movement when using keyboard arrows. creates boolean values for each arrow key. True if pressed.
        ##implement code in chatgpt during next meeting.

        dt = self.clock.tick(60) / 1000 #caps at 60 FPS, convert to seconds 
        keys = pygame.key.get_pressed()

        ##move dot left right, forward and backward by checking key press
        if keys[pygame.K_LEFT]:
            self.dot_x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.dot_x += self.speed
        if keys[pygame.K_UP]:
            self.dot_y -= self.speed
        if keys[pygame.K_DOWN]:
            self.dot_y += self.speed

        ##checks to see if z or x are pressed to go "up or down"
        ##if pressed checks measurements don't exceed bounds
        ##reduces radius or increases it by step size of 1 pixel
        if keys[pygame.K_z]:
            self.dot_radius = min(self.max_radius, self.dot_radius + self.radius_step)
        if keys[pygame.K_x]:
            self.dot_radius = max(self.min_radius, self.dot_radius - self.radius_step)

        ##keep dot within window bounds
        self.dot_x = min(self.width - self.dot_radius, max(self.dot_radius, self.dot_x))
        self.dot_y = min(self.height - self.dot_radius, max(self.dot_radius, self.dot_y))

    ##renders display
    def on_render(self):
        ##Clears previous frame every time dot moves
        self._display_surf.fill((0, 0, 0))

        ##Draws red dot at new position
        pygame.draw.circle(self._display_surf, self.dot_color, (self.dot_x, self.dot_y), self.dot_radius)
        
        ##Updates display to show new dot position
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
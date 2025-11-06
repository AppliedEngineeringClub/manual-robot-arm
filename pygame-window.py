#!/usr/bin/env python3


import pygame
import sys
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.dot_x = self.width // 2
        self.dot_y = self.height // 2
        self.dot_radius = 10
        self.speed = 5
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
 
 ##checks to see if arrow keys are pressed and adjusts based on speed of 5 pixels(half of dot width) 
 ##Since it is on_event() it only takes individual key presses, we will need to implement this in on_loop() for smooth functionality. 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.dot_x = max(self.dot_radius, self.dot_x - self.speed)
            elif event.key == pygame.K_RIGHT:
                self.dot_x = min(self.width - self.dot_radius, self.dot_x + self.speed)
            elif event.key == pygame.K_UP:
                self.dot_y = max(self.dot_radius, self.dot_y - self.speed)
            elif event.key == pygame.K_DOWN:
                self.dot_y = min(self.height - self.dot_radius, self.dot_y + self.speed)

    ##checks for continuous input
    def on_loop(self):
        ##continuous movement when using keyboard arrows. creates boolean values for each arrow key. True if pressed.
        ##implement code in chatgpt during next meeting. 
        pass


    ##renders display
    def on_render(self):
        ##Clears previous frame every time dot moves
        self._display_surf.fill((0, 0, 0))
        ##Draws red dot at new position
        pygame.draw.circle(self._display_surf, (255, 0, 0), (self.dot_x, self.dot_y), self.dot_radius)
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
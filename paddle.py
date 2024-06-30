import pygame
from settings import SCREEN_HEIGHT, PADDLE_HEIGHT

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
    
    def move(self, move_strength):
        new_position = self.y + move_strength
        # Ensure the paddle stays within the screen bounds
        if 0 <= new_position <= SCREEN_HEIGHT - self.height:
            self.y = new_position
        elif new_position < 0:
            self.y = 0
        else:
            self.y = SCREEN_HEIGHT - self.height

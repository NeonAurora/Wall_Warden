import pygame
from settings import BALL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.move_count = 0
        self.speed_increment_interval = 200

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y <= 0 or self.y + self.size >= SCREEN_HEIGHT:
            self.speed_y *= -1  # Reverse the vertical direction of the ball

        self.move_count += 1
        self.check_speed_increment()

        # Check if the ball goes out of the horizontal bounds
        if self.x <= 0:  # Ball exits on the left
            return 'right_scored'
        if self.x + self.size >= SCREEN_WIDTH:  # Ball exits on the right
            return 'left_scored'
        return 'continue'

    def draw(self, screen, color):
        pygame.draw.ellipse(screen, color, (self.x, self.y, self.size, self.size))
    
    def check_speed_increment(self):
        if self.move_count % self.speed_increment_interval == 0:
            self.increase_speed()
    
    def increase_speed(self):
        # Increase speed by 10%
        self.speed_x *= 1.1
        self.speed_y *= 1.1
        # Ensure that the ball speed doesn't exceed a maximum value
        max_speed = 15
        self.speed_x = min(max_speed, self.speed_x) if self.speed_x > 0 else max(-max_speed, self.speed_x)
        self.speed_y = min(max_speed, self.speed_y) if self.speed_y > 0 else max(-max_speed, self.speed_y)

    def check_collision(self, paddle):
        # Check collision with a paddle (rectangular collision detection)
        if self.x <= paddle.x + paddle.width and self.x + self.size >= paddle.x:
            if self.y <= paddle.y + paddle.height and self.y + self.size >= paddle.y:
                self.speed_x *= -1  # Reverse the horizontal direction of the ball


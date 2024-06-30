import pygame
from settings import *
from paddle import Paddle
from ball import Ball
from fuzzy_logic import ai_paddle_move

left_player_is_AI = 1

def reset_game(ball, player_paddle, ai_paddle):
    ball.x = SCREEN_WIDTH // 2
    ball.y = SCREEN_HEIGHT // 2
    ball.speed_x = BALL_SPEED_X * (-1 if ball.speed_x < 0 else 1)
    ball.speed_y = BALL_SPEED_Y * (-1 if ball.speed_y < 0 else 1)
    player_paddle.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    ai_paddle.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)  # Create a font object

    player_paddle = Paddle(10, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ai_paddle = Paddle(SCREEN_WIDTH - 10 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_SIZE, BALL_SPEED_X, BALL_SPEED_Y)

    left_score = 0
    right_score = 0
    winning_score = 3

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        if left_player_is_AI:
            ai_paddle_logic(ball, player_paddle)  # AI controls the left paddle
        else:
            if keys[pygame.K_w]:
                player_paddle.move(-10)  # Move up by 10 units
            if keys[pygame.K_s]:
                player_paddle.move(10)   # Move down by 10 units

        if keys[pygame.K_UP]:
            ai_paddle.move(-10)  # This should probably control the right paddle, not the player_paddle
        if keys[pygame.K_DOWN]:
            ai_paddle.move(10)   # This should probably control the right paddle, not the player_paddle

        screen.fill(BLACK)  # Fill the screen with black before drawing anything

        game_status = ball.move()
        if game_status != 'continue':
            if game_status == 'left_scored':
                left_score += 1
            elif game_status == 'right_scored':
                right_score += 1

            if left_score >= winning_score or right_score >= winning_score:
                print(f"Game over: {'Left wins!' if left_score > right_score else 'Right wins!'}")
                break

            reset_game(ball, player_paddle, ai_paddle)  # Reset positions for a new round

        score_text = font.render(f"{left_score}-{right_score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

        ball.check_collision(player_paddle)
        ball.check_collision(ai_paddle)
        ai_paddle_logic(ball, ai_paddle)  # Logic for right paddle if it's AI controlled

        player_paddle.draw(screen, WHITE)
        ai_paddle.draw(screen, WHITE)
        ball.draw(screen, WHITE)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def ai_paddle_logic(ball, ai_paddle):
    # Calculate the move strength from the fuzzy logic
    ai_paddle_y = ai_paddle_move(ball.y, ai_paddle.y, ball.speed_y)
    # Directly use the new AI paddle y-position calculated from fuzzy logic
    ai_paddle.move(ai_paddle_y - ai_paddle.y)  # Pass the difference as move strength


if __name__ == "__main__":
    game_loop()

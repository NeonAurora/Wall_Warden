from settings import SCREEN_HEIGHT, SCREEN_WIDTH, PADDLE_HEIGHT
def fuzzy_membership(value, start_point, mid_point, end_point):
    # This function calculates the degree of membership for a value within a triangular shaped fuzzy set
    if start_point <= value < mid_point:
        return (value - start_point) / (mid_point - start_point)
    elif mid_point <= value < end_point:
        return (end_point - value) / (end_point - mid_point)
    else:
        return 0

def fuzzy_degree(value, low, high):
    if value < low:
        return 0
    elif low <= value < high:
        return (value - low) / (high - low)
    else:
        return 1

def ai_paddle_move(ball_y, ai_paddle_y, ball_speed_y):
    distance = ball_y - ai_paddle_y
    speed = ball_speed_y

    # Calculate fuzzy degrees
    close = fuzzy_degree(abs(distance), 0, 50)
    medium = fuzzy_degree(abs(distance), 30, 150)
    far = fuzzy_degree(abs(distance), 100, 200)

    # Membership functions for speed
    moving_slow = fuzzy_degree(abs(speed), 0, 3)
    moving_fast = fuzzy_degree(abs(speed), 2, 10)

    # Multiplier to increase overall movement responsiveness
    responsiveness_multiplier = 130  # Adjust this value to increase/decrease responsiveness

    # Combine the rules to determine movement strength
    move_strength = 0
    if distance > 0:  # Ball is below the paddle
        move_strength += (far * moving_slow * 0.5 + far * moving_fast * 1 +
                          medium * moving_slow * 0.3 + medium * moving_fast * 0.7 +
                          close * moving_slow * 0.1 + close * moving_fast * 0.3) * responsiveness_multiplier
    elif distance < 0:  # Ball is above the paddle
        move_strength -= (far * moving_slow * 0.5 + far * moving_fast * 1 +
                          medium * moving_slow * 0.3 + medium * moving_fast * 0.7 +
                          close * moving_slow * 0.1 + close * moving_fast * 0.3) * responsiveness_multiplier

    # Adjust AI paddle position based on calculated move strength
    new_paddle_y = ai_paddle_y + move_strength
    # Ensure the paddle does not move out of bounds
    new_paddle_y = max(0, min(new_paddle_y, SCREEN_HEIGHT - PADDLE_HEIGHT))
    return new_paddle_y


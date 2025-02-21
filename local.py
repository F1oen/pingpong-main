import pygame

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Local Multiplayer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
paddle_width, paddle_height = 20, 100
ball_size = 15

# Paddle positions
paddle1_y = paddle2_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 7

# Ball settings
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_speed_x, ball_speed_y = 5, 5

# Scores
score1, score2 = 0, 0

# Font for score display
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    pygame.time.delay(16)  # Maintain ~60 FPS
    screen.fill(BLACK)

    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls (W/S for Player 1, ↑/↓ for Player 2)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < HEIGHT - paddle_height:
        paddle1_y += paddle_speed
    if keys[pygame.K_UP] and paddle2_y > 0:
        paddle2_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2_y < HEIGHT - paddle_height:
        paddle2_y += paddle_speed

    # Move ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collision with top/bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - ball_size:
        ball_speed_y *= -1  # Reverse vertical direction

    # Ball collision with paddles
    if (ball_x <= 70 and paddle1_y < ball_y < paddle1_y + paddle_height) or \
       (ball_x >= WIDTH - 70 and paddle2_y < ball_y < paddle2_y + paddle_height):
        ball_speed_x *= -1  # Reverse horizontal direction

    # Scoring system (if ball goes out of bounds)
    if ball_x < 0:  # Player 2 scores
        score2 += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Reset ball
        ball_speed_x *= -1  # Reverse direction
    if ball_x > WIDTH:  # Player 1 scores
        score1 += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_speed_x *= -1

    # Draw paddles, ball, and scoreboard
    pygame.draw.rect(screen, WHITE, (50, paddle1_y, paddle_width, paddle_height))  # Player 1
    pygame.draw.rect(screen, WHITE, (WIDTH - 70, paddle2_y, paddle_width, paddle_height))  # Player 2
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))  # Ball
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  # Center line

    # Display scores
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 20, 20))

    pygame.display.flip()  # Update the display

pygame.quit()
import pygame
import socket
import threading

# 🎯 Change this to your server's IP
SERVER_IP = "192.168.1.100"  # Replace with the actual IP of your server
PORT = 5555

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
print(client.recv(1024).decode())  # Welcome message

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Multiplayer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle & Ball settings
paddle_width, paddle_height = 20, 100
ball_size = 15
paddle_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 7

# Initial ball position (will be updated from server)
ball_x, ball_y = WIDTH // 2, HEIGHT // 2

# Store opponent's paddle position
paddle_opponent_y = HEIGHT // 2 - paddle_height // 2

# Score tracking
score1, score2 = 0, 0

# Function to receive game updates from the server
def receive_updates():
    global paddle_opponent_y, ball_x, ball_y, score1, score2
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            paddle_opponent_y, ball_x, ball_y, score1, score2 = map(int, data.split(","))
        except:
            break

# Start a separate thread to receive data from server
thread = threading.Thread(target=receive_updates, daemon=True)
thread.start()

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Handle quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player control (W/S or ↑/↓)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        paddle_y -= paddle_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        paddle_y += paddle_speed

    # Send paddle position to server
    client.sendall(str(paddle_y).encode())

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, (50, paddle_y, paddle_width, paddle_height))  # Player paddle
    pygame.draw.rect(screen, WHITE, (WIDTH - 70, paddle_opponent_y, paddle_width, paddle_height))  # Opponent paddle
    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))  # Ball
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))  # Center line

    # Display scores
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 20, 20))

    pygame.display.flip()
    pygame.time.delay(16)  # Maintain ~60 FPS

pygame.quit()
client.close()
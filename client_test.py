import pygame

import socket




SERVER_IP = "192.168.1.100" # Change there IP addrees of IP server.py

PORT = 5555




client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((SERVER_IP, PORT))



print(client.recv(1024).decode())




pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Ping Pong Multiplayer")



WHITE = (255, 255, 255)

BLACK = (0, 0, 0)




paddle_width, paddle_height = 20, 100

ball_size = 15

paddle_y = HEIGHT // 2 - paddle_height // 2

paddle_speed = 7



ball_x, ball_y = WIDTH // 2, HEIGHT // 2

ball_speed_x, ball_speed_y = 5, 5



running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False




    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:

        paddle_y -= paddle_speed

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:

        paddle_y += paddle_speed




    client.sendall(str(paddle_y).encode())




    data = client.recv(1024).decode()

    paddle_opponent_y, ball_x, ball_y = map(int, data.split(","))




    screen.fill(BLACK)

    pygame.draw.rect(screen, WHITE, (50, paddle_y, paddle_width, paddle_height)) # Player 1 rocket

    pygame.draw.rect(screen, WHITE, (WIDTH - 70, paddle_opponent_y, paddle_width, paddle_height)) # Player 2 rocket

    pygame.draw.ellipse(screen, WHITE, (ball_x, ball_y, ball_size, ball_size)) # Ball

    pygame.display.flip()



pygame.quit()

client.close()

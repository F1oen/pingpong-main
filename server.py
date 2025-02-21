import socket

# Server settings
HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

print("🎮 Waiting for players to connect...")
clients = []

# Accept two players
while len(clients) < 2:
    conn, addr = server.accept()
    print(f"✅ Player connected from {addr}")
    clients.append(conn)

# Send welcome message
for conn in clients:
    conn.sendall(b"Connected to Ping Pong Server")

# Ball settings
ball_x, ball_y = 400, 300
ball_speed_x, ball_speed_y = 5, 5

# Paddle positions
paddles_y = [250, 250]

# Scores
score1, score2 = 0, 0

# Game loop
while True:
    try:
        # Receive paddle positions from both players
        paddles_y[0] = int(clients[0].recv(1024).decode())
        paddles_y[1] = int(clients[1].recv(1024).decode())

        # Move ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Bounce off top/bottom walls
        if ball_y <= 0 or ball_y >= 600 - 15:
            ball_speed_y *= -1

        # Paddle collision
        if (ball_x <= 70 and paddles_y[0] < ball_y < paddles_y[0] + 100) or \
           (ball_x >= 730 and paddles_y[1] < ball_y < paddles_y[1] + 100):
            ball_speed_x *= -1

        # Scoring system
        if ball_x < 0:  # Player 2 scores
            score2 += 1
            ball_x, ball_y = 400, 300
            ball_speed_x *= -1
        if ball_x > 800:  # Player 1 scores
            score1 += 1
            ball_x, ball_y = 400, 300
            ball_speed_x *= -1

        # Send game state to both players
        game_state = f"{paddles_y[1]},{ball_x},{ball_y},{score1},{score2}"
        clients[0].sendall(game_state.encode())

        game_state = f"{paddles_y[0]},{ball_x},{ball_y},{score1},{score2}"
        clients[1].sendall(game_state.encode())

    except:
        break  # Exit if connection is lost

# Close connections
for conn in clients:
    conn.close()
server.close()
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 500
FPS = 60

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("fire dodge")

# Load custom images
background_image = pygame.image.load("background_image.jpg").convert()
paddle_image = pygame.image.load("paddle.png").convert_alpha()
ball_image = pygame.image.load("loot.png").convert_alpha()
enemy_ball_image = pygame.image.load("enemy.png").convert_alpha()

# Resize images to fit the game window
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
paddle_image = pygame.transform.scale(paddle_image, (80, 80))
ball_image = pygame.transform.scale(ball_image, (30, 30))
enemy_ball_image = pygame.transform.scale(enemy_ball_image, (40, 60))

# Clock to control the frame rate
clock = pygame.time.Clock()


def reset_game():
    global game_over, game_started, score, start_time, ball_rect, enemy_ball_rect

    game_over = False
    game_started = False
    score = 0
    start_time = pygame.time.get_ticks()

    # Reset positions of both player-controlled ball and enemy ball
    ball_rect.x = random.randint(ball_rect.width, WIDTH - ball_rect.width)
    ball_rect.y = 0

    enemy_ball_rect.x = random.randint(enemy_ball_rect.width, WIDTH - enemy_ball_rect.width)
    enemy_ball_rect.y = -enemy_ball_rect.height  # Place enemy off-screen initially

# Load background music
pygame.mixer.music.load("background_music.mp3")  # Replace with your music file
pygame.mixer.music.set_volume(0.5)  # Adjust the volume if needed
pygame.mixer.music.play(-1)  # -1 makes the music loop continuously

# Paddle
paddle_rect = paddle_image.get_rect()
paddle_rect.x = (WIDTH - paddle_rect.width) // 2
paddle_rect.y = (HEIGHT - paddle_rect.height) // 2

# Balls
ball_rect = ball_image.get_rect()
ball_rect.x = random.randint(ball_rect.width, WIDTH - ball_rect.width)
ball_rect.y = 0
ball_speed = 5

enemy_ball_rect = enemy_ball_image.get_rect()
enemy_ball_rect.x = random.randint(enemy_ball_rect.width, WIDTH - enemy_ball_rect.width)
enemy_ball_rect.y = -enemy_ball_rect.height  # Place enemy off-screen initially
enemy_ball_speed = 6

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game state
game_over = False
game_started = False
start_time = pygame.time.get_ticks()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_started = True
                start_time = pygame.time.get_ticks()  # Reset start time when Enter is pressed
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                # Restart the game only if it's game over
                if game_over:
                    reset_game()
                    game_over = False
                    game_started = False
                    score = 0
                    start_time = pygame.time.get_ticks()  # Reset start time when Shift is pressed

    if game_started and not game_over:
        # Check if at least 2 seconds have passed since the start of the game
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= 2000:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and paddle_rect.x > 0:
                paddle_rect.x -= 5
            if keys[pygame.K_RIGHT] and paddle_rect.x < WIDTH - paddle_rect.width:
                paddle_rect.x += 5
            if keys[pygame.K_UP] and paddle_rect.y > 0:
                paddle_rect.y -= 5
            if keys[pygame.K_DOWN] and paddle_rect.y < HEIGHT - paddle_rect.height:
                paddle_rect.y += 5

            # Update ball positions
            ball_rect.y += ball_speed
            enemy_ball_rect.y += enemy_ball_speed

            # Check for collision with the paddle
            if paddle_rect.colliderect(ball_rect):
                ball_rect.y = 0
                ball_rect.x = random.randint(ball_rect.width, WIDTH - ball_rect.width)
                score += 1

            # Check for collision with the enemy ball
            if paddle_rect.colliderect(enemy_ball_rect):
                game_over = True

            # Reset ball position if it goes off the screen
            if ball_rect.y > HEIGHT:
                ball_rect.y = 0
                ball_rect.x = random.randint(ball_rect.width, WIDTH - ball_rect.width)

            if enemy_ball_rect.y > HEIGHT:
                enemy_ball_rect.y = -enemy_ball_rect.height  # Place enemy off-screen
                enemy_ball_rect.x = random.randint(enemy_ball_rect.width, WIDTH - enemy_ball_rect.width)

    # Draw everything
    screen.blit(background_image, (0, 0))
    screen.blit(paddle_image, paddle_rect)
    screen.blit(ball_image, ball_rect)
    screen.blit(enemy_ball_image, enemy_ball_rect)

    # Display the score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display "Game Over" if the game is over
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        start_text = font.render("Press shift to reset!", True, (255, 255, 255))
        screen.blit(start_text, ((WIDTH - start_text.get_width()) // 2, (HEIGHT - start_text.get_height()) //1.5))
    elif not game_started:
        start_text = font.render("Press Enter to Start", True, (255, 255, 255))
        screen.blit(start_text, ((WIDTH - start_text.get_width()) // 2, (HEIGHT - start_text.get_height()) // 1.5))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)

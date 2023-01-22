import pygame
import sqlite3
from player import *

# Initialize pygame
pygame.init()

# Set the screen size and caption
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Timer")

# Set the font and font size for the timer
font = pygame.font.Font(None, 36)

# Initialize the timer and a flag to check if the game is over
start_ticks=pygame.time.get_ticks()
game_over = False

# Create a connection to the database
conn = sqlite3.connect("times.db")
cursor = conn.cursor()

# Create the table to store the times if it doesn't already exist
cursor.execute("""CREATE TABLE IF NOT EXISTS times (
                    time FLOAT)""")
conn.commit()

# Run the game loop

running = True
while running:
    for event in pygame.event.get():
        if Player.complete = 0 :
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
                running = False
                final_time = (pygame.time.get_ticks() - start_ticks) / 1000
                # Insert the final time into the database
                cursor.execute("INSERT INTO times VALUES (?)", (final_time,))
                conn.commit()

    if not game_over:
        # Calculate the elapsed time
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

        # Render the timer text
        timer_text = font.render(str(elapsed_time), True, (255, 255, 255))

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the timer text in the top right corner
        screen.blit(timer_text, (700, 0))

        # Update the display
        pygame.display.update()
    else:
        # Retrieve the lowest time from the database
        cursor.execute("SELECT MIN(time) FROM times")
        lowest_time = cursor.fetchone()[0]

        print("Game over! Time: ", final_time)
        print("Lowest time: ", lowest_time)

# Close the database connection
conn.close()

# Quit pygame
pygame.quit()

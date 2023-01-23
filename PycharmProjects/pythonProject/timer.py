import pygame
import sqlite3


class Timer:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set the screen size and caption
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Timer")

        # Set the font and font size for the timer
        self.font = pygame.font.Font(None, 36)

        # Initialize the timer and a flag to check if the game is over
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False

        # Create a connection to the database
        self.conn = sqlite3.connect("times.db")
        self.cursor = self.conn.cursor()

        # Create the table to store the times if it doesn't already exist
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS times (
                            time FLOAT)""")
        self.conn.commit()

    def run(self):
        # Run the game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_over = True
                        running = False
                        self.final_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
                        self.save_time()

            if not self.game_over:
                # Calculate the elapsed time
                elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000

                # Render the timer text
                timer_text = self.font.render(str(elapsed_time), True, (255, 255, 255))

                # Clear the screen
                self.screen.fill((0, 0, 0))

                # Draw the timer text in the top right corner
                self.screen.blit(timer_text, (700, 0))

                # Update the display
                pygame.display.update()
            else:
                self.print_results()

        # Close the database connection
        self.conn.close()

        # Quit pygame
        pygame.quit()

    def save_time(self):
        # Insert the final time into the database
        self.cursor.execute("INSERT INTO times VALUES (?)", (self.final_time,))
        self.conn.commit()

    def print_results(self):
        # Retrieve the lowest time from the database
        self.cursor.execute("SELECT MIN(time) FROM times")
        lowest_time = self.cursor.fetchone()[0]

        print("Game over! Time: ", self.final_time)
        print("Lowest time: ", lowest_time)


if __name__ == '__main__':
    t = Timer()
    t.run()
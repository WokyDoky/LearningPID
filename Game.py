# File: Game.py
import pygame
import sys
# Import the modules (files) you created
import Config
import Ball

# --- Game Class ---
class Game:
    """Manages the main game loop and game state."""
    def __init__(self):
        """Initialize Pygame, screen, config, box, target, and ball."""
        pygame.init()
        # Instantiate the Config class from the Config module
        self.config = Config.Config()

        # Set up the screen
        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Move the Ball! (OOP)")

        # Set up the box
        box_x = (self.config.SCREEN_WIDTH - self.config.BOX_WIDTH) // 2
        box_y = (self.config.SCREEN_HEIGHT - self.config.BOX_HEIGHT) // 2
        self.box_rect = pygame.Rect(box_x, box_y, self.config.BOX_WIDTH, self.config.BOX_HEIGHT)

        # Instantiate the Ball class from the Ball module, passing the config instance
        self.ball = Ball.Ball(self.config, self.config.RED, self.config.BALL_SPEED * 2)
        self.ball_current_speed = self.config.BALL_SPEED

        self.ball2 = Ball.Ball(self.config, self.config.BLUE, self.config.BALL_SPEED/2)
        self.ball2_current_speed = self.config.BALL_SPEED

        self.ball3 = Ball.Ball(self.config, self.config.GREEN, self.config.BALL_SPEED * 2)
        self.ball3_current_speed = self.config.BALL_SPEED
        self.ball3.set_size(self.config.BALL_RADIUS/2)

        # Game clock
        self.clock = pygame.time.Clock()

    def run(self):
        """Starts the main game loop."""
        running = True
        while running:
            # Handle events (like closing the window)
            running = self._handle_events()
            if not running:
                break

            # Handle continuous key presses for movement
            self._handle_input()

            # Update game state (ball position, collisions)
            self._update()

            # Draw everything to the screen
            self._draw()

            # Limit frame rate
            self.clock.tick(self.config.FPS)

        self._quit_game()

    def _handle_events(self):
        """Process Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False # Signal to stop the loop
        return True # Signal to continue

    def _handle_input(self):
        """Check keyboard state and move the balls with acceleration."""
        keys = pygame.key.get_pressed()
        base_speed = self.config.BALL_SPEED
        acceleration = self.config.BALL_ACCELERATION
        max_speed = base_speed * 1.4

        # --- Ball 1 Logic (Left/Right Arrows) ---
        moving1 = False
        direction1 = 0
        if keys[pygame.K_LEFT]:
            direction1 = -1
            moving1 = True
        if keys[pygame.K_RIGHT]:
            # If both left/right pressed, right takes precedence
            direction1 = 1
            moving1 = True

        if moving1:
            # Accelerate
            self.ball_current_speed += acceleration
            # Cap speed at max_speed
            if self.ball_current_speed > max_speed:
                self.ball_current_speed = max_speed
        else:
            # Reset speed gradually or instantly when not moving
            # Instant reset:
            self.ball_current_speed = base_speed
            # Optional: Gradual deceleration (more complex)
            # if self.ball1_current_speed > base_speed:
            #     self.ball1_current_speed -= acceleration * 2 # Decelerate faster
            #     if self.ball1_current_speed < base_speed:
            #         self.ball1_current_speed = base_speed
            # else:
            #     self.ball1_current_speed = base_speed


        # Apply movement based on current speed and direction
        self.ball.x += direction1 * self.ball_current_speed

    def _update(self):
        """Update all game objects."""
        # Update ball position and check boundaries
        self.ball.update(self.box_rect)

        self.ball2.update(self.box_rect)

        self.ball3.update(self.box_rect)
        self.chase_ball()

    def _draw(self):
        """Draw all game elements to the screen."""
        # Fill background
        self.screen.fill(self.config.BLACK)

        # Draw the box (fill and border)
        pygame.draw.rect(self.screen, self.config.BOX_COLOR, self.box_rect)
        pygame.draw.rect(self.screen, self.config.BORDER_COLOR, self.box_rect, self.config.BORDER_WIDTH)

        # Draw the ball
        self.ball.draw(self.screen)
        self.ball2.draw(self.screen)
        self.ball3.draw(self.screen)

        # Update the display
        pygame.display.flip()

    def _quit_game(self):
        """Clean up and quit Pygame."""
        pygame.quit()
        sys.exit()

    def second_ball_accelerator(self, direction_to_move):
        base_speed = self.config.BALL_SPEED
        acceleration = self.config.BALL_ACCELERATION
        max_speed = base_speed * 1.4
        moving = False
        direction = 0
        if direction_to_move == "L":
            direction = -1
            moving = True
        if direction_to_move == "R":
            direction = 1
            moving = True

        if moving:
            self.ball2_current_speed += acceleration
            if self.ball2_current_speed > max_speed:
                self.ball2_current_speed = max_speed
        else:
            self.ball2_current_speed = base_speed

    def chase_ball(self):
        """Chase the ball."""
        # --- Calculate the difference in x ---
        pos1 = self.ball.get_position()  # Gets (x1, y1)
        pos2 = self.ball2.get_position()  # Gets (x2, y2)
        pos3 = self.ball3.get_position()

        x1 = pos1[0]  # Extract x-coordinate of ball 1
        x2 = pos2[0]  # Extract x-coordinate of ball 2
        x3 = pos3[0]  # Extract x-coords fo ball 3

        delta_x = x1 - x2  # Calculate the difference
        delta_xX = x1 - x3

        """
        TODO 
        Add orbiting third ball. 
        add y direction
            why? idk
        """
        if delta_x != 0:
            print("Ball position doesn't match the ball2 position.")
            if delta_x > 0:
                self.ball2._move("R")
            if delta_x < 0:
                self.ball2._move("L")


# --- Main execution ---
if __name__ == "__main__":
    game = Game() # Create an instance of the Game
    game.run()    # Start the game loop
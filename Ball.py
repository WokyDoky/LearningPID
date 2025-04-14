# File: Ball.py
import pygame # Required for drawing, rects, and key constants

# --- Ball Class ---
class Ball:
    """Represents the movable ball in the game."""
    def __init__(self, config, color, speed):
        """Initialize the ball's properties."""
        # Store the passed config object (which is an instance of Config.Config)
        self.config = config
        # Start the ball in the center of the screen
        self.x = self.config.SCREEN_WIDTH // 2
        self.y = self.config.SCREEN_HEIGHT // 2
        self.radius = self.config.BALL_RADIUS
        self.color = color
        self.speed = speed

    def move(self, keys):
        """Move the ball based on pressed keys."""
        # Access key constants through pygame
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
    def _move (self, direction):
        """Move the ball based on direction."""
        if direction == "L":
            self.x -= self.speed
        if direction == "R":
            self.x += self.speed

    def update(self, box_rect):
        """Update ball state, including boundary checks."""
        # Keep the ball within the box boundaries horizontally
        # Access config values through the stored config instance
        left_boundary = box_rect.left + self.config.BORDER_WIDTH + self.radius
        right_boundary = box_rect.right - self.config.BORDER_WIDTH - self.radius

        if self.x < left_boundary:
            self.x = left_boundary
        elif self.x > right_boundary:
            self.x = right_boundary

    def draw(self, surface):
        """Draw the ball on the provided surface."""
        # Access drawing functions through pygame
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def get_rect(self):
        """Return a pygame.Rect representing the ball's bounding box."""
        # Access Rect class through pygame
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                          self.radius * 2, self.radius * 2)

    def get_position(self):
        """Return the current (x, y) coordinates of the ball's center."""
        return self.x, self.y

    def set_size(self, r):
        self.radius = r
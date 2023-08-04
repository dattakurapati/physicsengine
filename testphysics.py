
import math
import pygame

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
BG_COLOR = (255, 255, 255)
CIRCLE_COLOR = (0, 0, 255)
GRAVITY = 9.81

class Circle:
    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

    def apply_force(self, force_x, force_y):
        self.acceleration_x += force_x / self.mass
        self.acceleration_y += force_y / self.mass

    def update(self, dt):
        self.velocity_x += self.acceleration_x * dt
        self.velocity_y += self.acceleration_y * dt

        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

        # Add gravity
        self.apply_force(0, GRAVITY * self.mass)

        self.acceleration_x = 0
        self.acceleration_y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, CIRCLE_COLOR, (int(self.x), int(self.y)), self.radius)

def check_collision(circle1, circle2):
    distance = math.sqrt((circle2.x - circle1.x) ** 2 + (circle2.y - circle1.y) ** 2)
    return distance <= circle1.radius + circle2.radius

def resolve_collision(circle1, circle2):
    # Simple collision resolution using conservation of momentum and restitution
    # This is not physically accurate and is just for demonstration purposes
    v1_x, v1_y = circle1.velocity_x, circle1.velocity_y
    v2_x, v2_y = circle2.velocity_x, circle2.velocity_y
    m1, m2 = circle1.mass, circle2.mass

    circle1.velocity_x = ((m1 - m2) * v1_x + 2 * m2 * v2_x) / (m1 + m2)
    circle1.velocity_y = ((m1 - m2) * v1_y + 2 * m2 * v2_y) / (m1 + m2)

    circle2.velocity_x = ((m2 - m1) * v2_x + 2 * m1 * v1_x) / (m1 + m2)
    circle2.velocity_y = ((m2 - m1) * v2_y + 2 * m1 * v1_y) / (m1 + m2)

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Physics Engine Example")
    clock = pygame.time.Clock()

    circles = [
        Circle(200, 200, 30, 1),
        Circle(300, 300, 40, 1.5),
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update circles
        for circle in circles:
            circle.update(dt)

        # Check for collisions
        for i, circle1 in enumerate(circles):
            for circle2 in circles[i + 1:]:
                if check_collision(circle1, circle2):
                    resolve_collision(circle1, circle2)

        # Draw everything
        screen.fill(BG_COLOR)
        for circle in circles:
            circle.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

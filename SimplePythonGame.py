import pygame
import sys
import random


pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Air Hockey")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
RED = (255, 0, 0)


font_path = "FarenheightPersonalUseRegular-9YdJ7.ttf"
FONT = pygame.font.Font(font_path, 62)






class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.color = color

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within the screen bounds
        self.rect.y = max(0, min(screen_height - 100, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Puck:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.radius = 10
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Check for collisions with walls
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y = -self.speed_y

    def check_collision(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.speed_x = -self.speed_x

    def off_screen(self):
        return self.rect.right < 0

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, self.radius)


player_paddle = Paddle(50, 250, SKY_BLUE)   # Sky blue for player paddle
ai_paddle = Paddle(730, 250, RED)          # Red for computer paddle
puck = Puck(390, 290)


stars = [(random.randint(0, screen_width), random.randint(0, screen_height)) for _ in range(50)]


def main():
    round_over = False
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not round_over:

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_paddle.move(-5)
            if keys[pygame.K_DOWN]:
                player_paddle.move(5)


            if puck.rect.centery < ai_paddle.rect.centery:
                ai_paddle.move(-5)
            elif puck.rect.centery > ai_paddle.rect.centery:
                ai_paddle.move(5)


            puck.move()


            puck.check_collision(player_paddle)
            puck.check_collision(ai_paddle)


            if puck.off_screen():
                round_over = True


        screen.fill(BLACK)

        # stars
        for star in stars:
            pygame.draw.circle(screen, WHITE, star, 1)


        player_paddle.draw()
        ai_paddle.draw()
        puck.draw()

        if round_over:

            text = FONT.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(screen_width//2, screen_height//2))
            screen.blit(text, text_rect)


        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

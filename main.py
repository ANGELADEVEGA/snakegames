import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.move()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE

class Snake:
    def __init__(self, parent_screen, color):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.color = color

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, (255, 0, 0))  # Single Player (Red)
        self.apple = Apple(self.surface)
        
        self.game_over = False

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface, (255, 0, 0))
        self.apple = Apple(self.surface)
        self.game_over = False

    def is_collision(self, x1, y1, x2, y2):
        return x1 >= x2 and x1 < x2 + SIZE and y1 >= y2 and y1 < y2 + SIZE

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # Check for collisions
        self.check_collisions()

    def check_collisions(self):
        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                self.game_over = True
                raise Exception("Player Collision Occurred")

        # Check for wall collision
        if (self.snake.x[0] < 0 or self.snake.x[0] >= 1000 or 
            self.snake.y[0] < 0 or self.snake.y[0] >= 800):
            self.play_sound('crash')
            self.game_over = True
            raise Exception("Player Collision Occurred")

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to restart or Escape to exit!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if self.game_over and event.key == K_RETURN:  # Restart with Enter key
                        self.reset()  

                if not self.game_over:
                    if event.type == KEYDOWN:
                        if event.key == K_LEFT:  # Move left
                            self.snake.move_left()
                        if event.key == K_RIGHT:  # Move right
                            self.snake.move_right()
                        if event.key == K_UP:  # Move up
                            self.snake.move_up()
                        if event.key == K_DOWN:  # Move down
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not self.game_over:
                    self.play()

            except Exception:
                self.show_game_over()
                self.game_over = True

            time.sleep(0.25)

if __name__ == '__main__':
    game = Game()
    game.run()

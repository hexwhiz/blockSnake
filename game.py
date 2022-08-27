import pygame
from pygame.locals import *
import time
import random
from pathlib import Path

# initializing block size
SIZE = 40
BASE_DIR = Path(__file__).resolve().parent

class Apple:
    def __init__(self, parent_screen):
        # initializing basic attributes about apple
        self.parent_screen = parent_screen

        # loading apple's image
        self.image = pygame.image.load(BASE_DIR / "resources/apple.jpg").convert()

        # apple's initial position
        self.x = 120
        self.y = 120

    def draw(self):
        # to draw apple with x and y as its positional axis
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
        # to display it on screeen and showing the changes made

    def move(self):
        # for moving apple to random places after being eaten
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        # initializing basic attributes about snake
        self.parent_screen = parent_screen

        # loading block(snake's image)
        self.image = pygame.image.load(BASE_DIR / "resources/block.jpg").convert()

        # snake's (initial) direction until and unless any key is pressed
        self.direction = 'down'

        # snake's initial size
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
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        # specifying directions and changes to be made on each direction in x and y position of element(snake)
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
        pygame.display.set_caption("Snake And Apple Game")

        # for background music
        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load(BASE_DIR / 'resources/bg_music_1.wav')
        pygame.mixer.music.play(-1, 0)
        # it will always play and that too from the starting

    def play_sound(self, sound_name):
        # for ingame sound
        if sound_name == "crash":
            sound = pygame.mixer.Sound(BASE_DIR / "resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound(BASE_DIR / "resources/ding.mp3")

        pygame.mixer.Sound.play(sound)
        # pygame.mixer.music.stop()


    def reset(self):
        # reseting the game
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)


    def is_collision(self, x1, y1, x2, y2):
        # x1,x2,y1,y2 are snake(block) and apple positional axis
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def background_image(self):
        bg = pygame.image.load(BASE_DIR / "resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.background_image()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
                # raising exception

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"

    def display_score(self):
        # sysfont module for font type and size
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length-1}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    def show_game_over(self):
        self.background_image()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press 'ENTER' to play again . Press 'ESCAPE' to exit !!!!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        # using flag to pause game
        pause = False

        while running:
            for event in pygame.event.get():
            # To capture mouse and keyboard activity
                if event.type == KEYDOWN:
                # To check which key is pressed
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            # catching exception 
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            # using time module
            time.sleep(.1)

if __name__ == '__main__':
    game = Game()
    game.run()
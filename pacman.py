# Build Pac-Man from Scratch in Python with PyGame!!
import copy
from board import board
import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pac-Man")
icon = pygame.image.load(f'assets/pac/1.png')
pygame.display.set_icon(icon)
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
lvl = copy.deepcopy(board)
color = '#2121DE'
PI = math.pi
player_images = []
for x in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/pac/{x}.png'), (45, 45)))
blinky_char = pygame.transform.scale(pygame.image.load(f'assets/ghost/red.png'), (45, 45))
pinky_char = pygame.transform.scale(pygame.image.load(f'assets/ghost/pink.png'), (45, 45))
inky_char = pygame.transform.scale(pygame.image.load(f'assets/ghost/blue.png'), (45, 45))
clyde_char = pygame.transform.scale(pygame.image.load(f'assets/ghost/orange.png'), (45, 45))
spooked_char = pygame.transform.scale(pygame.image.load(f'assets/ghost/powerup.png'), (45, 45))
dead_char = pygame.transform.scale(pygame.image.load(f'assets/ghost/dead.png'), (45, 45))
pac_x = 450
pac_y = 663
direct = 0
blinky_x = 56
blinky_y = 58
blinky_direct = 0
inky_x = 440
inky_y = 388
inky_direct = 2
pinky_x = 440
pinky_y = 438
pinky_direct = 2
clyde_x = 440
clyde_y = 438
clyde_driect = 2
counter = 0
flicker = False
# Directions R, L, U, D = 0, 1, 2, 3
valid = [False, False, False, False]
direct_cmd = 0
pac_speed = 2
score = 0
power = False
power_counter = 0
eat = [False, False, False, False]
target = [(pac_x, pac_y), (pac_x, pac_y), (pac_x, pac_y), (pac_x, pac_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speed = [2, 2, 2, 2]
start_counter = 0
lives = 3
game_over = False
game_won = False


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direct = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turn, self.in_box = self.check_colls()
        self.rect = self.draw()


    def draw(self):
        # Draw the ghost character on the board
        if (not power and not self.dead) or (eat[self.id] and power and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif power and not self.dead and not eat[self.id]:
            screen.blit(spooked_char, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_char, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect


    def check_colls(self):
        # Check for collisions
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turn = [False, False, False, False]

        if 0 < self.center_x // 30 < 29:
            if lvl[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turn[2] = True

            if lvl[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (lvl[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turn[1] = True

            if lvl[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (lvl[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                self.turn[0] = True

            if lvl[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (lvl[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                self.turn[3] = True

            if lvl[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (lvl[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                self.turn[2] = True

            if self.direct == 2 or self.direct == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if lvl[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (lvl[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[3] = True

                    if lvl[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (lvl[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[2] = True

                if 12 <= self.center_y % num1 <= 18:
                    if lvl[self.center_y // num1][(self.center_x - num2) // num2] < 3 or (lvl[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[1] = True

                    if lvl[self.center_y // num1][(self.center_x + num2) // num2] < 3 or (lvl[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[0] = True

            if self.direct == 0 or self.direct == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if lvl[(self.center_y + num3) // num1][self.center_x // num2] < 3 or (lvl[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[3] = True

                    if lvl[(self.center_y - num3) // num1][self.center_x // num2] < 3 or (lvl[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[2] = True

                if 12 <= self.center_y % num1 <= 18:
                    if lvl[self.center_y // num1][(self.center_x - num3) // num2] < 3 or (lvl[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[1] = True

                    if lvl[self.center_y // num1][(self.center_x + num3) // num2] < 3 or (lvl[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (self.in_box or self.dead)):
                        self.turn[0] = True

        else:
            self.turn[0] = True
            self.turn[1] = True

        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True

        else:
            self.in_box = False

        return self.turn, self.in_box


    def move_clyde(self):
        # clyde is going to turn whenever it is advantageous for pursuit
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turn[0]:
                self.x_pos += self.speed

            elif not self.turn[0]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

            elif self.turn[0]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                if self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                else:
                    self.x_pos += self.speed

        elif self.direct == 1:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.direct = 3

            elif self.target[0] < self.x_pos and self.turn[1]:
                self.x_pos -= self.speed

            elif not self.turn[1]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[1]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                if self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                else:
                    self.x_pos -= self.speed

        elif self.direct == 2:
            if self.target[0] < self.x_pos and self.turn[1]:
                self.direct = 1
                self.x_pos -= self.speed

            elif self.target[1] < self.y_pos and self.turn[2]:
                self.direct = 2
                self.y_pos -= self.speed

            elif not self.turn[2]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[2]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                else:
                    self.y_pos -= self.speed

        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.y_pos += self.speed

            elif not self.turn[3]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[3]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                else:
                    self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900

        elif self.x_pos > 900:
            self.x_pos - 30

        return self.x_pos, self.y_pos, self.direct


    def move_blinky(self):
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turn[0]:
                self.x_pos += self.speed

            elif not self.turn[0]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

            elif self.turn[0]:
                self.x_pos += self.speed

        elif self.direct == 1:
            if self.target[0] < self.x_pos and self.turn[1]:
                self.x_pos -= self.speed

            elif not self.turn[1]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[1]:
                self.x_pos -= self.speed

        elif self.direct == 2:
            if self.target[1] < self.y_pos and self.turn[2]:
                self.direct = 2
                self.y_pos -= self.speed

            elif not self.turn[2]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

            elif self.turn[2]:
                self.y_pos -= self.speed

        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.y_pos += self.speed

            elif not self.turn[3]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

            elif self.turn[3]:
                self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900

        elif self.x_pos > 900:
            self.x_pos - 30

        return self.x_pos, self.y_pos, self.direct

    def move_inky(self):
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turn[0]:
                self.x_pos += self.speed

            elif not self.turn[0]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

            elif self.turn[0]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                if self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                else:
                    self.x_pos += self.speed

        elif self.direct == 1:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.direct = 3

            elif self.target[0] < self.x_pos and self.turn[1]:
                self.x_pos -= self.speed

            elif not self.turn[1]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[1]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                if self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                else:
                    self.x_pos -= self.speed

        elif self.direct == 2:
            if self.target[1] < self.y_pos and self.turn[2]:
                self.direct = 2
                self.y_pos -= self.speed

            elif not self.turn[2]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[2]:
                self.y_pos -= self.speed

        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.y_pos += self.speed

            elif not self.turn[3]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[3]:
                self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900

        elif self.x_pos > 900:
            self.x_pos - 30

        return self.x_pos, self.y_pos, self.direct


    def move_pinky(self):
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direct == 0:
            if self.target[0] > self.x_pos and self.turn[0]:
                self.x_pos += self.speed

            elif not self.turn[0]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

            elif self.turn[0]:
                self.x_pos += self.speed

        elif self.direct == 1:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.direct = 3

            elif self.target[0] < self.x_pos and self.turn[1]:
                self.x_pos -= self.speed

            elif not self.turn[1]:
                if self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[1]:
                self.x_pos -= self.speed

        elif self.direct == 2:
            if self.target[0] < self.x_pos and self.turn[1]:
                self.direct = 1
                self.x_pos -= self.speed

            elif self.target[1] < self.y_pos and self.turn[2]:
                self.direct = 2
                self.y_pos -= self.speed

            elif not self.turn[2]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] > self.y_pos and self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[3]:
                    self.direct = 3
                    self.y_pos += self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[2]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                else:
                    self.y_pos -= self.speed

        elif self.direct == 3:
            if self.target[1] > self.y_pos and self.turn[3]:
                self.y_pos += self.speed

            elif not self.turn[3]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.target[1] < self.y_pos and self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[2]:
                    self.direct = 2
                    self.y_pos -= self.speed

                elif self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                elif self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

            elif self.turn[3]:
                if self.target[0] > self.x_pos and self.turn[0]:
                    self.direct = 0
                    self.x_pos += self.speed

                elif self.target[0] < self.x_pos and self.turn[1]:
                    self.direct = 1
                    self.x_pos -= self.speed

                else:
                    self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = 900

        elif self.x_pos > 900:
            self.x_pos - 30

        return self.x_pos, self.y_pos, self.direct


def misc():
    scr_txt = font.render(f'Score: {score}', True, 'white')
    screen.blit(scr_txt, (10, 920))

    if power:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)

    for x in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + x * 40, 915))

    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))

    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_colls(sco, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < pac_x < 870:
        if lvl[center_y // num1][center_x // num2] == 1:
            lvl[center_y // num1][center_x // num2] = 0
            sco += 10

        if lvl[center_y // num1][center_x // num2] == 2:
            lvl[center_y // num1][center_x // num2] = 0
            sco += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]

    return sco, power, power_count, eaten_ghosts


def board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for x in range(len(lvl)):
        for y in range(len(lvl[x])):
            if lvl[x][y] == 1:
                pygame.draw.circle(screen, 'white', (y * num2 + (0.5 * num2), x * num1 + (0.5 * num1)), 4)

            if lvl[x][y] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (y * num2 + (0.5 * num2), x * num1 + (0.5 * num1)), 10)

            if lvl[x][y] == 3:
                pygame.draw.line(screen, color, (y * num2 + (0.5 * num2), x * num1), (y * num2 + (0.5 * num2), x * num1 + num1), 3)

            if lvl[x][y] == 4:
                pygame.draw.line(screen, color, (y * num2, x * num1 + (0.5 * num1)), (y * num2 + num2, x * num1 + (0.5 * num1)), 3)

            if lvl[x][y] == 5:
                pygame.draw.arc(screen, color, [(y * num2 - (num2 * 0.4)) - 2, (x * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)

            if lvl[x][y] == 6:
                pygame.draw.arc(screen, color, [(y * num2 + (num2 * 0.5)), (x * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)

            if lvl[x][y] == 7:
                pygame.draw.arc(screen, color, [(y * num2 + (num2 * 0.5)), (x * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)

            if lvl[x][y] == 8:
                pygame.draw.arc(screen, color, [(y * num2 - (num2 * 0.4)) - 2, (x * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)

            if lvl[x][y] == 9:
                pygame.draw.line(screen, 'white', (y * num2, x * num1 + (0.5 * num1)), (y * num2 + num2, x * num1 + (0.5 * num1)), 3)


def pac():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direct == 0:
        screen.blit(player_images[counter // 5], (pac_x, pac_y))

    elif direct == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (pac_x, pac_y))

    elif direct == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (pac_x, pac_y))

    elif direct == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (pac_x, pac_y))


def pos(centx, centy):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centx // 30 < 29:
        if direct == 0:
            if lvl[centy // num1][(centx - num3) // num2] < 3:
                turns[1] = True

        if direct == 1:
            if lvl[centy // num1][(centx + num3) // num2] < 3:
                turns[0] = True

        if direct == 2:
            if lvl[(centy + num3) // num1][centx // num2] < 3:
                turns[3] = True

        if direct == 3:
            if lvl[(centy - num3) // num1][centx // num2] < 3:
                turns[2] = True

        if direct == 2 or direct == 3:
            if 12 <= centx % num2 <= 18:
                if lvl[(centy + num3) // num1][centx // num2] < 3:
                    turns[3] = True

                if lvl[(centy - num3) // num1][centx // num2] < 3:
                    turns[2] = True

            if 12 <= centy % num1 <= 18:
                if lvl[centy // num1][(centx - num2) // num2] < 3:
                    turns[1] = True

                if lvl[centy // num1][(centx + num2) // num2] < 3:
                    turns[0] = True

        if direct == 0 or direct == 1:
            if 12 <= centx % num2 <= 18:
                if lvl[(centy + num1) // num1][centx // num2] < 3:
                    turns[3] = True

                if lvl[(centy - num1) // num1][centx // num2] < 3:
                    turns[2] = True

            if 12 <= centy % num1 <= 18:
                if lvl[centy // num1][(centx - num3) // num2] < 3:
                    turns[1] = True

                if lvl[centy // num1][(centx + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns


def pac_move(play_x, play_y):
    # r, l, u, d
    if direct == 0 and valid[0]:
        play_x += pac_speed

    elif direct == 1 and valid[1]:
        play_x -= pac_speed

    if direct == 2 and valid[2]:
        play_y -= pac_speed

    elif direct == 3 and valid[3]:
        play_y += pac_speed

    return play_x, play_y


def capture(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if pac_x < 450:
        runaway_x = 900

    else:
        runaway_x = 0

    if pac_y < 450:
        runaway_y = 900

    else:
        runaway_y = 0

    return_target = (380, 400)

    if power:
        if not blinky.dead and not eat[0]:
            blink_target = (runaway_x, runaway_y)

        elif not blinky.dead and eat[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)

            else:
                blink_target = (pac_x, pac_y)

        else:
            blink_target = return_target

        if not inky.dead and not eat[1]:
            ink_target = (runaway_x, pac_y)

        elif not inky.dead and eat[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)

            else:
                ink_target = (pac_x, pac_y)

        else:
            ink_target = return_target

        if not pinky.dead:
            pink_target = (pac_x, runaway_y)

        elif not pinky.dead and eat[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)

            else:
                pink_target = (pac_x, pac_y)

        else:
            pink_target = return_target

        if not clyde.dead and not eat[3]:
            clyd_target = (450, 450)

        elif not clyde.dead and eat[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)

            else:
                clyd_target = (pac_x, pac_y)

        else:
            clyd_target = return_target

    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)

            else:
                blink_target = (pac_x, pac_y)

        else:
            blink_target = return_target

        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)

            else:
                ink_target = (pac_x, pac_y)

        else:
            ink_target = return_target

        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)

            else:
                pink_target = (pac_x, pac_y)

        else:
            pink_target = return_target

        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)

            else:
                clyd_target = (pac_x, pac_y)

        else:
            clyd_target = return_target

    return [blink_target, ink_target, pink_target, clyd_target]


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False

    else:
        counter = 0
        flicker = True

    if power and power_counter < 600:
        power_counter += 1

    elif power and power_counter >= 600:
        power_counter = 0
        power = False
        eat = [False, False, False, False]

    if start_counter < 180 and not game_over and not game_won:
        moving = False
        start_counter += 1

    else:
        moving = True

    screen.fill('black')
    board()
    center_x = pac_x + 23
    center_y = pac_y + 24
    if power:
        ghost_speed = [1, 1, 1, 1]

    else:
        ghost_speed = [2, 2, 2, 2]

    if eat[0]:
        ghost_speed[0] = 2

    if eat[1]:
        ghost_speed[1] = 2

    if eat[2]:
        ghost_speed[2] = 2

    if eat[3]:
        ghost_speed[3] = 2

    if blinky_dead:
        ghost_speed[0] = 4

    if inky_dead:
        ghost_speed[1] = 4

    if pinky_dead:
        ghost_speed[2] = 4

    if clyde_dead:
        ghost_speed[3] = 4

    game_won = True

    for x in range(len(lvl)):
        if 1 in lvl[x] or 2 in lvl[x]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    pac()
    blinky = Ghost(blinky_x, blinky_y, target[0], ghost_speed[0], blinky_char, blinky_direct, blinky_dead,
                   blinky_box, 0)
    inky = Ghost(inky_x, inky_y, target[1], ghost_speed[1], inky_char, inky_direct, inky_dead,
                 inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, target[2], ghost_speed[2], pinky_char, pinky_direct, pinky_dead,
                  pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, target[3], ghost_speed[3], clyde_char, clyde_driect, clyde_dead,
                  clyde_box, 3)
    misc()
    target = capture(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

    valid = pos(center_x, center_y)
    if moving:
        pac_x, pac_y = pac_move(pac_x, pac_y)
        if not blinky_dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direct = blinky.move_blinky()

        else:
            blinky_x, blinky_y, blinky_direct = blinky.move_clyde()

        if not pinky_dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direct = pinky.move_pinky()

        else:
            pinky_x, pinky_y, pinky_direct = pinky.move_clyde()

        if not inky_dead and not inky.in_box:
            inky_x, inky_y, inky_direct = inky.move_inky()

        else:
            inky_x, inky_y, inky_direct = inky.move_clyde()
        clyde_x, clyde_y, clyde_driect = clyde.move_clyde()

    score, power, power_counter, eat = check_colls(score, power, power_counter, eat)
    # add to if not powerup to check if eaten ghosts
    if not power:
        if (player_circle.colliderect(blinky.rect) and not blinky.dead) or (player_circle.colliderect(inky.rect) and not inky.dead) or (player_circle.colliderect(pinky.rect) and not pinky.dead) or (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                start_counter = 0
                power = False
                power_counter = 0
                pac_x = 450
                pac_y = 663
                direct = 0
                direct_cmd = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direct = 0
                inky_x = 440
                inky_y = 388
                inky_direct = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direct = 2
                clyde_x = 440
                clyde_y = 438
                clyde_driect = 2
                eat = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False

            else:
                game_over = True
                moving = False
                start_counter = 0

    if power and player_circle.colliderect(blinky.rect) and eat[0] and not blinky.dead:
        if lives > 0:
            power = False
            power_counter = 0
            lives -= 1
            start_counter = 0
            pac_x = 450
            pac_y = 663
            direct = 0
            direct_cmd = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direct = 0
            inky_x = 440
            inky_y = 388
            inky_direct = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direct = 2
            clyde_x = 440
            clyde_y = 438
            clyde_driect = 2
            eat = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False

        else:
            game_over = True
            moving = False
            start_counter = 0

    if power and player_circle.colliderect(inky.rect) and eat[1] and not inky.dead:
        if lives > 0:
            power = False
            power_counter = 0
            lives -= 1
            start_counter = 0
            pac_x = 450
            pac_y = 663
            direct = 0
            direct_cmd = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direct = 0
            inky_x = 440
            inky_y = 388
            inky_direct = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direct = 2
            clyde_x = 440
            clyde_y = 438
            clyde_driect = 2
            eat = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False

        else:
            game_over = True
            moving = False
            start_counter = 0

    if power and player_circle.colliderect(pinky.rect) and eat[2] and not pinky.dead:
        if lives > 0:
            power = False
            power_counter = 0
            lives -= 1
            start_counter = 0
            pac_x = 450
            pac_y = 663
            direct = 0
            direct_cmd = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direct = 0
            inky_x = 440
            inky_y = 388
            inky_direct = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direct = 2
            clyde_x = 440
            clyde_y = 438
            clyde_driect = 2
            eat = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False

        else:
            game_over = True
            moving = False
            start_counter = 0

    if power and player_circle.colliderect(clyde.rect) and eat[3] and not clyde.dead:
        if lives > 0:
            power = False
            power_counter = 0
            lives -= 1
            start_counter = 0
            pac_x = 450
            pac_y = 663
            direct = 0
            direct_cmd = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direct = 0
            inky_x = 440
            inky_y = 388
            inky_direct = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direct = 2
            clyde_x = 440
            clyde_y = 438
            clyde_driect = 2
            eat = [False, False, False, False]
            blinky_dead = False
            inky_dead = False
            clyde_dead = False
            pinky_dead = False

        else:
            game_over = True
            moving = False
            start_counter = 0

    if power and player_circle.colliderect(blinky.rect) and not blinky.dead and not eat[0]:
        blinky_dead = True
        eat[0] = True
        score += (2 ** eat.count(True)) * 100

    if power and player_circle.colliderect(inky.rect) and not inky.dead and not eat[1]:
        inky_dead = True
        eat[1] = True
        score += (2 ** eat.count(True)) * 100

    if power and player_circle.colliderect(pinky.rect) and not pinky.dead and not eat[2]:
        pinky_dead = True
        eat[2] = True
        score += (2 ** eat.count(True)) * 100

    if power and player_circle.colliderect(clyde.rect) and not clyde.dead and not eat[3]:
        clyde_dead = True
        eat[3] = True
        score += (2 ** eat.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direct_cmd = 0

            if event.key == pygame.K_LEFT:
                direct_cmd = 1

            if event.key == pygame.K_UP:
                direct_cmd = 2

            if event.key == pygame.K_DOWN:
                direct_cmd = 3

            if event.key == pygame.K_SPACE and (game_over or game_won):
                power = False
                power_counter = 0
                lives -= 1
                start_counter = 0
                pac_x = 450
                pac_y = 663
                direct = 0
                direct_cmd = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direct = 0
                inky_x = 440
                inky_y = 388
                inky_direct = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direct = 2
                clyde_x = 440
                clyde_y = 438
                clyde_driect = 2
                eat = [False, False, False, False]
                blinky_dead = False
                inky_dead = False
                clyde_dead = False
                pinky_dead = False
                score = 0
                lives = 3
                lvl = copy.deepcopy(board)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direct_cmd == 0:
                direct_cmd = direct

            if event.key == pygame.K_LEFT and direct_cmd == 1:
                direct_cmd = direct

            if event.key == pygame.K_UP and direct_cmd == 2:
                direct_cmd = direct

            if event.key == pygame.K_DOWN and direct_cmd == 3:
                direct_cmd = direct

    if direct_cmd == 0 and valid[0]:
        direct = 0

    if direct_cmd == 1 and valid[1]:
        direct = 1

    if direct_cmd == 2 and valid[2]:
        direct = 2

    if direct_cmd == 3 and valid[3]:
        direct = 3

    if pac_x > 900:
        pac_x = -47

    elif pac_x < -50:
        pac_x = 897

    if blinky.in_box and blinky_dead:
        blinky_dead = False

    if inky.in_box and inky_dead:
        inky_dead = False

    if pinky.in_box and pinky_dead:
        pinky_dead = False

    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()


# sound effects, restart and winning messages
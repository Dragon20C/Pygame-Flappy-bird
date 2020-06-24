import sys
import pygame
import random

pygame.init()
pygame.display.set_caption("Slivering snake")
window = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
black = 0, 0, 0
red = 255, 0, 0
score = 0
font = pygame.font.SysFont("segoe ui", 34, True)
sound = pygame.mixer.Sound("Ding Sound Effect.wav")


class Player:
    def __init__(self, x, y, w, h, s):
        self.x, self.y, self.width, self.height,self.speed = x, y, w, h, s
        self.colour = 0, 0, 255

    def movement(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_w] or self.keys[pygame.K_UP]:
            self.y -= self.speed

    def gravity(self):
        self.y += 4

    def draw(self):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))


player = Player(60, 200, 50, 50, 10)


class Pipes:
    def __init__(self, x, y, w, h, s):
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.speed = s
        self.colour = 0, 255, 0
        self.passed = False

    def movement(self):
        self.x -= self.speed
        if self.x < -95:
            self.x = 1030
            location = random.randint(-300, 300)
            self.y = location
            self.passed = False

    def score(self, player_rect):
        if not self.passed and player_rect.colliderect(pygame.Rect(self.x, 0, 1, 1024)):
            self.passed = True
            return True
        return False

    def collide(self, player_rect):
        rect1 = pygame.Rect(self.x, self.y - 300, self.width, self.height)
        rect2 = pygame.Rect(self.x, self.y + 490, self.width, self.height)
        return player_rect.colliderect(rect1) or player_rect.colliderect(rect2)

    def draw(self):
        pygame.draw.rect(window, self.colour, (self.x, self.y - 300, self.width, self.height))
        pygame.draw.rect(window, self.colour, (self.x, self.y + 490, self.width, self.height))


pipe_list = [
    Pipes(900, 0, 70, 600, 3.5),
    Pipes(1450, 0, 70, 600, 3.5)]

class Scene:
    def __init__(self):
        self.sceneNum = 1

    def Scene_1(self):
        pass

    def Scene_2(self):
        pass

    def Draw_Scene(self):
        if self.sceneNum == 1:
            self.Scene_1()
        elif self.sceneNum == 2:
            self.Scene_2()


running = True
while running:
    window.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    player.gravity()
    player.movement()

    for pipe in pipe_list:
        pipe.movement()
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for pipe in pipe_list:
        if pipe.collide(player_rect):
            running = False
    for pipe in pipe_list:
        if pipe.score(player_rect):
            score += 1
            sound.play()
            # pygame.mixer.music.play(0)

    text = font.render("Score " + str(score), True, red)

    for pipe in pipe_list:
        pipe.draw()

    player.draw()
    window.blit(text, (30, 20))
    clock.tick(60)
    pygame.display.flip()

import pygame
import random
import sys
import os
from pygame.locals import *
pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

BG = pygame.image.load(os.path.join("Assets/Other","Track.png"))
FONT = pygame.font.SysFont("comicsans",30)

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino","DinoJump.png"))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino","DinoRun1.png")),
pygame.image.load(os.path.join("Assets/Dino","DinoRun2.png"))]
global game_speed, x_pos_BG, y_pos_BG, points, obstacles, dinosaurs
game_speed = 20
x_pos_BG = 0 
y_pos_BG = 380
points = 0
print(BG.get_width(), BG.get_height())

class Dinosour:
	x_pos = 80
	y_pos = 310
	JUMP_VEL = 8.5


	def __init__(self,img = RUNNING[0]):
		self.image = img 
		self.step_index = 0
		self.rect = pygame.Rect(self.x_pos, self.y_pos, img.get_width(), img.get_height())
		self.dino_run = True
		self.dino_jump = False
		self.jump_vel = self.JUMP_VEL

	def update(self):
		if self.dino_run:
			self.run()
		if self.dino_jump:
			self.jump()

	def run(self):
		self.image = RUNNING[self.step_index // 5]
		self.step_index = (self.step_index + 1)%10

	def jump(self):
		self.image = JUMPING
		if(self.dino_jump):
			self.rect.y -= self.jump_vel * 4
			self.jump_vel-=0.8
		# print(self.JUMP_VEL)
		if self.rect.y >= self.y_pos:
			self.dino_jump = False
			self.dino_run = True
			self.jump_vel = self.JUMP_VEL
			self.rect.y = self.y_pos

		# if self.jump_vel <= -self.JUMP_VEL:
		# 	self.dino_jump = False
		# 	self.dino_run = True
		# 	self.jump_vel = self.JUMP_VEL

		# self.image = JUMPING
		# if self.dino_jump:
		# 	self.rect.y -= self.jump_vel * 4
		# 	self.jump_vel -= 0.8
		# if self.jump_vel <= -self.JUMP_VEL:
		# 	self.dino_jump = False
		# 	self.dino_run = True
		# 	self.jump_vel = self.JUMP_VEL

	def draw(self,SCREEN):
		SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Obstacle:
	def __init__(self, image, number_of_cacti):
		self.image = image
		self.type = number_of_cacti
		self.rect = self.image[self.type].get_rect()
		self.rect.x = SCREEN_WIDTH

	def update(self):
		self.rect.x -= game_speed
		if(self.rect.x + self.rect.width <=0):
			obstacles.pop()

	def draw(self, SCREEN):
		SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
	def __init__(self, image, number_of_cacti):
		super().__init__(image,number_of_cacti)
		self.rect.y = 325

class LargeCactus(Obstacle):
	def __init__(self, image, number_of_cacti):
		super().__init__(image,number_of_cacti)
		self.rect.y = 300

def score():
	global game_speed, points
	points+=1
	if points %100 == 0:
		game_speed+=1

	text = FONT.render("Points: " + str(points), True, (0,0,0))
	SCREEN.blit(text, (950,50))


def background():
	global x_pos_BG, y_pos_BG, game_speed
	w = BG.get_width()
	SCREEN.blit(BG,(x_pos_BG, y_pos_BG))
	SCREEN.blit(BG,(x_pos_BG + w, y_pos_BG))
	if(x_pos_BG + w <=0):
		x_pos_BG = 0 
	x_pos_BG -= game_speed

def remove(index):
	dinosaurs.pop(index)


def main():
	global obstacles, dinosaurs
	clock = pygame.time.Clock()
	run = True 
	obstacles = []
	dinosaurs = [Dinosour()]
	# print(x_pos_BG,y_pos_BG)
	while run:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		SCREEN.fill((255,255,255))
		background()
		score()
		for dinosaur in dinosaurs:
			dinosaur.update()
			dinosaur.draw(SCREEN)

		if len(dinosaurs) == 0:
			break

		if(len(obstacles) == 0):
			rand_int = random.randint(0,1)
			if(rand_int ==0):
				obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0,2)))
			elif(rand_int == 1):
				obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0,2)))

		for obstacle in obstacles:
			obstacle.draw(SCREEN)
			obstacle.update()
			for i, dinosaur in enumerate(dinosaurs):
				if dinosaur.rect.colliderect(obstacle.rect):
					remove(i)







		user_input = pygame.key.get_pressed()
		for i, dinosaur in enumerate(dinosaurs):
			if user_input[pygame.K_SPACE]:
				dinosaur.dino_jump = True
				dinosaur.dino_run = False


		clock.tick(60)
		pygame.display.update()

main()
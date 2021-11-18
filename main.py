import pygame
import random
import sys
import os
from pygame.locals import *
pygame.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

BG = pygame.image.load(os.path.join("Assets/Other","Track.png"))

JUMPING = pygame.image.load(os.path.join("Assets/Dino","DinoJump.png"))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino","DinoRun1.png")),
pygame.image.load(os.path.join("Assets/Dino","DinoRun2.png"))]


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

def main():
	clock = pygame.time.Clock()
	run = True 
	dino = Dinosour()
	while run:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		user_input = pygame.key.get_pressed()
		if user_input[pygame.K_SPACE]:
			dino.dino_jump = True 
			dino.dino_run = False
		SCREEN.fill((255,255,255))
		dino.draw(SCREEN)
		dino.update()
		print(dino.rect.y)
		clock.tick(30)
		pygame.display.update()

main()
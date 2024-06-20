import pygame
import sys
import os

pygame.init() 

def get_file(name):
    
	return os.path.join(os.path.dirname(__file__), name)

class Button():
	def __init__(self, x, y, image, hover_img, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.hover_img = pygame.transform.scale(hover_img, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
	
		pos = pygame.mouse.get_pos()
		surface.blit(self.image, (self.rect.x, self.rect.y))

		
		if self.rect.collidepoint(pos):   
			surface.blit(self.hover_img, (self.rect.x, self.rect.y))
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
			

		return action
	
	def update(self, new_img):
		width = self.image.get_width()
		height = self.image.get_height()
		
		self.image = pygame.transform.scale(new_img, (width, height))
		self.hover_img = self.image

	def hover(self, surface):
		return self.rect.collidepoint(pygame.mouse.get_pos())
	
	def not_hover(self, surface):
		return not self.hover(self, surface)

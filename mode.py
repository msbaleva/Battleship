import pygame
import sys
import os
import Button
import math
import random
import operator
import game
import imp


pygame.init()

def get_file(name):
	return os.path.join(os.path.dirname(__file__), name)


clock = pygame.time.Clock()
w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
bg = pygame.transform.scale(pygame.image.load(get_file('Layout\\bg.jpg')), (w, h))
logo = pygame.transform.scale(pygame.image.load(get_file('Layout\\logo.png')), (w * 0.3, h * 0.15))
logo_w = logo.get_width()
logo_h = logo.get_height()
logo_x = w / 2 - logo_w/2
logo_y = h * 0.03
logo_point = (logo_x, logo_y)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Battleship")



border = pygame.transform.scale(pygame.image.load(get_file('Layout\\rope.png')), (w * 0.1, h))
b1_point = (- border.get_width() / 3.5, 0)
b2_point = (w - border.get_width() / 1.4 , 0)

menu = pygame.transform.scale(pygame.image.load(get_file('Layout\\border_menu.png')), (h * 0.8, h * 0.8))



modes = ["easy", "medium", "hard"]
mode_buttons = list()

option = "back-to-menu"
image = pygame.image.load(get_file(f"Button\\button_{option}.png")).convert_alpha()
hover_img = pygame.image.load(get_file(f"Button\\button_{option}_hover.png")).convert_alpha()
img_w = image.get_width()
img_x = w / 2 - img_w / 2
img_y = h * 0.9
btn = Button.Button(img_x, img_y, image, hover_img, 1)


for mode in modes:
	mode_image = pygame.image.load(get_file(f"Button\\button_{mode}.png")).convert_alpha()
	mode_hover_img = pygame.image.load(get_file(f"Button\\button_{mode}_hover.png")).convert_alpha()
	mode_img_w = mode_image.get_width()
	mode_img_h = mode_image.get_height()
	mode_img_x = w / 2 - mode_img_w / 2
	mode_img_y = logo_y + logo_h + menu.get_width() / 3.7 + (mode_img_h + 10) * modes.index(mode) 
	mode_buttons.append(Button.Button(mode_img_x, mode_img_y, mode_image, mode_hover_img, 1))

chest = pygame.transform.scale(pygame.image.load(get_file('Layout\\chest.png')), (w * 0.09, h * 0.12))
chest_w = chest.get_width()
chest_h = chest.get_height()
chest_x = w /2 - chest_w /2 - w * 0.03
chest_y = h * 0.9 - menu.get_width() / 3.4
chest_point = (chest_x, chest_y)



def init(screen, user, coins):
	
	pygame.font.init()
	font = pygame.font.SysFont('Roboto', int(h * 0.05), True)
	total_coins_surface = font.render(str(coins), False, (239, 204, 0))
	total_coin_surface_point = (chest_x + w * 0.09, chest_y + h * 0.03)
	run = True
	while run:
		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		screen.blit(chest, chest_point)
		screen.blit(total_coins_surface, total_coin_surface_point)
		screen.blit(border, b1_point)
		screen.blit(border, b2_point)
		screen.blit(menu, (w / 2 - menu.get_width()/2, logo_h))
		
		if mode_buttons[0].draw(screen):
			run = False
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
			game.init_boards(screen, "easy", user, coins)
			
		elif coins == 0:
			continue
		elif mode_buttons[1].draw(screen):
			run = False
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
			game.init_boards(screen, "medium", user, coins - 1)
		elif mode_buttons[2].draw(screen):
			run = False
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
			game.init_boards(screen, "hard", user, coins - 1)
		elif btn.draw(screen):
			run = False

	
		for b in mode_buttons:
			if (btn.hover(screen) or b.hover(screen)):
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
				break
			else:
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
		clock.tick(100)
		for event in pygame.event.get():		
		
			if event.type == pygame.QUIT:
				run = False
			
				
		
	
		pygame.display.flip()
		pygame.display.update()
	
	imp.reload(game)
	
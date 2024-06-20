import pygame
import os
import sys
import Button

pygame.init()

def get_file(name):
	return os.path.join(os.path.dirname(__file__), name)




pygame.display.set_caption("Battleship")
w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
bg = pygame.transform.scale(pygame.image.load(get_file('Layout\\bg.jpg')), (w, h))
logo = pygame.transform.scale(pygame.image.load(get_file('Layout\\logo.png')), (w * 0.35, h * 0.17))
map = pygame.transform.scale(pygame.image.load(get_file('Panel\\rules.png')), (w * 0.8, h * 0.77))
logo_w = logo.get_width()
logo_h = logo.get_height()
map_w = map.get_width()
map_h = map.get_height()

logo_point = (w / 2 - logo_w/2, h * 0.05)
map_point = (w / 2 - map_w/2, h * 0.17)

border = pygame.transform.scale(pygame.image.load(get_file('Layout\\rope.png')), (w * 0.1, h))
b1_point = (- border.get_width() / 3.5, 0)
b2_point = (w - border.get_width() / 1.4, 0)

def show_rules(screen):
	
	option = "back-to-menu"
	image = pygame.image.load(get_file(f"Button\\button_{option}.png")).convert_alpha()
	hover_img = pygame.image.load(get_file(f"Button\\button_{option}_hover.png")).convert_alpha()
	img_w = image.get_width()
	img_x = w / 2 - img_w / 2
	img_y = h * 0.9
	btn = Button.Button(img_x, img_y, image, hover_img, 1)
	run = True
	while run:

		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		screen.blit(map, map_point)
		screen.blit(border, b1_point)
		screen.blit(border, b2_point)
		if btn.draw(screen):
			run = False

		if (btn.hover(screen)):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
	
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				run = False
				# pygame.quit()
				# sys.exit()

		pygame.display.update()


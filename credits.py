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
map = pygame.transform.scale(pygame.image.load(get_file('Panel\\map.png')), (w * 0.75, h * 0.75))
logo_w = logo.get_width()
logo_h = logo.get_height()
map_w = map.get_width()
map_h = map.get_height()

pygame.font.init()
size_font = int(h * 0.03)
font = pygame.font.SysFont('Roboto', size_font, True)
font2 = pygame.font.SysFont('Roboto', int(h * 0.05), True)
logo_point = (w / 2 - logo_w/2, h * 0.05)
map_x = w / 2 - map_w/2
map_y = h * 0.2
map_point = (map_x, map_y)

border = pygame.transform.scale(pygame.image.load(get_file('Layout\\rope.png')), (w * 0.1, h))

b1_point = (- border.get_width() / 3.5, 0)
b2_point = (w - border.get_width() / 1.4 , 0)

def draw_text(text, font, text_col, x, y, screen):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def show_credits(screen):
	
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
		col = (0,0,0)
		draw_text("CREDITS", font2, col, map_x + w * 0.27, map_y + h * 0.15, screen)
		draw_text("Created by Maria Baleva" , font, col, map_x + w * 0.27, map_y + h * 0.25, screen)
		draw_text("Music score by Hans Zimmer", font, col, map_x + w * 0.27, map_y + h * 0.3, screen)
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


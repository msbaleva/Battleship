import pygame
import os
import sys
import Button
import mysql.connector as connector

pygame.init()

def get_file(name):
	return os.path.join(os.path.dirname(__file__), name)




pygame.display.set_caption("Battleship")
w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
bg = pygame.transform.scale(pygame.image.load(get_file('Layout\\bg.jpg')), (w, h))
logo = pygame.transform.scale(pygame.image.load(get_file('Layout\\logo.png')), (w * 0.35, h * 0.17))
map = pygame.transform.scale(pygame.image.load(get_file('Panel\\leaderboard.png')), (w * 0.7, h * 0.78))
logo_w = logo.get_width()
logo_h = logo.get_height()
map_w = map.get_width()
map_h = map.get_height()
screen = pygame.display.set_mode((w, h))

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
	


pygame.font.init()
size_font = int(h * 0.03)
font = pygame.font.SysFont('Roboto', size_font, True)
logo_point = (w / 2 - logo_w/2, h * 0.05)
map_x = w / 2 - map_w/2
map_point = (w / 2 - map_w/2, h * 0.2)

border = pygame.transform.scale(pygame.image.load(get_file('Layout\\rope.png')), (w * 0.1, h))
b1_point = (- border.get_width() / 3.5, 0)
b2_point = (w - border.get_width() / 1.4, 0)
col = (0,0,0)
def show(screen):
	
	option = "back-to-menu"
	image = pygame.image.load(get_file(f"Button\\button_{option}.png")).convert_alpha()
	hover_img = pygame.image.load(get_file(f"Button\\button_{option}_hover.png")).convert_alpha()
	img_w = image.get_width()
	img_x = w / 2 - img_w / 2
	img_y = h * 0.9
	btn = Button.Button(img_x, img_y, image, hover_img, 1)
	run = True

	
	connection=connector.connect(host="localhost", user="root")
	c = connection.cursor()
	c.execute("use battleship;")
	c.execute("select player.USERNAME, player.COINS, player.BATTLES, player.VICTORIES from player ORDER BY player.COINS DESC;")
	info = c.fetchall()
	
	
	connection.close()

	while run:

		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		screen.blit(map, map_point)
		screen.blit(border, b1_point)
		screen.blit(border, b2_point)
		for i in range(len(info)):
			player = info[i]
			player_h = h * 0.45 + i * w * 0.02
			draw_text(str(player[0]), font, col, map_x + w * 0.15, player_h)
			draw_text(str(player[1]), font, col, map_x + w * 0.28, player_h)
			draw_text(str(player[2]), font, col, map_x + w * 0.4, player_h)
			draw_text(str(player[3]), font, col, map_x + w * 0.53, player_h)
			
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


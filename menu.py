import pygame
import sys
import os
import credits
import rules
import login
import coins
import leaderboard
import Button


pygame.init()
pygame.mixer.init()



def get_file(name):
	return os.path.join(os.path.dirname(__file__), name)


clock = pygame.time.Clock()
w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
bg = pygame.transform.scale(pygame.image.load(get_file('Layout\\bg.jpg')), (w, h))
logo = pygame.image.load(get_file('Layout\\logo.png'))
logo_w = logo.get_width()
logo_h = logo.get_height()
logo_point = (w / 2 - logo_w/2, h * 0.17)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Battleship")
music = pygame.mixer.music.load(get_file('Sound\\theme.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1) 
options = ["new-game", "leaderboard", "coins", "how-to-play", "credits", "quit"]
imgs = []
buttons = []

border = pygame.transform.scale(pygame.image.load(get_file('Layout\\rope.png')), (w * 0.1, h))
b1_point = (- border.get_width() / 3.5, 0)
b2_point = (w - border.get_width() / 1.4 , 0)

for option in options:
	i = options.index(option)
	image = pygame.image.load(get_file(f"Button\\button_{option}.png")).convert_alpha()
	hover_img = pygame.image.load(get_file(f"Button\\button_{option}_hover.png")).convert_alpha()
	imgs.append(image)
	img_w = image.get_width()
	img_x = 0
	img_y = 0
	if (i < 3):
		img_x = logo_point[0] + logo_w / 4 - img_w / 2
		img_y = h * 0.5 + 100 * i
	else:
		img_x = logo_point[0] + logo_w * 3 / 4 - img_w / 2
		img_y = h * 0.5 + 100 * (i - 3)
	buttons.append(Button.Button(img_x, img_y, image, hover_img, 1))



def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def show_menu():
	run = True
	while run:
		
		pygame.mixer.music.set_volume(0.1)
		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)

		screen.blit(border, b1_point)
		screen.blit(border, b2_point)
 
		if buttons[0].draw(screen):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			login.login_form(screen)
		elif buttons[1].draw(screen):
			leaderboard.show(screen)
		elif buttons[2].draw(screen):
			coins.show_rules(screen)
		elif buttons[3].draw(screen):
			rules.show_rules(screen)
		elif buttons[4].draw(screen):
			credits.show_credits(screen)
		elif buttons[5].draw(screen):
			run = False
			pygame.quit()
			sys.exit()

		for btn in buttons:
			if (btn.hover(screen)):
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
				break
			else:
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				sys.exit()

		pygame.display.flip()	
		pygame.display.update()

show_menu()
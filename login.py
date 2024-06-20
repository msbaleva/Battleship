import pygame
import os
import Button
import mode
import mysql.connector as connector


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
menu_w = menu.get_width()

option = "back-to-menu"
image = pygame.image.load(get_file(f"Button\\button_{option}.png")).convert_alpha()
hover_img = pygame.image.load(get_file(f"Button\\button_{option}_hover.png")).convert_alpha()
img_w = image.get_width()
img_x = w / 2 - img_w / 2
img_y = h * 0.9
btn = Button.Button(img_x, img_y, image, hover_img, 1)

username_image = pygame.transform.scale(pygame.image.load(get_file(f"Button\\username.png")).convert_alpha(), (menu_w * 0.45, h * 0.08))
username_hover_img = pygame.image.load(get_file(f"Button\\username_hover.png")).convert_alpha()
username_img_w = username_image.get_width()
username_img_h = username_image.get_height()
username_img_x = w / 2 - username_img_w / 2
username_img_y = logo_h + menu_w/ 2.7  + 10
username_box = Button.Button(username_img_x, username_img_y, username_image, username_hover_img, 1)

password_image = pygame.transform.scale(pygame.image.load(get_file(f"Button\\password.png")).convert_alpha(), (menu_w * 0.45, h * 0.08))
password_hover_img = pygame.image.load(get_file(f"Button\\password_hover.png")).convert_alpha()
password_img_w = password_image.get_width()
password_img_h = password_image.get_height()
password_img_x = w / 2 - password_img_w / 2
password_img_y =  logo_h + menu_w / 2.7 + (username_img_h + 10) + 10
password_box = Button.Button(password_img_x, password_img_y, password_image, password_hover_img, 1)

start_image = pygame.image.load(get_file(f"Button\\button_start.png")).convert_alpha()
start_hover_img = pygame.image.load(get_file(f"Button\\button_start_hover.png")).convert_alpha()
start_img_w = start_image.get_width() * 0.9
start_img_h = start_image.get_height() * 0.9
start_img_x = w / 2 - start_img_w / 2
start_img_y = logo_h + menu_w / 2.7 + (username_img_h + 10) * 2.5 + 10
start = Button.Button(start_img_x, start_img_y, start_image, start_hover_img, 0.9)



def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def login_form(screen):

	pygame.font.init()
	size_font = int(h * 0.03)
	font = pygame.font.SysFont('Roboto', size_font, True)

	
	
	run = True
	pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
	connection=connector.connect(host="localhost", user="root")
	c = connection.cursor()
	c.execute("use battleship;")
	wrong_pass = False
	username = ""
	password = ""
	password_display = ""
	user_active = False
	pw_active = False
	while run:
		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		
		screen.blit(border, b1_point)
		screen.blit(border, b2_point)
		screen.blit(menu, (w / 2 - menu.get_width()/2, logo_h))
		
		draw_text(username, font, (50,20,20),  username_img_x - w * 0.001 , username_img_y)
		draw_text(password_display, font, (50,20,20),  password_img_x - w * 0.001, password_img_y)
		draw_text(username, font, (252,194,0),  username_img_x , username_img_y)
		draw_text(password_display, font, (252,194,0),  password_img_x, password_img_y)
		if wrong_pass:
			draw_text("Wrong password!", font, (50,20,20),  start_img_x - w * 0.001 , start_img_y - h * 0.05)
			draw_text("Wrong password!", font, (252,194,0),  start_img_x, start_img_y - h * 0.05)
		
		start.draw(screen)
		
		if username_box.draw(screen):
			pw_active = False
			user_active = True
		if password_box.draw(screen):
			user_active = False
			pw_active = True
		btn.draw(screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif start.draw(screen) and username != "" and password != "":
				run = False
						
				c.execute(f"select player.PASSWORD, player.COINS from player where player.USERNAME = \"{username}\";")
				info = c.fetchone()
				user_active = False
				pw_active = False

				if info is None:
					c.execute(f"INSERT INTO player (ID, USERNAME, PASSWORD, COINS, BATTLES, VICTORIES) VALUES (NULL, '{username}', '{password}', '30', '0', '0');")
					connection.commit()
					connection.close()
					mode.init(screen, username, 30)
				elif password == str(info[0]):
					connection.close()
					mode.init(screen, username, info[1])
				else:
					wrong_pass = True
					run = True
					
				
				
			elif btn.draw(screen):
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					if user_active:
						username = username[:-1]
					elif pw_active:
						password  = password[:-1]
						password_display = password_display[:-1]
				elif event.key == pygame.K_RETURN:
					pass
			
				elif user_active:
					username += event.unicode
				elif pw_active:
					password += event.unicode
					password_display += '*'
				
			
		
		
	
		
		if (start.hover(screen) or password_box.hover(screen) or username_box.hover(screen) or btn.hover(screen)):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
		clock.tick(100)
	

	
		pygame.display.flip()
		pygame.display.update()

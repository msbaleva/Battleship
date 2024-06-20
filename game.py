import pygame
import sys
import os
import Button
import math
import random
import operator
import mysql.connector as connector


pygame.init()

mode = "easy"
user = "user"

def get_file(name):
	return os.path.join(os.path.dirname(__file__), name)

player_board = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
				['A', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['B', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['C','W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['D','W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['E', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['F', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['G', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['H', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['I', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['J', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]
computer_board = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
				['A', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['B', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['C','W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['D','W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['E', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['F', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['G', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['H', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['I', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
				['J', 'W','W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]
player_visuals = []
computer_visuals = []
player_sunk_cnt = 0
computer_sunk_cnt = 0
player_cnt = {"Aircraft_Carrier":5,  "Battleship":4, "Destroyer":3, "Submarine":3,"Cruiser":2  }
computer_cnt = {"Aircraft_Carrier":5,  "Battleship":4, "Destroyer":3, "Submarine":3,"Cruiser":2  }
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']



clock = pygame.time.Clock()
w = pygame.display.Info().current_w
h = pygame.display.Info().current_h
bg = pygame.transform.scale(pygame.image.load(get_file('Layout\\bg.jpg')), (w, h))
logo = pygame.transform.scale(pygame.image.load(get_file('Layout\\logo.png')), (w * 0.2, h * 0.1))
logo_w = logo.get_width()
logo_h = logo.get_height()
logo_x = w / 2 - logo_w/2
logo_y = h * 0.03
logo_point = (logo_x, logo_y)
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Battleship")

coin = pygame.transform.scale(pygame.image.load(get_file('Layout\\coins.webp')), (w * 0.04, h * 0.07))
coin_w = coin.get_width()
coin_h = coin.get_height()
coin_x = logo_x - coin_w - w * 0.06
coin_y = h * 0.03 + coin_h * 0.2
coin_point = (coin_x, coin_y)

chest = pygame.transform.scale(pygame.image.load(get_file('Layout\\chest.png')), (w * 0.09, h * 0.12))
chest_w = chest.get_width()
chest_h = chest.get_height()
chest_x = coin_x - chest_w - w * 0.04
chest_y = h * 0.03 
chest_point = (chest_x, chest_y)

pygame.font.init()
font = pygame.font.SysFont('Roboto', int(coin_y), True)
coins_surface = font.render(str(0), False, (239, 204, 0))
coin_surface_point = (coin_x + w * 0.05, coin_y + h * 0.01)


total_coins_surface = font.render(str(0), False, (239, 204, 0))
total_coin_surface_point = (coin_x - w * 0.05, coin_y + h * 0.01)
total_coins = 0

ships = ["Aircraft_Carrier", "Battleship", "Destroyer", "Submarine", "Cruiser"]
sizes = {"Aircraft_Carrier":5,  "Battleship":4, "Destroyer":3, "Submarine":3,"Cruiser":2  }
ships_img = []
ship_scoreboard_p = []
ship_scoreboard_c = []
for s in ships:
	img = pygame.transform.scale(pygame.image.load(get_file(f'Scoreboard\\{s}.png')), (w * 0.2, h * 0.1))
	img_p = pygame.transform.scale(pygame.image.load(get_file(f'Scoreboard\\{s}_P_ok.png')), (w * 0.1, h * 0.1))
	img_c = pygame.transform.scale(pygame.image.load(get_file(f'Scoreboard\\{s}_C_ok.png')), (w * 0.1, h * 0.1))
	ships_img.append(img)
	ship_scoreboard_p.append(img_p)
	ship_scoreboard_c.append(img_c)

targets_hard_mode = list()

coins_lose = {"easy":-15, "medium":-10, "hard":-5}
coins_win = {"easy":3, "medium":5, "hard":10}
remaining_unsunken = 5

quit_image = pygame.image.load(get_file(f"Button\\button_quit_game.png")).convert_alpha()
quit_hover_img = pygame.image.load(get_file(f"Button\\button_quit_game_hover.png")).convert_alpha()
quit_img_w = quit_image.get_width()
quit_img_h = quit_image.get_height()
quit_img_x = logo_x + logo_w + 30
quit_img_y = logo_h / 2 - quit_img_h / 2 + logo_y
quit_btn = Button.Button(quit_img_x, quit_img_y, quit_image, quit_hover_img, 1)

flip_image = pygame.image.load(get_file(f"Button\\button_flip.png")).convert_alpha()
flip_hover_img = pygame.image.load(get_file(f"Button\\button_flip_hover.png")).convert_alpha()
flip_img_w = flip_image.get_width()
flip_img_x = w / 1.1 - flip_img_w / 2
flip_img_y = h * 0.8
flip_btn = Button.Button(flip_img_x, flip_img_y, flip_image, flip_hover_img, 0.9)

pygame.mixer.fadeout(10)


def init_boards(screen, gamemode, logged_user, total_user_coins):
	
	global mode, user, total_coins, total_coins_surface
	mode = gamemode
	user = logged_user
	total_coins = total_user_coins
	total_coins_surface = font.render(str(total_coins), False, (239, 204, 0))

	print(player_board)

	index = "W"
	for i in range(11):
		player_row = []
		computer_row = []
		for j in range(11):
			if i == 0:
				index = j
			elif j == 0:
				index = letters[i-1]
			else:
				index = "W"

			p_image = pygame.image.load(get_file(f"Board\\P_{index}.png")).convert_alpha()
			c_image = pygame.image.load(get_file(f"Board\\C_{index}.png")).convert_alpha()

			img_w = p_image.get_width() * 0.073 + 1
			p_img_x = j * img_w + w * 0.07
			p_img_y = i * img_w + h * 0.17 
			c_img_x = j * img_w + w * 0.54 
			c_img_y = i * img_w + h * 0.17
			
			player_row.append(Button.Button(p_img_x, p_img_y, p_image, p_image, 0.073))
			computer_row.append(Button.Button(c_img_x, c_img_y, c_image, c_image, 0.073))


		player_visuals.append(player_row)
		computer_visuals.append(computer_row)

	place_ships(screen)




def init_computer():
	random.seed()
	ind = 0
	while ind < len(ships):
		ship = ships[ind]
		horizontal = random.randint(0,1)
		i = random.randint(1, 10)
		j = random.randint(1, 10)
	
		no_crossing = True
		l = sizes.get(ship)
		if horizontal:
			if (j + l) > 11:
				no_crossing = False
				continue
			for k in range(l):
				if computer_board[i][j+k] != "W":
					no_crossing = False
					continue 
		else:
			if (i + l) > 11:
				no_crossing = False
				continue
			for k in range(l):
				if computer_board[i+k][j] != "W":
					no_crossing = False
					continue 

		if no_crossing:
			ii, jj = i, j
						
			for k in range(l):
				if horizontal:
					jj = j + k
				else:
					ii = i + k		
								
				computer_board[ii][jj] = f"{ship}_{k}"
				
			ind += 1
				

def place_ships(screen):
	init_computer()
	
	run = True
	ind = 0
	horizontal = True
	while run and ind < len(ships):
		
		if horizontal:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		screen.blit(coin, coin_point)
		screen.blit(chest, chest_point)
		screen.blit(coins_surface, coin_surface_point)
		screen.blit(total_coins_surface, total_coin_surface_point)
		clock.tick(100)
		ship = ships[ind]
		ship_panel = pygame.transform.scale(pygame.image.load(get_file(f'Panel\\{ship}_panel.png')), (w * 0.45, h* 0.55))
		screen.blit(ship_panel, (w * 0.5, h * 0.2))


		for i in range(5):
			screen.blit(ships_img[i], (w * i * 0.2, h * 0.9))

		
		if flip_btn.draw(screen):
			if horizontal:
				horizontal = False
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZENS)
			else:
				horizontal = True
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEWE)

	
		for event in pygame.event.get():		
		
			if event.type == pygame.QUIT:
				run = False
					

		
		for i in range(11):
			for j in range(11):
				
								
				if player_visuals[i][j].draw(screen):
					no_crossing = True
					l = sizes.get(ship)
					if horizontal:
						if (j + l) > 11:
							no_crossing = False
							break
						for k in range(l):
							if player_board[i][j+k] != "W":
								no_crossing = False
								break 
					else:
						if (i + l) > 11:
							no_crossing = False
							break
						for k in range(l):
							if player_board[i+k][j] != "W":
								no_crossing = False
								break 
					if no_crossing:
						ii, jj = i, j
						if mode == "hard":
							# targets_hard_mode.append((i,j))
							if horizontal:
								targets_hard_mode.append((i,j + random.randint(0,l - 1)))
							else:
								targets_hard_mode.append((i + random.randint(0,l - 1), j))
						for k in range(l):
							name = f"Board\\P_W_{ship}_{k}.png"
							new_img = pygame.image.load(get_file(name)).convert_alpha()
							if horizontal:
								jj = j + k
							else:
								ii = i + k		
								new_img = pygame.transform.rotate(pygame.image.load(get_file(name)).convert_alpha(), -90)			
							player_board[ii][jj] = f"{ship}_{k}"
							player_visuals[ii][jj].update(new_img)
							player_visuals[ii][jj].draw(screen)
							
						ind += 1

						pygame.mixer.Sound.play(pygame.mixer.Sound(get_file('Sound\\placeship.wav')))
					

		if quit_btn.draw(screen):
			run = False
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
			

		if (quit_btn.hover(screen)):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			

		
		pygame.display.flip()
		pygame.display.update()
	print(player_board)
	if run:
		play(screen)


def play(screen):
	global computer_sunk_cnt, player_sunk_cnt, mode, coins_surface, remaining_unsunken, total_coins, total_coins_surface
	run = True
	
	is_player_turn = True
	hitting = False
	tiles = list()
	directions = list()
	direction = "left"
	coins = 0
	if mode == "hard":
		random.seed()
		random.shuffle(targets_hard_mode)

	while run:

		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		screen.blit(coin, coin_point)
		screen.blit(chest, chest_point)
		screen.blit(coins_surface, coin_surface_point)
		screen.blit(total_coins_surface, total_coin_surface_point)
	
		for i in range(5):
			screen.blit(ship_scoreboard_p[i], (w * i * 0.2, h * 0.9))
			screen.blit(ship_scoreboard_c[i], (w * i * 0.2 + ship_scoreboard_p[i].get_width(), h * 0.9))
		clock.tick(100)
		

		for i in range(11):
			for j in range(11):
				player_visuals[i][j].draw(screen)
				computer_visuals[i][j].draw(screen)

		
		for event in pygame.event.get():		
		
			if event.type == pygame.QUIT:
				run = False

			
			if is_player_turn:

				
				for i in range(1, 11):
					for j in range(1, 11):				
								
						if computer_visuals[i][j].draw(screen):
							name = f"Board\\missed_W.png"
							if computer_board[i][j] == "hit":
								continue
							elif computer_board[i][j] != "W":
								name = f"Board\\C_W_hit.png"
								
								s = computer_board[i][j][:-2]
								cnt = computer_cnt.get(s) - 1
								computer_cnt.update({s:cnt})
								if cnt == 0:
									ship_scoreboard_c[ships.index(s)] = pygame.transform.scale(pygame.image.load(get_file(f'Scoreboard\\{s}_C_hit.png')), (w * 0.1, h * 0.1))
									computer_sunk_cnt += 1
									pygame.mixer.Sound.play(pygame.mixer.Sound(get_file('Sound\\sunk.wav')))
									coins += sizes.get(s)
									coins_surface = font.render(str(coins), False, (239, 204, 0))
									screen.blit(coins_surface, coin_surface_point)
								else:
									pygame.mixer.Sound.play(pygame.mixer.Sound(get_file('Sound\\hit.wav')))
							else:
								pygame.mixer.Sound.play(pygame.mixer.Sound(get_file('Sound\\miss.wav')))	

							new_img = pygame.image.load(get_file(name)).convert_alpha()
					
							computer_visuals[i][j].update(new_img)
							computer_visuals[i][j].draw(screen)
							computer_board[i][j] = "hit"

							if computer_sunk_cnt == 5:
								run = False
								coins += coins_win.get(mode)
								coins += remaining_unsunken
								total_coins += coins
								coins_surface = font.render(str(coins), False, (239, 204, 0))
								total_coins_surface = font.render(str(total_coins), False, (239, 204, 0))
								# screen.blit(coins_surface, coin_surface_point)
								endgame("player", total_coins)
							
							is_player_turn = False
			else:
				random.seed()
				pygame.time.wait(random.randint(500, 1000))
				# choose i and j / row and col
				
				i = random.randint(1, 10)
				j = random.randint(1, 10)
				name = f"Board\\missed_W.png"
				
				if mode == "hard" and not hitting and len(targets_hard_mode) != 0:
					(i, j) = targets_hard_mode.pop(0)
					while i in range(1, 11) and j in range(1, 11) and player_board[i][j] == "hit":
						if (direction == "left" or direction == "right"):
							if (i - 1, j) not in tiles:
								tiles.append((i - 1, j))
								directions.append("up")
							if (i + 1, j) not in tiles:
								tiles.append((i + 1, j))
								directions.append("down")
						elif (direction == "up" or direction == "down"):
							if (i, j - 1) not in tiles:
								tiles.append((i, j - 1))
								directions.append("left")
							if (i, j + 1) not in tiles:
								tiles.append((i, j + 1))
								directions.append("right")
						
						(i, j) = tiles.pop(0)
						direction = directions.pop(0)
				elif mode == "easy" or not hitting:
					while player_board[i][j].startswith("hit"):
						i = random.randint(1, 10)
						j = random.randint(1, 10)
				elif hitting:
					(i, j) = tiles.pop(0)
					direction = directions.pop(0)
					while i not in range(1, 11) or j not in range(1, 11) or player_board[i][j][-1] == "W":
						if direction == "left" and j != 11:
							tiles.insert(0, (i, j + 1))
							directions.insert(0, "right")
						elif direction == "up" and i != 11:
							tiles.insert(0, (i + 1, j))
							directions.insert(0, "down")
						elif direction == "right" and j != 1:
							tiles.insert(0, (i, j - 1))
							directions.insert(0, "left")
						elif direction == "down" and i != 1:
							tiles.insert(0, (i - 1, j))
							directions.insert(0, "up")
						
						if i in range(1, 11) and j in range(1, 11) and player_board[i][j] == "W":
							break
						
						(i, j) = tiles.pop(0)
						direction = directions.pop(0)

					print(i,j)
					print(player_board[i][j])

					while i in range(1, 11) and j in range(1, 11)  and player_board[i][j] == "hit":
						if  (direction == "left" or direction == "right"):
							if (i - 1, j) not in tiles:
								tiles.append((i - 1, j))
								directions.append("up")
							if (i + 1, j) not in tiles:
								tiles.append((i + 1, j))
								directions.append("down")
						elif (direction == "up" or direction == "down"):
							if (i, j - 1) not in tiles:
								tiles.append((i, j - 1))
								directions.append("left")
							if (i, j + 1) not in tiles:
								tiles.append((i, j + 1))
								directions.append("right")
						
						(i, j) = tiles.pop(0)
						direction = directions.pop(0)
					
					print(i,j)
					print(player_board[i][j])

				
				if  player_board[i][j][-1] != "W":
					
					if not hitting and mode != "easy":
						hitting = True
						tiles.insert(0, (i,j - 1))
						directions.insert(0, "left")
					elif hitting and mode != "easy":
						if direction == "left":
							tiles.insert(0, (i, j - 1))
						elif direction == "up":
							tiles.insert(0, (i - 1, j))
						elif direction == "right":
							tiles.insert(0, (i, j + 1))
						elif direction == "down":
							tiles.insert(0, (i + 1, j))

						directions.insert(0, direction)

					name = f"Board\\C_W_hit.png"
					print(">>>>>>>>>>>", i,j)
					print(player_board[i][j])
					s = player_board[i][j][:-2]
					cnt = player_cnt.get(s) - 1
					player_cnt.update({s:cnt})
					player_board[i][j] = "hit"
					pygame.mixer.Sound.play(pygame.mixer.Sound(get_file('Sound\\hit.wav')))
					if cnt == 0:
						ship_scoreboard_p[ships.index(s)] = pygame.transform.scale(pygame.image.load(get_file(f'Scoreboard\\{s}_P_hit.png')), (w * 0.1, h * 0.1))
						player_sunk_cnt += 1
						remaining_unsunken -= 1
						hitting = False
						tiles.clear()
						directions.clear()
				else:
					player_board[i][j] = "hit_W"
					pygame.mixer.Sound.play(pygame.mixer.Sound(get_file('Sound\\miss.wav')))

				new_img = pygame.image.load(get_file(name)).convert_alpha()
					
				player_visuals[i][j].update(new_img)
				player_visuals[i][j].draw(screen)
				if player_sunk_cnt == 5:
					run = False
					coins = coins_lose.get(mode)
					total_coins += coins
					if total_coins < 0:
						total_coins = 0
					coins_surface = font.render(str(coins), False, (239, 204, 0))
					total_coins_surface = font.render(str(total_coins), False, (239, 204, 0))
					# screen.blit(coins_surface, coin_surface_point)
					endgame("computer", total_coins)
				is_player_turn = True
	



		if quit_btn.draw(screen):
			run = False
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
			

		if (quit_btn.hover(screen)):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
	
		pygame.display.flip()
		pygame.display.update()
	# pygame.quit()

def endgame(winner, coins):
	connection=connector.connect(host="localhost", user="root")
	c = connection.cursor()
	c.execute("use battleship;")
	c.execute(f"select player.VICTORIES, player.BATTLES from player where player.USERNAME = '{user}'")
	result = c.fetchone()
	battles = result[1] + 1
	victories = result[0]
	if winner == "player":
		victories += 1
	
	c.execute(f"UPDATE player SET COINS = '{coins}', BATTLES = '{battles}', VICTORIES = '{victories}' WHERE player.USERNAME = '{user}';")
	connection.commit()
	connection.close()
	
	pygame.mixer.music.set_volume(0)
	pygame.mixer.Sound.play(pygame.mixer.Sound(get_file(f'Sound\\{winner}.mp3')))
	run = True
	while run:
		victory = pygame.transform.scale(pygame.image.load(get_file(f'Panel\\game-over-{winner}.png')), (h * 0.8, h * 0.8))
		screen.blit(bg, (0, 0))
		screen.blit(logo, logo_point)
		screen.blit(coin, coin_point)
		screen.blit(chest, chest_point)
		screen.blit(coins_surface, coin_surface_point)
		screen.blit(total_coins_surface, total_coin_surface_point)
		screen.blit(victory,  (w / 2 - victory.get_width()/2, logo_h))


		for i in range(5):
			screen.blit(ship_scoreboard_p[i], (w * i * 0.2, h * 0.9))
			screen.blit(ship_scoreboard_c[i], (w * i * 0.2 + ship_scoreboard_p[i].get_width(), h * 0.9))
		
		if quit_btn.draw(screen):
			run = False
			
			# pygame.quit()

		if (quit_btn.hover(screen)):
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
		else:
			pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
			
		clock.tick(100)
		for event in pygame.event.get():		
		
			if event.type == pygame.QUIT:
				run = False
			
				

	
		pygame.display.flip()
		pygame.display.update()

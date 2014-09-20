#!/usr/bin/env python3
import pygame
import random

BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
RED = [232, 42, 42]

SCREEN_WIDTH=800
SCREEN_HEIGHT=600


#`````````````````````````````````````````GHOST PLAYER````````````````````````````````````
class Player(pygame.sprite.Sprite):
	
	#Set speed vector of player
	change_x=0
	change_y=0
	
	#List of sprites we can bump against
	level=None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("ghost.png").convert()
		self.image.set_colorkey(BLACK)
		self.image=pygame.transform.scale(self.image,[62,62])
		self.rect = self.image.get_rect()
	
	def update(self):
		self.rect.x += self.change_x
		
		self.rect.y += self.change_y
		
	def go_left(self):
		self.change_x=-5
	def go_right(self):
		self.change_x = 5
	def go_up(self):
		self.change_y = -5
	def go_down(self):
		self.change_y = 5
	def stop(self):
		self.change_x=0
		self.change_y=0
		
		
#`````````````````````````````````````````BULLETS````````````````````````````````````
class Bullet(pygame.sprite.Sprite):

	change_x = 0

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([20,5])
		self.image.fill(RED)
		self.rect=self.image.get_rect()
		
	def update(self):
		self.rect.x += self.change_x
	def shoot_right(self):
		self.change_x = 6
	def shoot_left(self):
		self.change_x = -6

#`````````````````````````````````````````ENEMY DUDE````````````````````````````````````
class Enemy(pygame.sprite.Sprite):

	change_x=0
	change_y=0
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("ghost2left.png").convert()
		self.image.set_colorkey(BLACK)
		self.image=pygame.transform.scale(self.image,[62,62])
		self.rect = self.image.get_rect()
		
	def update(self):
		self.rect.x += self.change_x
		self.rect.y += self.change_y



#`````````````````````````````````````````MAIN APPLICATION````````````````````````````````````
			
def main():
	pygame.init()

	myfont = pygame.font.SysFont("monospace", 20)
	#lazertext = myfont.render("lazer noise",1, WHITE)
	wintext = myfont.render("Oh...",1, WHITE)
	deadtext = myfont.render("I guess you died.",1, WHITE)
	restarttext = myfont.render("Press 'r' to try again.",1, WHITE)
	quittext = myfont.render("Press 'q' to quit.",1, WHITE)
	
	
	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("Ghost Fight")
	background=pygame.image.load("darknight.png").convert()
	background=pygame.transform.scale(background,[800,600])
	

	
	player_list = pygame.sprite.Group()
	bullet_list = pygame.sprite.Group()
	player = Player()
	player.rect.x=0
	player.rect.y = (SCREEN_HEIGHT/2) - player.rect.height
	player_list.add(player)
	enemy_list = pygame.sprite.Group()
	
	for i in range(40):
		enemy = Enemy()
		enemy.rect.x=random.randrange(800, 1000)
		enemy.rect.y=random.randrange(600)
		enemy_list.add(enemy)
	
	dead=False 
	facing_right=True
	score = 0
	
	clock=pygame.time.Clock()

	done=False

	while not done:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				done=True
		
			if event.type == pygame.KEYDOWN:
				if event.key  == pygame.K_LEFT:
					player.go_left()
					player.image=pygame.image.load("ghostleft.png").convert()
					player.image.set_colorkey(BLACK)
					facing_right = False
				elif event.key == pygame.K_RIGHT:
					player.go_right()
					player.image=pygame.image.load("ghost.png").convert()
					player.image.set_colorkey(BLACK)
					facing_right = True
				elif event.key == pygame.K_UP:
					player.go_up()
				elif event.key == pygame.K_DOWN:
					player.go_down()
				elif event.key == pygame.K_SPACE and facing_right == True and dead == False:
					bullet = Bullet()
					bullet.rect.x=player.rect.x+50
					bullet.rect.y=player.rect.y+16
					bullet.shoot_right()
					bullet_list.add(bullet)
				elif event.key == pygame.K_SPACE and facing_right == False and dead == False:
					bullet = Bullet()
					bullet.rect.x=player.rect.x+0
					bullet.rect.y=player.rect.y+16
					bullet.shoot_left()
					bullet_list.add(bullet)
					
					
			if event.type == pygame.KEYUP:
				if event.key  == pygame.K_LEFT and player.change_x <0:
					player.stop()
				elif event.key == pygame.K_RIGHT and player.change_x >0:
					player.stop()
				elif event.key == pygame.K_UP and player.change_y <0:
					player.stop()
				elif event.key == pygame.K_DOWN and player.change_y >0:
					player.stop()
				
			
		if player.rect.right>SCREEN_WIDTH:
			player.rect.right=SCREEN_WIDTH
		if player.rect.left<0:
			player.rect.left=0
		if player.rect.bottom>SCREEN_HEIGHT:
			player.rect.bottom=SCREEN_HEIGHT
		if player.rect.top<0:
			player.rect.top=0
			
		for enemy in enemy_list:
			if pygame.sprite.spritecollide(enemy, player_list, True):
				dead = True

		for enemy in enemy_list:
			enemy_speed = random.randrange(0,3)
			if enemy.rect.x > player.rect.x:
				enemy.rect.x = enemy.rect.x-enemy_speed
				#enemy.image=pygame.image.load("/Users/connormcbride/Documents/Firstprogram/ghost2left.png").convert()
				enemy.image.set_colorkey(BLACK)
			if enemy.rect.x < player.rect.x:
				enemy.rect.x = enemy.rect.x+enemy_speed
				#enemy.image=pygame.image.load("/Users/connormcbride/Documents/Firstprogram/ghost2.png").convert()
				enemy.image.set_colorkey(BLACK)
			if enemy.rect.y > player.rect.y:
				enemy.rect.y = enemy.rect.y-enemy_speed
			if enemy.rect.y < player.rect.y:
				enemy.rect.y = enemy.rect.y+enemy_speed
		
		scoretext = myfont.render("Score: " + str(score),1, WHITE)
		
		for bullet in bullet_list:
			dead_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
			#enemy_list.remove(enemy)
			for enemy in dead_list:
				score += 1
				bullet_list.remove(bullet)
				enemy = Enemy()
				enemy.rect.x=random.randrange(800, 1000)
				enemy.rect.y=random.randrange(1000)
				enemy_list.add(enemy)
				
				
		screen.blit(background, (0,0))
		player_list.update()
		player_list.draw(screen)
		enemy_list.update()
		enemy_list.draw(screen)
		bullet_list.update()
		bullet_list.draw(screen)
		screen.blit(scoretext, (40, 550))
		
		if dead == True:
			screen.blit(deadtext, (40, 100))
			screen.blit(restarttext, (40, 125))
			screen.blit(quittext, (40, 150))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					main()
				if event.key == pygame.K_q:
					pygame.quit()
		if len(enemy_list) == 0:
			screen.blit(wintext, (40, 100))
			screen.blit(restarttext, (40, 125))
			screen.blit(quittext, (40, 150))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					main()
				if event.key == pygame.K_q:
					pygame.quit()
			
				
		clock.tick(60)
		pygame.display.flip()
				
	pygame.quit ()
	
if __name__ == "__main__":
	main()
	
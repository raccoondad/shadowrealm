#!/usr/bin/env python3
import pygame
import random

BLACK = [  0,   0,   0]
WHITE = [255, 255, 255]
GREY = [80, 80, 87]
RED = [232, 42, 42]

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

#`````````````````````````````````````````GHOST DOG````````````````````````````````````
class Player(pygame.sprite.Sprite):
	
	#Set speed vector of player
	change_x=0
	change_y=0
	
	#List of sprites we can bump against
	level=None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("/Users/connormcbride/Documents/Firstprogram/ghost.png").convert()
		self.image.set_colorkey(BLACK)
		self.image=pygame.transform.scale(self.image,[124,124])
		self.rect = self.image.get_rect()
	
	def update(self):
		self.calc_grav()
		
		self.rect.x += self.change_x
		player_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for player in player_hit_list:
			if self.change_x>0:
				self.rect.right = player.rect.left
			elif self.change_x<0:
				self.rect.left=player.rect.right
				
		self.rect.y += self.change_y
		player_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list, False)
		for player in player_hit_list:
			if self.change_y>0:
				self.rect.bottom = player.rect.top
			elif self.change_y<0:
				self.rect.top = player.rect.bottom
			self.change_y=0
		
		
	def calc_grav(self):
		if self.change_y==0:
			self.change_y=1
		else:
			self.change_y += 0.35
		if self.rect.y >=SCREEN_HEIGHT  - self.rect.height and self.change_y>=0:
			self.change_y=0
			self.rect.y = SCREEN_HEIGHT - self.rect.height
	
	
	def jump(self):
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 2
		if len(platform_hit_list)>0 or self.rect.bottom >= SCREEN_HEIGHT:
			self.change_y = -10
	def go_left(self):
		self.change_x=-6
	def go_right(self):
		self.change_x = 6
	def stop(self):
		self.change_x=0

#`````````````````````````````````````````WIZARDS````````````````````````````````````
class Wizard(pygame.sprite.Sprite):

	wizardspeed_x=0
	wizardspeed_y=0
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.image.load("/Users/connormcbride/Documents/Firstprogram/wizard.png").convert()
		self.image.set_colorkey(BLACK)
		self.image=pygame.transform.scale(self.image,[124,124])
		self.rect=self.image.get_rect()
		self.wizardspeed_x+=20

#`````````````````````````````````````````BULLETS````````````````````````````````````
class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface([10,10])
		self.image.fill(RED)
		self.rect=self.image.get_rect()
	def update(self):
		self.rect.x += 6


#`````````````````````````````````````````PLATFORMS````````````````````````````````````
class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.Surface([width, height])
		self.image.fill(GREY)
		
		self.rect=self.image.get_rect()
		
#`````````````````````````````````````````LEVELS````````````````````````````````````
class Level():
	platform_list = None
	enemy_list = None
	
	world_shift = 0
	
	def __init__(self, player):
		self.platform_list = pygame.sprite.Group()
		self.enemy_list = pygame.sprite.Group()
		self.player = player
	def update (self):
		self.platform_list.update()
		self.enemy_list.update()
	def draw(self, screen):
		screen.fill(BLACK)
		self.platform_list.draw(screen)
		self.enemy_list.draw(screen)
		
	def shift_world(self, shift_x):
		self.world_shift += shift_x
		for platform in self.platform_list:
			platform.rect.x += shift_x
			
			
#`````````````````````````````````````````LEVEL 1````````````````````````````````````
class Level_01(Level):
	def __init__(self, player):
		Level.__init__(self, player)
		self.level_limit = -1000
		
		level = [[210, 70, 500, 500],
				[210, 70, 800, 400],
				[210, 70, 1500, 400],
				[210, 70, 1120, 280],
				[210, 70, 2000, 500],
				]
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player=self.player
			self.platform_list.add(block)
		
		
def main():
	pygame.init()

	screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
	pygame.display.set_caption("I'm Scrolling")
	
	#background_image = pygame.image.load("/Users/connormcbride/Documents/Firstprogram/dungeon.gif").convert()
	#background_image=pygame.transform.scale(background_image,[800,600])
	
	player_list = pygame.sprite.Group()
	bullet_list = pygame.sprite.Group()
	enemy_list = pygame.sprite.Group()
	
	
	wizard = Wizard()
	player = Player()
	level_list=[]
	level_list.append(Level_01(player))
	level_list.append(Level_01(wizard))
	current_level_no=0
	current_level=level_list[current_level_no]
	player.level = current_level
	player.rect.x=340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	wizard.rect.x =1 
	wizard.rect.y=SCREEN_HEIGHT - wizard.rect.height
	player_list.add(player)
	enemy_list.add(wizard)
	

	clock=pygame.time.Clock()

	done=False

	while not done:
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				done=True
			
			if event.type == pygame.KEYDOWN:
				if event.key  == pygame.K_LEFT:
					player.go_left()
				if event.key == pygame.K_RIGHT:
					player.go_right()
				if event.key == pygame.K_UP:
					player.jump()
		
			if event.type == pygame.KEYUP:
				if event.key  == pygame.K_LEFT and player.change_x <0:
					player.stop()
				if event.key == pygame.K_RIGHT and player.change_x >0:
					player.stop()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bullet = Bullet()
					bullet.rect.x=player.rect.x+100
					bullet.rect.y=player.rect.y+32
					player_list.add(bullet)
					bullet_list.add(bullet)
					
		player_list.update()
		current_level.update()
		enemy_list.update()
		
		if player.rect.right >= 500:
			diff = player.rect.right -500
			player.rect.right = 500
			current_level.shift_world(-diff)
		if player.rect.left <= 120:
			diff = 120 - player.rect.left
			player.rect.left = 120
			current_level.shift_world(diff)
		
		for bullet in bullet_list:
			if bullet.rect.y <-10:
				bullet_list.remove(bullet)
				player_list.remove(bullet)
		
		current_level.draw(screen)
		#screen.fill(BLACK)
		#screen.blit(background_image, [0,0])
		player_list.draw(screen)
		enemy_list.draw(screen)
		
		clock.tick(60)
		pygame.display.flip()
				
	pygame.quit ()
if __name__ == "__main__":
	main()

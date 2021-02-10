import pygame, sys
from pygame.locals import *
from pygame import mixer
import random
import time
 
'''install''' 
pygame.init()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
'''Setting up FPS'''
FPS = 60
FramePerSec = pygame.time.Clock()

'''buat tampilan'''
panjang =900
lebar = 470

tampilan = pygame.display.set_mode((panjang, lebar))
pygame.display.set_caption("Galaxy Shooter")
icon = pygame.image.load('Img/player.png')


'''Text'''
text30 = pygame.font.SysFont('Constantia', 30)
text40 = pygame.font.SysFont('Constantia', 40)
text50 = pygame.font.SysFont('comicsans', 45)

pygame.display.set_icon(icon)
'''Music'''
bom_music = pygame.mixer.Sound('music/bom.wav')
bom_music.set_volume(0.05) 

'''Laser music'''
laser_music = pygame.mixer.Sound('music/laser2.wav')
laser_music.set_volume(0.10)

'''Bom Music'''
bom_hit_fx = pygame.mixer.Sound('music/bom.wav')
bom_hit_fx.set_volume(0.05)

'''Bom music'''
bom_hit_music = pygame.mixer.Sound('music/bom.wav')
bom_hit_music.set_volume(0.10) 

# background music
pygame.mixer.music.load("music/music1.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
'''Variabel'''

rows = 1
cols = 1
merah = (255,0,0)
hijau = (0,255,0)
putih = (255,255,255) 
alien_colldown = 1000
last_alien_shoot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()

'''Text'''
def text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	tampilan.blit(img, (x, y))


def text_bos():
	bos_label = text30.render("Bos Enemy", 1, (putih))
	tampilan.blit(bos_label, (10, 10))


'''Player Space Shoter'''
class Pesawat(pygame.sprite.Sprite):
	def __init__(self, x, y, darah):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Img/player.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.health_start = darah
		self.health_remaining = darah
		self.last_shoot = pygame.time.get_ticks()

	def update(self):
		'''Kecepatan bergegerak'''
		kecepatan = 8
		speed = 5 # Ecepatan bergerak ke atas bawah

		'''Colldown'''
		colldown = 500
		COLLDOWN = 80
		roket_player_colldown = 1000
		game_over = 0		

		'''Keys/ Tombol untuk menjalankannya'''
		key = pygame.key.get_pressed()
		if key[pygame.K_a] and self.rect.left > 0:
			self.rect.x -= kecepatan
		if key[pygame.K_d] and self.rect.right < panjang:
			self.rect.x += kecepatan

		if key[pygame.K_w] and self.rect.top > 0:
			self.rect.y -= speed
		if key[pygame.K_s] and self.rect.bottom < lebar:
			self.rect.y += speed
		'''catat waktu saat ini'''
		time_now = pygame.time.get_ticks()

		if  key[pygame.K_SPACE] and time_now - self.last_shoot > colldown:
			laser_music.play()
			peluru = Peluru(self.rect.centerx+100, self.rect.top+30)
			peluru_group.add(peluru)
			self.last_shoot = time_now
		if key[pygame.K_b] and time_now - self.last_shoot > COLLDOWN:
			laser_music.play()
			peluru_laser = Peluru_laser(self.rect.centerx+100, self.rect.top+30)
			peluru_laser_group.add(peluru_laser)
			self.last_shoot = time_now

		if  key[pygame.K_v] and time_now - self.last_shoot > roket_player_colldown:
			laser_music.play()
			roket_player = Roket_Player(self.rect.centerx+100, self.rect.top+30)
			roket_player_group.add(roket_player)
			self.last_shoot = time_now

		'''mask'''
		self.mask = pygame.mask.from_surface(self.image)


		if self.health_remaining == 0:
			bom_hit_music.play()						
			lost = True
			lose()										
'''Musuh class'''
class Musuh(pygame.sprite.Sprite):
	def __init__(self, x, y, health):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Img/bos.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.health_start = health
		self.health_remaining = 1000
		self.move_counter = 7
		self.move_direction = 1
		self.last_alien_shoot = pygame.time.get_ticks()
		self.shoot_alien = pygame.time.get_ticks()
		self.roket_alien = pygame.time.get_ticks()
		self.roket_alien_1 = pygame.time.get_ticks()
		self.power_musuh = pygame.time.get_ticks()
		self.alien_colldown = 500
		self.colldown_musuh = 400
		self.colldown_roket = 2000
		self.colldown_roket_1 = 2000
		self.power_colldown = 2200

	def update(self):
		self.rect.y += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 100:
			self.move_direction *= -1
			self.move_counter *= self.move_direction
		
		time_now = pygame.time.get_ticks()
		waktu = pygame.time.get_ticks()
		waktu_roket_alien = pygame.time.get_ticks()
		waktu_roket_alien_1 = pygame.time.get_ticks()
		waktu_power = pygame.time.get_ticks()

		if time_now - self.last_alien_shoot > self.alien_colldown:
			peluru_musuh = Peluru_Musuh(self.rect.centerx-115, self.rect.top+20)
			peluru_musuh_group.add(peluru_musuh)
			self.last_alien_shoot = time_now

		if waktu- self.shoot_alien > self.colldown_musuh:
			peluru_musuh_1 = Peluru_Musuh_1(self.rect.centerx-115, self.rect.bottom-30)
			peluru_musuh_1_group.add(peluru_musuh_1)
			self.shoot_alien = waktu

		if waktu_roket_alien - self.roket_alien > self.colldown_roket:
			roket_musuh = Roket_Musuh(self.rect.centerx+30, self.rect.top-15)
			roket_musuh_group.add(roket_musuh)
			self.roket_alien = waktu_roket_alien

		if waktu_roket_alien_1 - self.roket_alien_1 > self.colldown_roket_1:
			roket_musuh_1 = Roket_Musuh_1(self.rect.centerx+30, self.rect.bottom+20)
			roket_musuh_1_group.add(roket_musuh_1)
			self.roket_alien_1 = waktu_roket_alien_1

		if waktu_power - self.power_musuh > self.power_colldown:
			power_musuh = Power_Musuh(self.rect.centerx-115, self.rect.top+70)
			power_musuh_group.add(power_musuh)
			self.power_musuh = waktu_power	

		if self.health_remaining == 800:
			self.alien_colldown -= 50
			self.colldown_musuh -= 50
			self.colldown_roket -= 100
			self.colldown_roket_1 -= 100
			self.power_colldown -= 400
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			bom_hit_music.play()
		elif self.health_remaining == 450:
			self.alien_colldown += 80
			self.colldown_musuh += 90
			self.colldown_roket -= 100
			self.colldown_roket_1 -= 100
			self.power_colldown -= 100
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			bom_hit_music.play()
		elif self.health_remaining == 220:
			self.alien_colldown -= 90
			self.colldown_musuh += 90
			self.colldown_roket -= 100
			self.colldown_roket_1 -= 100
			self.power_colldown -= 300
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			bom_hit_music.play()	
		elif self.health_remaining <= 0:			
			bom = Bom(self.rect.centerx, self.rect.centery, 3)
			bom_group.add(bom)
			self.kill()
			win()
			bom_hit_music.play()
'''Peluru player class'''
class Peluru(pygame.sprite.Sprite):
	def __init__(self, x, y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/peluru_player.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.x += 9
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, musuh_group, False):
			self.kill()
			bom_music.play()
			musuh.health_remaining -= 2
			bom = Bom(self.rect.centerx+20, self.rect.centery, 2)
			bom_group.add(bom)

'''laser player class''' 
class Peluru_laser(pygame.sprite.Sprite):
	def __init__(self, x, y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/laser_player.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]


	def update(self):
		self.rect.x += 9
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, musuh_group, False):
			self.kill()
			musuh.health_remaining -= 2
			bom = Bom(self.rect.centerx+30, self.rect.centery, 2)
			bom_group.add(bom)

'''laser player class''' 
class Roket_Player(pygame.sprite.Sprite):
	def __init__(self, x, y,):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/roket_player.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]


	def update(self):
		self.rect.x += 9
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, musuh_group, False):
			self.kill()
			musuh.health_remaining -= 2
			bom = Bom(self.rect.centerx, self.rect.centery, 2)
			bom_group.add(bom)


				

'''Peluru musuh class'''
class Peluru_Musuh(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/peluru_musuh.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.x -= 13
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, ship_group, False):
			self.kill()
			ship.health_remaining -= 2
			bom = Bom(self.rect.centerx, self.rect.centery, 1)
			bom_group.add(bom)
		if ship.health_remaining <= 0:
			if pygame.sprite.spritecollide(self, ship_group, True):
				bom = Bom(self.rect.centerx, self.rect.centery, 3)
				bom_group.add(bom)
				self.kill()

class Peluru_Musuh_1(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/peluru_musuh.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.x -= 13
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, ship_group, False):
			self.kill()
			ship.health_remaining -= 2
			bom = Bom(self.rect.centerx, self.rect.centery, 1)
			bom_group.add(bom)
		if ship.health_remaining <= 0:
			if pygame.sprite.spritecollide(self, ship_group, True):
				bom = Bom(self.rect.centerx, self.rect.centery, 3)
				bom_group.add(bom)
				self.kill()

'''roket musuh class'''
class Roket_Musuh(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/roket_musuh.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.x -= 13
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, ship_group, False):
			self.kill()
			ship.health_remaining -= 2
			bom = Bom(self.rect.centerx-30, self.rect.centery, 2)
			bom_group.add(bom)
		if ship.health_remaining <= 0:
			if pygame.sprite.spritecollide(self, ship_group, True):
				bom = Bom(self.rect.centerx, self.rect.centery, 3)
				bom_group.add(bom)
				self.kill()

class Roket_Musuh_1(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/roket_musuh.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.x -= 13
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, ship_group, False):
			self.kill()
			ship.health_remaining -= 2
			bom = Bom(self.rect.centerx-10, self.rect.centery, 2)
			bom_group.add(bom)
		if ship.health_remaining <= 0:
			if pygame.sprite.spritecollide(self, ship_group, True):
				bom = Bom(self.rect.centerx, self.rect.centery, 3)
				bom_group.add(bom)
				self.kill()

class Power_Musuh(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('PeluruImg/laser_musuh.png')
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]

	def update(self):
		self.rect.x -= 13
		if self.rect.top > lebar:
			self.kill()
		if pygame.sprite.spritecollide(self, ship_group, False):
			self.kill()
			ship.health_remaining -= 2
			bom = Bom(self.rect.centerx-10, self.rect.centery, 2)
			bom_group.add(bom)
		if ship.health_remaining <= 0:
			if pygame.sprite.spritecollide(self, ship_group, True):
				bom = Bom(self.rect.centerx, self.rect.centery, 3)
				bom_group.add(bom)
				self.kill()


'''bom class'''				
class Bom(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1,6):
			img = pygame.image.load(f'BomImg/bom_musuh.png')
			if size == 1:
				img = pygame.transform.scale(img, (20, 20))
			if size == 2:
				img = pygame.transform.scale(img, (40, 40))
			if size == 3:
				img = pygame.transform.scale(img, (160, 160))
			if size == 4:
				img = pygame.transform.scale(img, (200, 200))
			self.images.append(img)

		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x,y]
		self.counter = 0

	def update(self):
		bom_speed = 3
		'''animasi bom'''
		self.counter += 1

		if self.counter >= bom_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		'''Delete bom animasi'''
		if self.index >= len(self.images) - 1 and self.counter >= bom_speed:
			self.kill()
def lose():
	lose_label = text30.render("Game Over", 1, (putih))
	tampilan.blit(lose_label,(350, 250))
def win():
	win_label = text30.render("You Win", 1, (putih))
	tampilan.blit(win_label, (400, 250))



'''	Buat spiret gruop'''
ship_group = pygame.sprite.Group()
peluru_group = pygame.sprite.Group()
musuh_group = pygame.sprite.Group()
peluru_musuh_group = pygame.sprite.Group()
bom_group = pygame.sprite.Group()
peluru_laser_group = pygame.sprite.Group()
peluru_musuh_1_group = pygame.sprite.Group()
roket_musuh_group = pygame.sprite.Group()
roket_musuh_1_group = pygame.sprite.Group()
roket_player_group = pygame.sprite.Group()
power_musuh_group = pygame.sprite.Group()			
'''buat player'''
ship = Pesawat(100,250,150)
ship_group.add(ship)

'''Musuh'''
musuh = Musuh(730,250,1000)
musuh_group.add(musuh)

'''Background bergerak'''                   
class Background():
      def __init__(self):
            self.bgimage = pygame.image.load('Img/background.png')
            self.rectBGimg = self.bgimage.get_rect()
 
            self.bgY1 = 0
            self.bgX1 = 0
 
            self.bgY2 = 0
            self.bgX2 = self.rectBGimg.width
 
            self.movingUpSpeed = 1.5
         
      def update1(self):
        self.bgX1 -= self.movingUpSpeed
        self.bgX2 -= self.movingUpSpeed
        if self.bgX1 <= -self.rectBGimg.width:
            self.bgX1 = self.rectBGimg.width
        if self.bgX2 <= -self.rectBGimg.width:
            self.bgX2 = self.rectBGimg.width
             
      def render(self):
         tampilan.blit(self.bgimage, (self.bgX1, self.bgY1))
         tampilan.blit(self.bgimage, (self.bgX2, self.bgY2))


back_ground = Background()

	
'''Game Looping'''
run = True
while run:          

    
    back_ground.update1()
    back_ground.render()
    
    if countdown == 0:	
	    ship.update()
	    peluru_group.update()
	    musuh_group.update()
	    peluru_musuh_group.update()
	    peluru_musuh_1_group.update()	    
	    roket_musuh_group.update()
	    roket_musuh_1_group.update()
	    roket_player_group.update()
	    power_musuh_group.update()
			   	
    bom_group.update()
    peluru_laser_group.update()
	
    '''menggambar spirite group'''
    ship_group.draw(tampilan)
    peluru_group.draw(tampilan)
    musuh_group.draw(tampilan) 
    peluru_musuh_group.draw(tampilan)
    bom_group.draw(tampilan)
    peluru_laser_group.draw(tampilan)
    peluru_musuh_1_group.draw(tampilan)
    roket_player_group.draw(tampilan)
    roket_musuh_group.draw(tampilan)
    roket_musuh_1_group.draw(tampilan)
    power_musuh_group.draw(tampilan)
    text_bos()
    '''Tombol atau keys '''   
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run = False	
            
    if countdown > 0:
    	text('Ready!!', text40, putih, int(panjang / 2 - 70), int(lebar / 2 + 10))
    	text(str(countdown), text40, putih, int(panjang / 2 - 10), int(lebar / 2 + 50))
    	count_timer = pygame.time.get_ticks()	
    	
    	if count_timer - last_count > 1000:    	
    		countdown -= 1 
    		last_count = count_timer

    pygame.display.update()
    FramePerSec.tick(FPS)
    
pygame.quit()
import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
game_width = 800
game_height = 480
window_size = (game_width, game_height)
game_window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Tappy Plane')

# function for resizing an image
def scale_image(image, new_width):
	image_scale = new_width / image.get_rect().width
	new_height = image.get_rect().height * image_scale
	scaled_size = (new_width, new_height)
	return pygame.transform.scale(image, scaled_size)

# function for displaying the score
def display_score(score):

	# determine how many digits
	num_digits = len(str(score))

	# display every digit in the score
	score_x = int(game_width / 2 - number_images[0].get_width() * num_digits / 2)
	for digit in str(score):
		number_image = number_images[int(digit)]
		game_window.blit(number_image, (score_x, 30))
		score_x += number_image.get_width()

# load background image
bg = pygame.image.load('images/background.png').convert_alpha()
bg_scroll = 0

# load the ground image
ground_image = pygame.image.load('images/groundGrass.png').convert_alpha()
ground_image = scale_image(ground_image, 400)

# load the rock images
rock_up_image = pygame.image.load('images/rockGrass.png').convert_alpha()
rock_down_image = pygame.image.load('images/rockGrassDown.png').convert_alpha()

# load the star image
star_image = pygame.image.load('images/starGold.png').convert_alpha()
star_image = scale_image(star_image, 20)

# load the plane images
plane_images = []
for i in range(1, 4):
	plane_image = pygame.image.load(f'images/planeRed{i}.png').convert_alpha()
	plane_image = scale_image(plane_image, 50)
	plane_images.append(plane_image)

# load the number images
number_images = []
for i in range(10):
	number_image = pygame.image.load(f'images/number{i}.png').convert_alpha()
	number_images.append(number_image)

# load the game over image
gameover_image = pygame.image.load('images/textGameOver.png').convert_alpha()

class Ground(pygame.sprite.Sprite):
	
	def __init__(self, x):

		pygame.sprite.Sprite.__init__(self)

		self.image = ground_image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = game_height - ground_image.get_height()

	def update(self):

		# move left
		self.rect.x -= 2

		# once this object goes off screen on the left side
		# reposition it to the right side
		if self.rect.right <= 0:
			self.rect.x = game_width

class Rock(pygame.sprite.Sprite):
	
	def __init__(self, x, point_direction):

		pygame.sprite.Sprite.__init__(self)

		if point_direction == 'up':
			self.image = rock_up_image
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = game_height - rock_up_image.get_height()
		else:
			self.image = rock_down_image
			self.rect = self.image.get_rect()
			self.rect.x = x
			self.rect.y = 0

		self.point_direction = point_direction

	def update(self):

		self.rect.x -= 2

		# remove rock when it goes off screen and replace it with a new rock
		if self.rect.right <= 0:
			self.kill()

			# find the right most rock
			rock_x = 0
			for rock in rock_group:
				if rock.rect.x > rock_x:
					rock_x = rock.rect.x

			# create a gap after the right most rock
			rock_x += random.randint(200, 400)

			# add the new rock to the group
			rock_group.add(Rock(rock_x, self.point_direction))

			# add a star to the group
			star_x = rock_x + random.randint(-100, 100)
			if self.point_direction == 'up':
				star_y = game_height - rock_up_image.get_height() - random.randint(50, 100)
			else:
				star_y = rock_down_image.get_height() + random.randint(50, 100)
			star_group.add(Star(star_x, star_y))

class Plane(pygame.sprite.Sprite):
	
	def __init__(self):

		pygame.sprite.Sprite.__init__(self)

		self.image_index = 0
		self.image = plane_images[self.image_index]
		self.rect = self.image.get_rect()
		self.rect.x = 50
		self.rect.y = game_height / 2

		self.score = 0

	def update(self):

		self.rect.y += 2

		# update image
		self.image_index += 0.2
		if self.image_index >= len(plane_images):
			self.image_index = 0
		self.image = plane_images[int(self.image_index)]

	def fly_up(self):

		self.rect.y -= 4

class Star(pygame.sprite.Sprite):
	
	def __init__(self, x, y):

		pygame.sprite.Sprite.__init__(self)

		self.image = star_image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self):
		self.rect.x -= 2

		# remove star when it goes off screen
		if self.rect.x <= 0:
			self.kill()

# create the sprite groups
ground_group = pygame.sprite.Group()
rock_group = pygame.sprite.Group()
plane_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()

# add the ground objects
for ground_x in range(0, game_width + 1, ground_image.get_width()):
	ground_group.add(Ground(ground_x))

# add 4 rocks and stars
point_direction = 'up'
rock_x = game_width
for i in range(4):

	star_x = rock_x + random.randint(-100, 100)
	if point_direction == 'up':
		star_y = game_height - rock_up_image.get_height() - random.randint(50, 100)
	else:
		star_y = rock_down_image.get_height() + random.randint(50, 100)
	star_group.add(Star(star_x, star_y))

	rock_group.add(Rock(rock_x, point_direction))

	# randomly generate a gap distance for the next rock
	rock_x += random.randint(200, 400)

	# alternate rock direction
	if point_direction == 'up':
		point_direction = 'down'
	else:
		point_direction = 'up'

# add the plane
plane = Plane()
plane_group.add(plane)

# game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:

	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	# make the plane fly up when left mouse button is clicked or held
	if pygame.mouse.get_pressed()[0]:
		plane.fly_up()

	# draw the background
	game_window.blit(bg, (0 - bg_scroll, 0))
	game_window.blit(bg, (game_width - bg_scroll, 0))
	bg_scroll += 1
	if bg_scroll == game_width:
		bg_scroll = 0

	# move and draw the rock objects
	rock_group.update()
	rock_group.draw(game_window)

	# move and draw the ground objects
	ground_group.update()
	ground_group.draw(game_window)

	# move and draw the stars
	star_group.update()
	star_group.draw(game_window)

	# move and draw the plane
	plane_group.update()
	plane_group.draw(game_window)

	# check for collision with star
	if pygame.sprite.spritecollide(plane, star_group, True, pygame.sprite.collide_mask):
		plane.score += 1

	# display score
	display_score(plane.score)

	# check for collision with rock or ground
	gameover = False
	if pygame.sprite.spritecollide(plane, rock_group, False, pygame.sprite.collide_mask):
		gameover = True
	elif pygame.sprite.spritecollide(plane, ground_group, False, pygame.sprite.collide_mask):
		gameover = True

	# check if game is over
	while gameover:

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
				gameover = False

		gameover_x = game_width / 2 - gameover_image.get_width() / 2
		gameover_y = game_height / 2 - gameover_image.get_height() / 2
		game_window.blit(gameover_image, (gameover_x, gameover_y))
		pygame.display.update()

	pygame.display.update()

pygame.quit()
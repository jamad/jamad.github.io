import pygame, sys, time, asyncio

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 480
FRAMERATE = 60

class Game:
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		pygame.display.set_caption('Flappy Sammy')
		self.clock = pygame.time.Clock()
		self.active = True

		# sprite groups
		self.all_sprites = pygame.sprite.Group()
		self.collision_sprites = pygame.sprite.Group()
		self.particles = pygame.sprite.Group()

		# timer
		self.obstacle_timer = pygame.USEREVENT + 1
		pygame.time.set_timer(self.obstacle_timer,1400)
		
		# text
		self.font = pygame.font.Font(None,30)
		self.score = 0
		self.fps = 0
		self.start_offset = 0

	def display_score(self):
		if self.active:
			self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
			y = WINDOW_HEIGHT / 10
		else:
			y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

		score_surf = self.font.render(str(self.score),True,'grey')
		score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
		self.display_surface.blit(score_surf,score_rect)

	def display_fps(self):
		self.fps = (self.clock.get_fps())
		y = WINDOW_HEIGHT / 60

		fps_surf = self.font.render(str(round(self.fps)),True,'black')
		fps_rect = fps_surf.get_rect(topright = (WINDOW_WIDTH ,y))
		self.display_surface.blit(fps_surf,fps_rect)

	async def run(self):
		
		last_time = time.time()
		while True:
			
			# delta time
			dt = time.time() - last_time
			last_time = time.time()
			
			mycolor='black'
			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.active:
						mycolor='blue'
					
			# game logic
			self.display_surface.fill(mycolor)
			self.all_sprites.update(dt)
			self.all_sprites.draw(self.display_surface)
			self.display_score()
			self.display_fps()

			if not self.active: 
				self.display_surface.blit(self.menu_surf,self.menu_rect)

			pygame.display.update()
			self.clock.tick(FRAMERATE)
			await asyncio.sleep(0)

if __name__ == '__main__':
	game = Game()
	asyncio.run(game.run())
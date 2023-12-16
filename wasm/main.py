import pygame, sys
from pygame.math import Vector2

import asyncio

BLUE = (0,0,32)
DARK_BLUE = (0, 128, 0)
CELL_SIZE = 2
CELL_COUNT = 128
OFFSET = 20
DIRECTION={pygame.K_UP :Vector2(0, -1),pygame.K_DOWN : Vector2(0, 1),pygame.K_LEFT : Vector2(-1, 0),pygame.K_RIGHT: Vector2(1, 0)}

pygame.init()
screen = pygame.display.set_mode( [2*OFFSET + CELL_SIZE*CELL_COUNT]*2)

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 15) 	# the smaller, the faster


async def main():
	init=True
	while True:
		if init:
			bodies=[Vector2(i, 9) for i in range(18,3,-1)]
			dir = Vector2(1,0)
			init=False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(pygame.quit())
			if event.type == SNAKE_UPDATE:
				new_head=bodies[0] + dir
				bodies = [new_head]+bodies[:-1]	
				if 	not -1<new_head.x <= CELL_COUNT or not -1<new_head.y <= CELL_COUNT or	new_head in bodies[1:]:	
					init=True
			if event.type == pygame.KEYDOWN:
				dir =DIRECTION.get(event.key,dir) # default : no change

		#Draw
		screen.fill(BLUE)
		pygame.draw.rect(screen, DARK_BLUE, (OFFSET-5, OFFSET-5, CELL_SIZE*CELL_COUNT+2, CELL_SIZE*CELL_COUNT+2), 5)
		
		for body in bodies:
			body_rect = (OFFSET + body.x * CELL_SIZE, OFFSET+ body.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
			pygame.draw.rect(screen, DARK_BLUE, body_rect, 0, 7)

		title_surface = pygame.font.Font(None, 15).render("Simple Snake", True, DARK_BLUE)

		screen.blit(title_surface, (OFFSET-15, 2))
		pygame.display.update()
		pygame.time.Clock().tick(60)

		await asyncio.sleep(0)

asyncio.run(main())

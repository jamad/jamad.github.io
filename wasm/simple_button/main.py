import asyncio # step1

import pygame
pygame.init() 
w=h=360
screen = pygame.display.set_mode((h,w) ) 
smallfont = pygame.font.SysFont('Corbel',35) 

async def main(): # step2
	flag=True
	while True:  	
		x,y = pygame.mouse.get_pos() 
		hoverover=0 <= x-w/2 <= 140 and 0 <= y-h/2 <= 40
		
		for ev in pygame.event.get(): 
			if (ev.type == pygame.MOUSEBUTTONDOWN and hoverover): 
				flag=not flag
				
		screen.fill((60,25,60)) 
		pygame.draw.rect(screen,((100,100,100) ,(170,170,170) )[hoverover],[w/2,h/2,140,40]) 	
		text = smallfont.render(('A','B')[flag ] , True , (255,255,255) ) 
		screen.blit(text , (w/2+25,h/2)) 
		pygame.display.update() 

		await asyncio.sleep(0) # step3

asyncio.run(main()) # step4
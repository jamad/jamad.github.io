import pygame

pygame.init() 
SCREEN_IPHONE=(360,640)
myscreen = pygame.display.set_mode(SCREEN_IPHONE) 
myfont = pygame.font.SysFont(None,25)   

# Create a player object
player = pygame.Surface((50, 50))
# Set the initial position of the player
player_pos = [175, 175]

player.fill((255, 0, 0))
greencolor=0

def mainloop():
    global player_pos, greencolor
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            player_pos = pygame.mouse.get_pos()# changed for the position to draw
            greencolor= not greencolor

    player.fill((255-255*greencolor,0,255*greencolor))

    myscreen.fill((0, 0, 0))
    myscreen.blit(player, player_pos)
    pygame.display.update()

if __name__=='__main__':
    while 1:mainloop()



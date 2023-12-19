import pygame

pygame.init() 
SCREEN_IPHONE=(360,640)
myscreen = pygame.display.set_mode(SCREEN_IPHONE) 
myfont = pygame.font.SysFont(None,25)   

# Create a player object
player = pygame.Surface((50, 50))
player.fill((255, 0, 0))
# Set the initial position of the player
player_pos = [175, 175]

def mainloop():
    global player_pos
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
            player_pos = event.pos

    myscreen.fill((0, 0, 0))
    myscreen.blit(player, player_pos)
    pygame.display.update()

if __name__=='__main__':
    while 1:mainloop()



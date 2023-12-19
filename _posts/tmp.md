Working With Touch Inputs in PyGame


PyGame’s Touch Support
PyGame has built-in support for working with touch inputs. This includes support for mouse and finger touch inputs.

To detect a mouse, you can use the pygame.MOUSEBUTTONDOWN and pygame.MOUSEBUTTONUP events. For example:

for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        print("Mouse button pressed")
To detect finger touch inputs, you can use the pygame.FINGERDOWN and pygame.FINGERUP events. For example:

for event in pygame.event.get():
    if event.type == pygame.FINGERDOWN:
        print("Finger touched the screen")
Creating a Simple Game
You can find all the code in this GitHub Repo.

Start by creating a simple game. This game will consist of a player character that you can move around the screen using touch inputs. To do this, you will need to create a game loop and a player character.

Before you begin, make sure you have pip installed on your device, then use the following command to install the PyGame module:

pip install pygame
Now, import the PyGame module in your game code:

import pygame
pygame.init()
After that, create the game window and a game object:

# Set up the display
size = (400, 400)
screen = pygame.display.set_mode(size)

# Create a player object
player = pygame.Surface((50, 50))
player.fill((255, 0, 0))

# Set the initial position of the player
player_pos = [175, 175]
Finally, create the game loop:

# The game loop
running = True

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the player position
    player_pos[0] += 5
    player_pos[1] += 5

    # Draw the player
    screen.blit(player, player_pos)

    # Update the display
    pygame.display.update()
Note that the above code only creates a simple game where the player character moves around the screen. To make the game more interesting, you can add physics and collisions to create obstacles for the player to overcome.

Mouse Touch Inputs for Player Movement
Now that you have a game with a player character, you can start adding touch inputs. To do this, you will need to add an event handler for the mouse inputs. Add the pygame.MOUSEBUTTONDOWN and pygame.MOUSEBUTTONUP events to the game loop.

Create an event handler for the mouse inputs. When a player presses the mouse button, update the character’s position to the current mouse position. The program will ignore the release of the mouse button, since it doesn't need to take any action in that case.

# The game loop
running = True

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            player_pos[0] = mouse_x
            player_pos[1] = mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
    
    screen.fill((0, 0, 0))

    # Draw the player
    screen.blit(player, player_pos)

    # Update the display
    pygame.display.update()
You can also add extra logic to the event handler to make the player move in response to the mouse input.

Finger Touch Inputs for Player Movement
In addition to mouse inputs, you can also add finger touch inputs. To do this, you will need to add an event handler for the finger-touch inputs.

Add the pygame.FINGERDOWN and pygame.FINGERUP events to the game loop:

# The game loop
running = True

while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for mouse inputs
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            player_pos[0] = mouse_x
            player_pos[1] = mouse_y
        elif event.type == pygame.MOUSEBUTTONUP:
            pass
        # Check for finger inputs
        elif event.type == pygame.FINGERDOWN:
            finger_x, finger_y = event.pos
            player_pos[0] = finger_x
            player_pos[1] = finger_y
        elif event.type == pygame.FINGERUP:
            pass

    screen.fill((0, 0, 0))
    
    # Draw the player
    screen.blit(player, player_pos)

    # Update the display
    pygame.display.update()
Notice how similar this is to the mouse input event handler. This event handler updates the character’s position when the player presses their finger on the screen. When they release their finger, nothing happens. This allows you to create a game that you can control using both mouse and finger touch inputs. Keep in mind that you can also use other events such as pygame.FINGERMOTION to respond to finger movement.

Pygame’s Additional Touch Features
With the basic touch features in place, you can start adding more advanced features. PyGame has a few built-in features that can help you add more touch features to your game.

The first feature is the pygame.mouse.set_visible() function. This function allows you to hide the mouse cursor. This can be useful if you want to create a game that only uses touch inputs and not the mouse.

Here’s an example of how to use the set_visible() function:

pygame.mouse.set_visible(False)
The pygame.mouse.set_pos() function sets the mouse cursor to a specific position on the screen. This is useful if you want to move the mouse to a specific location without using the mouse inputs.

Below is an example of how to use the set_pos() function:

pygame.mouse.set_pos(200, 200)
You can use the pygame.mouse.get_rel() function to get the relative movement of the mouse. You can use this to detect how far the mouse has moved since the last mouse event.

This is how you can use the get_rel() function:

dx, dy = pygame.mouse.get_rel()
Finally, you can use the pygame.mouse.get_pressed() function to check if the player presses any mouse button. This can be useful when creating games with mouse/touch controls.

Below is an example of how to use the get_pressed() function:

mouse_buttons = pygame.mouse.get_pressed()
PyGame also provides a MOUSEWHEEL event type which you can use to detect mouse wheel scrolls. It supports both vertical and horizontal scrolls.

Here’s an example:

for event in pygame.event.get():
    if event.type == pygame.MOUSEWHEEL:
        if event.y > 0:
            print("Mouse wheel scrolled up")
        elif event.y < 0:
            print("Mouse wheel scrolled down")
Create Interactive Games With Touch Inputs
With the touch inputs in place, you can now create interactive games. For example, you can create a game where the player can move around the screen using touch inputs. You can also create gesture-based games, where the player can perform different gestures to trigger actions in the game.

The possibilities are endless when it comes to creating games with touch inputs. With the help of PyGame, you can create games that are both fun and interactive. So get out there and start creating!

Upgrade Your Tech IQ With Our Free Newsletters
Email Address
By subscribing, you agree to our Privacy Policy and may receive occasional deal communications; you can unsubscribe anytime.

Comments
Share
Share
Share
Share
Share
Copy
Email
Link copied to clipboard
RELATED TOPICS
PROGRAMMING
PROGRAMMING
PYTHON
GAME DEVELOPMENT
ABOUT THE AUTHOR
Imran Alam
(85 Articles Published)
Imran is a writer at MUO with 3 years of experience in writing technical content. He has also worked with many startups as a full-stack developer. He is passionate about writing and helping others learn about technology. In his free time, he enjoys exploring new programming languages.

ARTIFICIAL INTELLIGENCE
WHATSAPP
The Microsoft Copilot logo 1
What Is Microsoft Copilot? How to Use Copilot in Windows
4 days ago
Graphic that reads ChatGPT Alternatives 1
Generative AI APIs and ChatGPT Alternatives for Developers to Consider
6 days ago
microsoft edge copilot logo with santa hat 1
How to Use Microsoft Edge Copilot to Find Better Holiday Shopping Deals
Dec 10, 2023
See More
HOME
PROGRAMMING
Implementing Basic Physics and Collision Detection in Pygame
BY
IMRAN ALAM
PUBLISHED JAN 23, 2023
Save time and avoid errors with Pygame’s built-in collision-handling.

Illustrations representing wireframe diagrams of four website pages
Readers like you help support MUO. When you make a purchase using links on our site, we may earn an affiliate commission. Read More.
Pygame provides several built-in functions for detecting collisions between game objects. These are invaluable because working out exactly when and how moving objects overlap can be a complicated task.

Learn how to add basic physics and collisions in your game using the pygame module.

Pygame’s Built-In Collision Detection Functions
The most basic built-in collision detection function is spritecollide. It takes in a sprite, a group of sprites, and a boolean value indicating whether or not the sprites should "die" (be removed) when they collide. This function returns a list of sprites that have collided. Here is an example of how to use it:

collided_sprites = pygame.sprite.spritecollide(sprite1, sprite_group, True)
Another useful collision detection function is groupcollide, which takes in two groups of sprites and a boolean value as well. This function returns a dictionary with the collided sprites as the keys and the sprites they collided with as the values. Here's an example of how to use it:

collision_dict = pygame.sprite.groupcollide(group1, group2, True, True)
Creating a Basic Platformer Game Using the spritecollide Function
To create a basic platformer game using Pygame, you will need to create a player sprite that the user can control and a platform sprite for the player to stand on. You can use the spritecollide function to detect when the player sprite collides with the platform sprite and prevent the player from falling through the platform.

To start, install the pygame module using pip:

pip install pygame
After that, create simple classes for the Player and Platform, both of which should inherit from Pygame’s Sprite class. The Player class should have an update method to handle the position of the player based on the velocity. Also, it should have a y_velocity variable to apply the gravity effect. The Platform class should have an __init__ method that takes the coordinates of the platform and creates a surface with that size.

Player Class
You can create a Player class using the pygame.sprite.Sprite module. This class will initialize the player with a given x and y coordinates. Then, the update method will update the position of the player by incrementing the y_velocity value.

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.y_velocity = 0

    def update(self):
        self.rect.y += self.y_velocity
Platform Class
The Platform class also uses the pygame.sprite.Sprite module. This class will initialize the platform with given x and y coordinates, as well as a width and height.

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
The Game Loop
The game loop will allow you to create a window with a size of 640x480. Then, it will run a loop that will check for any events, such as a quit command. It will also check for any collisions between the player and the platform. Finally, it will fill the screen with a white color, draw the player and platform, and then flip the display.

player = Player(100, 300)
player_group = pygame.sprite.Group()
player_group.add(player)

platform = Platform(50, 400, 100, 20)
platform_group = pygame.sprite.Group()
platform_group.add(platform)

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    player_group.update()
    collided = pygame.sprite.spritecollide(player, platform_group, False)

    if collided:
        player.y_velocity = 0
    screen.fill((255, 255, 255))
    player_group.draw(screen)
    platform_group.draw(screen)
    pygame.display.flip()

pygame.quit()
Below is the output:

simple platformer game using pygame
Implementing Gravity and Jumping Behavior
To implement gravity and jumping behavior in your platformer game, you will need to add a y velocity to your player sprite and update its y position in each frame. To do this you can use the update method inside the Player class and add the following code snippet:

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.y_velocity = 0

    def update(self):
        self.rect.y += self.y_velocity
        self.y_velocity += GRAVITY # Apply gravity to y velocity
Now every time you call the update method, it will update the player position according to its velocity and gravity.

To make the player sprite jump, you can bind the jumping action to a specific key or button and update the player's y velocity with a negative value. The following code snippet is an example of how to jump when a player presses the spacebar.

JUMP_VELOCITY = -10

# inside the game loop
if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
    player.y_velocity = JUMP_VELOCITY
Note that you will need to check the event.type to make sure that the event is a KEYDOWN event before checking the key value.

Adding Basic Physics Such as Friction and Acceleration
To add basic physics such as friction and acceleration to your platformer game, you will need to update the x velocity of your player sprite in each frame. You can add x velocity to the player class and update it in the same way as y velocity. To implement friction, you can decrease the x velocity of the player sprite by a small amount in each frame. For example, you can add the following code snippet inside the update method of the Player class:

FRICTION = 0.9

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.y_velocity = 0
        self.x_velocity = 0

    def update(self):
        self.rect.y += self.y_velocity
        self.rect.x += self.x_velocity
        self.y_velocity += GRAVITY # Apply gravity to y velocity
        self.x_velocity *= FRICTION # Apply friction to x velocity
To implement acceleration, you can set a variable, player_movement, for the horizontal movement, and update the x velocity of the player sprite according to the player_movement value. You can do this by binding the movement to specific keys or buttons and updating the player's x velocity in the event loop, for example:

ACCELERATION = 0.5
player_movement = 0

if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_LEFT:
        player_movement = -1
    elif event.key == pygame.K_RIGHT:
        player_movement = 1
elif event.type == pygame.KEYUP:
    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
        player_movement = 0
        
player.x_velocity += player_movement * ACCELERATION
By using these techniques, you can create a simple yet fun platformer game using Pygame's built-in collision detection functions and basic physics. With a little bit of creativity and experimentation, you can use these techniques to create a variety of different games and game mechanics.

You can find the complete code in the GitHub repository.

Below is the output:

simple platformer game with gravity and acceleration
Improve User Engagement With Collisions
Many games require some form of collision detection. You can use collisions to create a wide range of game mechanics, from simple platformers to complex physics-based simulations.

Implementing basic physics such as gravity, friction, and acceleration can also greatly improve user engagement, adding realism and a sense of weight to game objects.

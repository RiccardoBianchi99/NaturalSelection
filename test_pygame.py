import sys, pygame
pygame.init()

size = width, height = 1366, 768
speed = [0.5, 0.5]
black = 0, 0, 0

screen = pygame.display.set_mode(size) #create a graphical window. This is a surface object

ball = pygame.image.load("intro_ball.gif") # load the ball image, this is not however an object used by pygame
ballrect = ball.get_rect() # the object rect means that is an object with a rectangle area

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(speed) # i just need to define the speed in this case, not the position of the object
    
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black) #for each frame we erase all the images on the screen by paiting it black
    screen.blit(ball, ballrect) #we can redraw the ball afterwards, it basicallt opied the pixel of the image ball in the location of ballrect
    
    pygame.display.flip() # double buffer that makes sure that the new screen is displaied only when fully prepared
    
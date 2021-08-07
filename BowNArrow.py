import pygame
import random
import time
import threading


#initialize pygame
pygame.init()

#screen vars
WIDTH = 400
HEIGHT = 400

#screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("1 minute bow n arrow")
#font
myfont = pygame.font.SysFont('Comic Sans MS', 30)

#arrow position
bowX = 0
bowY = 0
targetY = 0

SCORE = 0

#load images
arrow = pygame.image.load("arrow.png")
bow = pygame.image.load("bow.png")
targ = pygame.image.load("target.png")
#scale bow
bow = pygame.transform.scale(bow, (75,150))

#array for arrows
arrowXArr = []
arrowYArr = []

running = True
start = True
end = False
thread_need = True
count_loop = True

#starting screen
def begin():
	pygame.font.init()
	screen.fill((0,0,0))
	begin_text = myfont.render('CLICK TO START', True, (255,255,255))
	screen.blit(begin_text, (0,0))

#end game page
def end_pg():
	global end
	end = True
	end_text = myfont.render('GAME OVER', True, (0,0,0))
	screen.blit(end_text, (0, HEIGHT/2))

#timer
def countdown():
	for i in range(60):
		if count_loop:
			time.sleep(1)
	global end
	end = True

#adds arrow into array
def shot(x,y):
	if len(arrowXArr) < 10:
		arrowXArr.append(x)
		arrowYArr.append(y)

#draws arrows moving
def updateArrows():
	for arrows in arrowXArr:
		if arrows < WIDTH:
			screen.blit(arrow, (arrows,arrowYArr[arrowXArr.index(arrows)]))
			arrowXArr[arrowXArr.index(arrows)] = arrows + 1
#remove if past width of pg
	for arrows in arrowXArr:
		if arrows >= WIDTH:
			arrowYArr.pop(arrowXArr.index(arrows))
			arrowXArr.pop(arrowXArr.index(arrows))

#draws bow
def drawbow():
	screen.blit(bow, (bowX, bowY))

#creates random target
def randomTarget():
	randomY = random.randrange(0,HEIGHT,50)
	global targetY 
	targetY= randomY
	target(targetY)

#draws targets and checks if hits
def target(y):
	screen.blit(targ, (WIDTH-50, y))
	for arrows in arrowXArr:
		if arrows > WIDTH-50:
			if y-5 < arrowYArr[arrowXArr.index(arrows)] and y+45>arrowYArr[arrowXArr.index(arrows)]:
				arrowYArr.pop(arrowXArr.index(arrows))
				arrowXArr.pop(arrowXArr.index(arrows))
				global SCORE
				SCORE= SCORE+1
				randomTarget()
#keeps score
def score():
	scoretext = myfont.render(str(SCORE), True, (0,0,0))
	screen.blit(scoretext, (0,0))

#makes thread
t = threading.Thread(target = countdown)

screen.fill((255,255,255))
begin()

#main running loop
while running:

	#checks if exit
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
					if t.is_alive():
						count_loop = False
						t.join()
					running = False
	#checks if started
	if event.type == pygame.MOUSEBUTTONDOWN:
		start = False
		if thread_need:
			try:
				thread_need = False
				t.start()
			except:
				print("Error")

	#checks state
	if start:
		begin()
	elif end:
		end_pg()

	#starts the loop of the game
	else:

		centerY = bowY + 60
		screen.fill((255,255,255))
		drawbow()
		target(targetY)
		score()

		#keyboard check
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				shot(20, centerY)
			if event.key == pygame.K_UP:
				if centerY > -30:
					bowY -= .5
			if event.key == pygame.K_DOWN:
				if centerY < HEIGHT+30:
					bowY += .5

		
		updateArrows()
	pygame.display.update()
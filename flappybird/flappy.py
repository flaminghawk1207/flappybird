import pygame
import random
from pygame.locals import *
import sys

#global variables:
fps=32
screenheight=512
screenwidth=289 #can be 511 also
screen=pygame.display.set_mode((screenwidth,screenheight)) #this is the game screen
groundy=screenheight*0.8
pics={} #sprites
audio={} #sounds
player='pictures/bird.png'
background='pictures/background.png'
pipe='pictures/pipe.png'

def welcomeScreen():
	playerx=int(screenwidth/5)
	playery=int((screenheight -pics['player'].get_height())/2)
	basex=0
	while True:
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type==KEYDOWN and (event.key==K_SPACE):
				return
			else:
				screen.blit(pics['background'],(0,0))
				screen.blit(pics['player'],(playerx,playery))
				screen.blit(pics['base'],(basex,groundy))
				pygame.display.update()
				fpsclock.tick(fps)

def mainGame():
	#for blitting
	score=0
	playerx=int(screenwidth/5)
	playery=int(screenwidth/2)
	basex=0

	pipe1=getRandomPipe() #this will generate pipes with random gaps
	pipe2=getRandomPipe()
	upperPipe=[
	{'x':screenwidth+200,'y':pipe1[0]['y']},{'x':screenwidth+200+(screenwidth/2),'y':pipe2[0]['y']}]
	lowerPipe=[
	{'x':screenwidth+200,'y':pipe1[1]['y']},{'x':screenwidth+200+(screenwidth/2),'y':pipe2[1]['y']}
	]

	pipevelx=-4 #because we are moving the pipes and not the bird
	playervely=-9
	playermaxvely=10
	playerminvely=-8
	playeraccvely=1


	playerflapacc=-8 #when key is pressed
	playerflapped=False #becomes true when player is presseing space


	while True:# game loop
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN and event.key==K_SPACE:
				if playery 	> 0: #meaning player is on the screen
					playervely=playerflapacc
					playerflapped=True
					audio['wing'].play()
		crashtest=isCollide(playerx,playery,upperPipe,lowerPipe) #checks collision
		if crashtest==True:
			return


		#score check
		playerposmid=playerx +pics['player'].get_width()/2
		for pip in upperPipe:
			pipeposmid= pip['x']+pics['pipe'][0].get_width()/2
			if pipeposmid<=playerposmid<pipeposmid +4: #we take 4 becasue we want to create a small band
				score+=1
				print(f"the score is{score}")
				audio['point'].play()

		if playervely<playermaxvely and not playerflapped:
			playervely+=playeraccvely

		if playerflapped is True:
			playerflapped=False #ensuring that he needs to keep pressing

		playerHeight=pics['player'].get_height()
		playery=playery+min(playervely,groundy - playery - playerHeight) #to make sure thaat once player touches the ground he cant get back up as it will hit zero once ground is touched
		#moving pipes to the left
		for upprpipe,lowrpipe in zip(upperPipe,lowerPipe):
			upprpipe['x']+=pipevelx #thats why this is negetive
			lowrpipe['x']+=pipevelx


		#adding pipes after previous pipe has been deleted
		if 0<upperPipe[0]['x']<5: #just a range
			newpipe=getRandomPipe()
			upperPipe.append(newpipe[0])
			lowerPipe.append(newpipe[1])


		if upperPipe[0]['x']< -pics['pipe'][0].get_width(): #when position of pipe is out of the screen
			upperPipe.pop(0)
			lowerPipe.pop(0)


		screen.blit(pics['background'],(0,0))
		for upprpipe,lowrpipe in zip(upperPipe,lowerPipe):
			screen.blit(pics['pipe'][0],(upprpipe['x'],upprpipe['y']))
			screen.blit(pics['pipe'][1],(lowrpipe['x'],lowrpipe['y']))
		screen.blit(pics['base'],(basex,groundy))
		screen.blit(pics['player'],(playerx,playery))

		myDigits=[int(x) for x in list(str(score))]
		width=0
		for digit in myDigits:
			width+=pics['numbers'][digit].get_width()
			Xoffset=(screenwidth- width)/2

			for digit in myDigits:
				screen.blit(pics['numbers'][digit],(Xoffset,screenheight*0.12))
				Xoffset+=pics['numbers'][digit].get_width() #this is for displaying two digits
			pygame.display.update()
			fpsclock.tick(fps)

		






def isCollide(playerx,playery,upperPipe,lowerPipe):
	if playery>groundy -25 or playery<0:    #25 is a random number
		audio['hit'].play()
		return True
	# to check if pipe is getting hit or not:
	for pip in upperPipe:
		pipeheight=pics['pipe'][0].get_height()
		if (playery <pipeheight +pip['y'] and abs(playerx-pip['x']) <pics['pipe'][0].get_width()):
			audio['hit'].play()
			return True

	for pip in lowerPipe:
		if(playery+pics['player'].get_height() >pip['y']) and abs(playerx -pip['x'])<pics['pipe'][1].get_width():
			audio['hit'].play()
			return True


	return False









def getRandomPipe():
	pipeheight=pics['pipe'][0].get_height()
	offset=screenheight/3
	y2=offset + random.randrange(0,int(screenheight-pics['base'].get_height() -0.8*offset))
	pipex=screenwidth+10
	y1=pipeheight -y2 +offset
	piPe=[
	{'x':pipex,'y':-y1},
	{'x':pipex,'y':y2}
	]
	return piPe



if __name__ == '__main__':
	#game starts here
	pygame.init()
	fpsclock=pygame.time.Clock()
	pygame.display.set_caption('Flappy Bird')
	pics['numbers']=(
		pygame.image.load('pictures/0.png').convert_alpha(),pygame.image.load('pictures/1.png').convert_alpha(),
		pygame.image.load('pictures/2.png').convert_alpha(),pygame.image.load('pictures/3.png').convert_alpha(),
		pygame.image.load('pictures/4.png').convert_alpha(),pygame.image.load('pictures/5.png').convert_alpha(),
		pygame.image.load('pictures/6.png').convert_alpha(),pygame.image.load('pictures/7.png').convert_alpha(),
		pygame.image.load('pictures/8.png').convert_alpha(),pygame.image.load('pictures/9.png').convert_alpha())
	pics['base']=pygame.image.load('pictures/base.png').convert_alpha()
	pics['pipe']=(
		pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),pygame.image.load(pipe).convert_alpha())

	audio['die']=pygame.mixer.Sound('audio/die.wav')
	audio['hit']=pygame.mixer.Sound('audio/hit.wav')
	audio['point']=pygame.mixer.Sound('audio/point.wav')
	audio['swoosh']=pygame.mixer.Sound('audio/swoosh.wav')
	audio['wing']=pygame.mixer.Sound('audio/wing.wav')

	pics['background']=pygame.image.load(background).convert_alpha()
	pics['player']=pygame.image.load(player).convert_alpha()
	while True:
		welcomeScreen()
		mainGame()














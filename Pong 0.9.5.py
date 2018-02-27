import sys, pygame, time, os; from random import random, randrange
from pygame.locals import *; pygame.init(); pygame.mixer.init()

size = width, height = 800, 600 # the optimized window size for this game is 800 by 600
black_color = (0, 0, 0); white_color = (255,255,255) #white_color = (0, 0, 0); black_color = (255,255,255) #inverted colors
screen = pygame.display.set_mode(size) # for fullscreen: screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Pong")
clock = pygame.time.Clock(); data_dir = os.getcwd(); #gets current directory
media_dr = data_dir + "/media/"
wallhit= pygame.mixer.Sound(media_dr + "wall_hit.ogg");
paddlehit= pygame.mixer.Sound(media_dr + "paddle_hit.ogg")
point= pygame.mixer.Sound(media_dr + "point.ogg");
menuchange = pygame.mixer.Sound(media_dr + "menuchange.ogg")
entergamemode = pygame.mixer.Sound(media_dr + "entergamemode.ogg")
																													 #________________________________________________
incomingballspeed = False; upperlimit = 7; lowerlimit = 7; scorelimit = originalscorelimit = 10   	    	  # <- Settings when the game launches:
paddlewidth = 11; paddleheight = 70; ballwidth = 10; ballheight = 10; def_fps=framerate = 60	    	  	        #________________________________________________
difficultychoice = 2; modechoice = 1; timechoicemade = 0; mouseclick = False; finishgame = False
changescore = True; ballreset = False; issound_on=True; isfullscreen_on=False; ispause_on=False;
timeoflastsoundtoggle = pygame.time.get_ticks();timeoflastscreentoggle = pygame.time.get_ticks();
timebetweencollisions = 500; timeoflastsound = 0; timebetweenwallhits = 0; timeoflastpausetoggle = pygame.time.get_ticks();



class rect_object:
	def __init__(self, r_width = 30, r_height = 30, color = white_color):
		self.width = r_width; self.height = r_height; rect_object.generate(self, False, color)
	def generate(self, regenerate = False, color = white_color): # generates the surface and rect of the paddle
		self.surface = pygame.Surface((self.width, self.height)); self.surface.fill(color)
		if regenerate == False:
			self.rect = pygame.Rect(width/2 - self.width/2, height/2 - self.height/2, self.width, self.height)
		else: # regenerating is used when the any dimesion of the object is changed
			self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)
	def blit(self):
		screen.blit(self.surface, self.rect)
	def move(self, delt_x, delt_y):
		self.rect = self.rect.move(delt_x, delt_y)

paddle1 = rect_object(paddlewidth, paddleheight); paddle1.rect.x = paddlewidth; paddle1.rect.y = height/2 - paddleheight/2
paddle2 = rect_object(paddlewidth, paddleheight); paddle2.rect.x = width-paddlewidth*2; paddle2.rect.y = height/2 - paddleheight/2
ball = rect_object(ballwidth, ballheight); defaultballrect = ball.rect

nbnets = 40; netrects_ypos = [] # this creates nbnets nets and displays them correctly according to the screen's size
netwidth, netheight = 2, 2*(height)/(3*nbnets+1); spacebetweennets = netheight/2  #calculates the height of nets for the number and the space given
net = rect_object(netwidth, netheight); net.surface.set_alpha(105)
for i in range(nbnets):  #creates nbnets net rectangles and appends them to the list of nets
	net.rect.x = width/2-netwidth/2; net.rect.y = spacebetweennets+i*(spacebetweennets+netheight)
	netrects_ypos.append(net.rect.y)


class text:
	def __init__(self, text, font, fontsize):
		self.text = text; self.font = font; self.fontsize = fontsize; self.xpos = 0; self.ypos = 0;
		self.textfont = pygame.font.SysFont(font, fontsize)

	def size(self): #used to accurately display position
		return (self.textfont).size(self.text)
	def render(self, color=white_color):
		return (self.textfont).render(self.text, True, color)
	def blit(self, color=white_color):
		screen.blit(self.render(color), (self.xpos, self.ypos))
	def right(self): return (self.xpos+self.size()[0])
	def bottom(self): return (self.ypos+self.size()[1])
	def outline(self): #highlights the chosen text surface
		outline = rect_object(self.size()[0], self.size()[1], (142,142,142))
		outline.rect.x = self.xpos; outline.rect.y = self.ypos; outline.blit()
		
#creates the title, subtitle, author and score and comment surfaces and generates their position
title = text("PONG", "PressStart2P", 95); subtitle = text("Press enter/space or click to continue", "PressStart2P", 13)
title.xpos = (width - title.size()[0])/2 ; title.ypos = height/8
subtitle.xpos = (width-subtitle.size()[0])/2 ; subtitle.ypos = 0.71 * height
authornote = text("A hardcore clone of the original game, created by Karl Hayek;\nhardware designed by Tarek Tohme", "PressStart2P", 8)
authornote.xpos = (width-authornote.size()[0])/2; authornote.ypos = (title.ypos+title.size()[1])+0.01*height
score1 = text("0", "pxlvetica", 45); score2 = text("0", "pxlvetica", 45)
score1.xpos = ((width - score1.size()[0])/2) - round(width/7); score1.ypos = height/8
score2.xpos = ((width - score2.size()[0])/2) + round(width/7); score2.ypos = height/8
comment = text("Press enter/space or click to continue", "PressStart2P", 12)
comment.xpos = (width - comment.size()[0])/2; comment.ypos = 0.95*height

#creates the different difficulty and mode surfaces and generates their position
diff0 = text("DIFFICULTY LEVEL: ", "PressStart2P",14); diff0.xpos = (width - diff0.size()[0])/2 + width/45; diff0.ypos = 0.4*height
diff1 = text("Intermediate", "PressStart2P",14); diff1.xpos = 1.2 * diff0.xpos; diff1.ypos = diff0.ypos + 0.05*height
diff2 = text("Hard", "PressStart2P",14); diff2.xpos = 1.2 * diff0.xpos; diff2.ypos = diff1.ypos + 0.05*height
diff3 = text("Expert", "PressStart2P",14); diff3.xpos = 1.2 * diff0.xpos; diff3.ypos = diff2.ypos + 0.05*height

mode0 = text("PLAYER MODE: ", "PressStart2P", 14); mode0.xpos = diff0.xpos; mode0.ypos = 0.67*height
mode1 = text("1 Player", "PressStart2P", 14); mode1.xpos = 1.2 * mode0.xpos; mode1.ypos = mode0.ypos + 0.05*height
mode2 = text("2 Players", "PressStart2P", 14); mode2.xpos = 1.2 * mode0.xpos; mode2.ypos = mode1.ypos + 0.05*height
difflist = [diff0, diff1, diff2, diff3]; modelist = [mode0, mode1, mode2]
	
#creates the text surfaces that explain the controls for the different game modes
mode1player = text("LEFT PADDLE: W/S, K/M, UP/DOWN or mouse", "PressStart2P", 11)
mode1player.xpos = (width - mode1player.size()[0])/2; mode1player.ypos = modelist[len(modelist)-1].bottom() + height*0.04
mode2player = text("LEFT PADDLE: W/S or mouse ; RIGHT PADDLE: K/M or UP/DOWN", "PressStart2P", 11)
mode2player.xpos = (width - mode2player.size()[0])/2; mode2player.ypos = modelist[len(modelist)-1].bottom() + height*0.04
gameexplanation = text("The first player to reach "+str(scorelimit)+" points wins!", "PressStart2P", 14)
gameexplanation.xpos = (width - gameexplanation.size()[0])/2; gameexplanation.ypos = mode1player.ypos+height*0.058
toggles = text("(Press F to toggle fullscreen; Press U to toggle sound)", "PressStart2P", 9)
toggles.xpos = (width - toggles.size()[0])/2; toggles.ypos = (title.ypos - toggles.size()[1])/2

#creates the text that is displayed when the score limit is reached
gameover_win = text("WIN!", "PressStart2P", 52)
gameover_win.xpos = (width/4) - (gameover_win.size()[0])/2; gameover_win.ypos = (height - gameover_win.size()[1])/2 - paddleheight/8
gameover_lose = text("LOSE", "PressStart2P", 38)
gameover_lose.xpos = (width/4) - (gameover_lose.size()[0])/2; gameover_lose.ypos = (height - gameover_lose.size()[1])/2 - paddleheight/8
gameover_comment = text("PRESS ENTER/SPACE TO PLAY AGAIN, ESC TO LEAVE", "PressStart2P", 11)
gameover_comment.xpos = (width/2) - (gameover_comment.size()[0])/2; gameover_comment.ypos = (height - gameover_comment.size()[1])/2 + gameover_win.size()[1]+height/5

def introsettings():
	global ballpositionwait, timeballout, introballspeed, intropaddlespeed, yballdirection, introycollisionfactor, randpaddlemovefactor, maxdistpaddleball
	ballpositionwait = False
	timeballout = pygame.time.get_ticks()
	yballdirection = (round(random(),2)+0.8) * (randrange(-1,2,2))
	introballspeed = [-5, yballdirection]; intropaddlespeed = 4
	introycollisionfactor = 3.4; randpaddlemovefactor = 0.5; maxdistpaddleball = 10
						#_______________________________________________________________________________
						#  Settings for the intro/settings and beginner/intermediate/expert game modes
						#_______________________________________________________________________________
def difficultychanges(difficulty):
	global timeballout, ballpositionwait, paddle1, paddle2, paddlewidth, paddleheight, ballspeed, yballdirection, paddlespeed, computerpaddlespeed, randpaddlemovefactor, maxdistpaddleball, ycollisionfactor, black_color, white_color
	ballpositionwait = True
	timeballout = pygame.time.get_ticks()
	yballdirection = (round(random(),2)+2) * (randrange(-1,2,2))
	ball.rect = defaultballrect
	if difficulty == "intermediate" or difficulty == 1: #for beginners
		paddlewidth = 11; paddleheight = 77
		ballspeed = [-8,yballdirection]
		paddlespeed=[0,6]; computerpaddlespeed = 4
		randpaddlemovefactor = 0.45; maxdistpaddleball = 9; ycollisionfactor=8.7
	elif difficulty == "hard" or difficulty == 2:
		paddlewidth = 11; paddleheight = 70
		ballspeed = [-13.5,yballdirection]
		paddlespeed=[0,9]; computerpaddlespeed = 9
		randpaddlemovefactor = 0.85; maxdistpaddleball = 12; ycollisionfactor=13
	elif difficulty == "expert" or difficulty == 3:
		paddlewidth = 11; paddleheight = 63
		ballspeed = [-14.5,yballdirection]
		paddlespeed=[0,11.55]; computerpaddlespeed = 11.55
		randpaddlemovefactor = 0.7; maxdistpaddleball = 12; ycollisionfactor=14.8
	paddle1 = rect_object(paddlewidth, paddleheight); paddle1.rect.x = paddlewidth; paddle1.rect.y = height/2 - paddleheight/2
	paddle2 = rect_object(paddlewidth, paddleheight); paddle2.rect.x = width-paddlewidth*2; paddle2.rect.y = height/2 - paddleheight/2


def changechoice_keys(choice, choicelowerlimit, choiceupperlimit): #changes the user's choice according to his key input
	global timechoicemade, pressedkey
	timebetweenchoices = pygame.time.get_ticks()
	if (pressedkey[K_k] or pressedkey[K_w] or pressedkey[K_UP]) and choice-1 >= choicelowerlimit and timebetweenchoices - timechoicemade > 150:
		collisionsound("menuchange"); choice = choice - 1; timechoicemade = pygame.time.get_ticks()
	if (pressedkey[K_m] or pressedkey[K_s] or pressedkey[K_DOWN]) and choice+1 <= choiceupperlimit and timebetweenchoices - timechoicemade > 150:
		collisionsound("menuchange"); choice = choice + 1; timechoicemade = pygame.time.get_ticks()
	return(choice)
	
def changechoice_mouse(choice, choicelist): #changes the user's choice and highlights it according to the mouse's position
	global mousex, mousey
	for i in range (1,len(choicelist)):
		if choicelist[i].xpos <= mousex <= choicelist[i].right() and choicelist[i].ypos <= mousey <= choicelist[i].bottom():
			if choice != i: collisionsound("menuchange")
			return (i)
	return choice

def collisionangle(paddlerect): # determines the y-direction of the ball after it hits a paddle
	global ycollisionfactor
	if gamemode == "intro" or gamemode == "settings": ycollisionfactor = introycollisionfactor
	collisionangle = 2*(ball.rect.centery - paddlerect.centery)/(paddlerect.bottom-paddlerect.top) # generates the collsion angle (between -1 and 1)
	if 0<=collisionangle<0.3:
		collisionangle = collisionangle + ((random()/5 +0.9)*0.3)-collisionangle
	elif -0.3<collisionangle<=0:
		collisionangle = collisionangle - ((random()/5 +0.9)*0.3)-collisionangle
	elif collisionangle > 1: collisionangle = 1
	elif collisionangle < - 1: collisionangle = -1
	ballspeed[1] = collisionangle*ycollisionfactor
	

def collisionsound(collisiontype): # plays sounds according to the type of contact
	global timeoflastsound, issound_on # this variable prevents multiple sounds from being played at the same time
	if issound_on:
		if (gamemode != "intro" and gamemode != "settings"): # if the game mode is intro, no sounds are played
			if collisiontype == "point": point.play()
			elif collisiontype == "paddlehit": paddlehit.play()
		
			if collisiontype == "wallhit":
				if pygame.time.get_ticks() - timeoflastsound > 20: wallhit.play()
			
		if pygame.time.get_ticks() - timeoflastsound > 25:
			if collisiontype == "entergamemode":
				entergamemode.play()
			elif collisiontype == "menuchange":
				menuchange.play()
	timeoflastsound = pygame.time.get_ticks()



##_______________________________________________________________________Game Engine______________________________________________________________________________##
gamemode = "intro"; introsettings()
while True:
	clock.tick(framerate)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == MOUSEMOTION:# and (gamemode == "normal" or gamemode == "twoplayers"):
			mousex, mousey = event.pos #mouse commands
			if gamemode == "normal" or gamemode == "twoplayers":
				if mousey-paddle1.rect.height/2 < upperlimit: paddle1.rect.centery = upperlimit + paddleheight/2
				elif mousey+paddle1.rect.height/2 > height-lowerlimit: paddle1.rect.centery = (height-lowerlimit) - paddleheight/2
				else: paddle1.rect.centery = mousey

		if event.type == MOUSEBUTTONDOWN: mouseclick = True
		else: mouseclick = False
		
	keys = pygame.key.get_pressed();
	if keys[K_u] and pygame.time.get_ticks() - timeoflastsoundtoggle > 500: #sound toggle controls
		if  issound_on: issound_on = False; timeoflastsoundtoggle = pygame.time.get_ticks()
		else: issound_on = True; timeoflastsoundtoggle = pygame.time.get_ticks()
		
	if keys[K_f] and pygame.time.get_ticks() - timeoflastscreentoggle > 1000: #fullscreen toggle controls
		if not isfullscreen_on:
			screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
			isfullscreen_on = True; timeoflastscreentoggle = pygame.time.get_ticks()			
		else:
			screen = pygame.display.set_mode(size)
			isfullscreen_on = False; timeoflastscreentoggle = pygame.time.get_ticks()

	if keys[K_p] and pygame.time.get_ticks() - timeoflastpausetoggle > 500: #pausetoggle controls
		if not ispause_on:
			ispause_on = True; framerate = 20; timeoflastpausetoggle = pygame.time.get_ticks();
		else:
			ispause_on = False; framerate = def_fps; timeoflastpausetoggle = pygame.time.get_ticks();
	if ispause_on: continue
		
	## computer paddle movements for intro and normal game modes
	if gamemode == "intro" or gamemode == "settings" or gamemode == "normal":
		if gamemode == "intro" or gamemode == "settings":
			computerpaddlespeed = intropaddlespeed; ballspeed = introballspeed; ycollisionfactor = introycollisionfactor
			# sets the ball speed and collision factor to that of the intro
			if 0 < abs(paddle1.rect.centery - paddle2.rect.centery) <= intropaddlespeed: #recalibrates the two paddles
				paddle2.rect.move(0, ((paddle1.rect.top+paddle1.rect.bottom)/2) - (paddle2.rect.top+paddle2.rect.bottom)/2)
			elif paddle1.rect.centery > paddle2.rect.centery:
				paddle1.move(0,-intropaddlespeed); paddle2.move(0,intropaddlespeed)
			elif paddle1.rect.centery < paddle2.rect.centery:
				paddle1.move(0,intropaddlespeed); paddle2.move(0,-intropaddlespeed)
			
			if (ball.rect.centerx >= width/2):
				paddlerect = paddle2.rect # if the ball is on the right side of the screen, the right paddle becomes the main paddle 
				if ballspeed[0]>0 and ball.rect.left <= paddlerect.right:  incomingballspeed = True # the ball is heading towards the main paddle
				elif ballspeed[0]<0:  incomingballspeed = False
			elif (ball.rect.centerx < width/2):
				paddlerect = paddle1.rect # if the ball is on the left side of the screen, the left paddle becomes the main paddle 
				if ballspeed[0]<0 and ball.rect.right >= paddlerect.left:  incomingballspeed = True # the ball is heading towards the main paddle
				elif ballspeed[0]>0:  incomingballspeed = False
		elif gamemode == "normal":
			paddlerect = paddle2.rect # the right paddle is the computer paddle by default
			if (ball.rect.centerx > width/2):
				if ballspeed[0]>0 and ball.rect.left <= paddlerect.right:  incomingballspeed = True # the ball is heading towards the main paddle
				elif ballspeed[0]<0:  incomingballspeed = False

		if ((abs(paddlerect.centery - ball.rect.centery) <= 2*ballheight) and incomingballspeed == True) and (0<=abs(paddlerect.centerx - ball.rect.centerx)<maxdistpaddleball*abs(ballspeed[0])) and paddlerect.top > upperlimit and paddlerect.bottom < height - lowerlimit:
# if the y-coordinate of the ball is near the center of the paddle, the ball is close enough to the paddle and is heading towards it, the paddle moves randomly		
			direction = randdirection
			if gamemode == "intro" or gamemode == "settings":   # if the game mode is intro, both paddles move at the same speed
				paddle1.move(0, direction*(computerpaddlespeed*randpaddlemovefactor)); paddle2.move(0, direction*(computerpaddlespeed*randpaddlemovefactor))
			elif gamemode == "normal":
				paddle2.move(0, direction*(computerpaddlespeed*randpaddlemovefactor))


		else: # otherwise, the computer paddle moves normally
			direction = randdirection = (randrange(-1,2,2))			
			if paddlerect.centery - ball.rect.centery > ballheight and paddlerect.top > upperlimit: # if the paddle is under the ball, the paddle moves up
				if gamemode == "intro" or gamemode == "settings": # if the game mode is intro, both paddles move at the same speed
					paddle1.move(0, -computerpaddlespeed); paddle2.move(0, -computerpaddlespeed)
				elif gamemode == "normal":
					paddle2.move(0, -computerpaddlespeed)
					
			elif paddlerect.centery - ball.rect.centery < -ballheight and paddlerect.bottom < height - lowerlimit: #if the paddle is above the ball, the paddle moves down
				if gamemode == "intro" or gamemode == "settings": # if the game mode is intro, both paddles move at the same speed
					paddle1.move(0, computerpaddlespeed); paddle2.move(0, computerpaddlespeed)
				elif gamemode == "normal":
					paddle2.move(0, computerpaddlespeed)

		
	## key input to control the paddles	
	if gamemode == "normal": # if the game mode is normal the 'm', 'k' and arrow keys are used to vertically control the player's paddle
		if keys[K_k] or keys[K_w] or keys[K_UP]: paddle1.move(0, -paddlespeed[1]) #move up
		if keys[K_m] or keys[K_s] or keys[K_DOWN]: paddle1.move(0, paddlespeed[1]) #move down
	elif gamemode == "twoplayers": # if the game mode is twoplayers the 'w' and 's' keys are used to control paddle1, and the 'k' and 'm' and arrow keys to control paddle2
		if keys[K_w]: paddle1.move(0, -paddlespeed[1])
		if keys[K_s]: paddle1.move(0, paddlespeed[1])
		if keys[K_k] or keys[K_UP]: paddle2.move(0, -paddlespeed[1])
		if keys[K_m] or keys[K_DOWN]: paddle2.move(0, paddlespeed[1])

	# prevents the paddles from going under and over the imposed vertical boundaries
	if paddle1.rect.y < upperlimit: paddle1.rect.y = upperlimit
	if paddle1.rect.bottom > height - lowerlimit: paddle1.rect.bottom = height - lowerlimit
	if paddle2.rect.y < upperlimit: paddle2.rect.y = upperlimit
	if paddle2.rect.bottom > height - lowerlimit: paddle2.rect.bottom = height - lowerlimit
	if ball.rect.y > height: ball.rect.y = height # if a part of the ball somehow gets outside the boundaries,
	if ball.rect.y < 0: ball.rect.y = 0			# it is brought back inside
	
	
	if ball.rect.right < 0 or ball.rect.left > width or ballreset == True:  # if the ball goes out of the right and left bounds of the screen
		if changescore is True: # change score once
			if ball.rect.right < 0: score2.text = str(int(score2.text) + 1)
			elif ball.rect.left > width: score1.text = str(int(score1.text) + 1)
			ball.rect = defaultballrect; previousballspeed = ballspeed; ballspeed = [0,0]; ballreset = True
			changescore = False; collisionsound("point")
		if pygame.time.get_ticks() - timeballout > 600: # wait 0.6 seconds before the ball reappears
			ball.rect = defaultballrect; ballspeed = previousballspeed; ballspeed[0] = -ballspeed[0]
			ballspeed[1] = (round(random(),2)+2) * (randrange(-1,2,2)) #generate a random nb between 1.2 and 2.2 
			changescore = True; ballreset = False


	elif ballpositionwait == True: # at the beginning of a game mode that is not intro, wait 0.6 seconds before the ball appears
		if pygame.time.get_ticks() - timeballout > 600: ballpositionwait = False
	
	elif finishgame == False: # if the ball is in the screen, it moves normally
		ball.move(ballspeed[0], ballspeed[1]); timeballout = pygame.time.get_ticks()
		
		
	if (ball.rect.top <= 0 or ball.rect.bottom >= height) and ballspeed[1]!=0 and pygame.time.get_ticks() - timebetweenwallhits >= 20: # if the ball goes out of the top and bottom bounds of the screen, its y coordinate is reversed
		ballspeed[1] = -ballspeed[1]; collisionsound("wallhit")
		timebetweenwallhits = pygame.time.get_ticks()
		
	
	if ball.rect[0] < (width/4): # if the ball is on the left side of the screen
		if paddle1.rect.right>=ball.rect.left and ball.rect.right>=paddle1.rect.left and ball.rect.top<=paddle1.rect.bottom and ball.rect.bottom>=paddle1.rect.top and pygame.time.get_ticks() - timebetweencollisions >= 300: # if the ball hits the left paddle
			collisionangle(paddle1.rect); ballspeed[0] = -ballspeed[0]; collisionsound("paddlehit")
			timebetweencollisions = pygame.time.get_ticks(); #prevents multiple collisions in a short amount of time
			
	elif ball.rect[0] > (width/4): # if the ball is on the right side of the screen
		if ball.rect.right>=paddle2.rect.left and ball.rect.left<=paddle2.rect.right and ball.rect.top<=paddle2.rect.bottom and ball.rect.bottom>=paddle2.rect.top and  pygame.time.get_ticks() - timebetweencollisions >= 300: # if the ball hits the right paddle
			collisionangle(paddle2.rect); ballspeed[0] = -ballspeed[0]; collisionsound("paddlehit")
			timebetweencollisions = pygame.time.get_ticks(); #prevents multiple collisions in a short amount of time

	
	for i in range (len(netrects_ypos)): screen.blit(net.surface, (net.rect.x, netrects_ypos[i]))
	paddle1.blit(); paddle2.blit()
	if (gamemode == "intro" or gamemode == "settings") or ((gamemode == "normal" or gamemode == "twoplayers") and (finishgame == False and ballreset == False)):
		ball.blit()
	if gamemode == "normal" or gamemode == "twoplayers":
		score1.blit(); score2.blit()
				
	pygame.display.flip()
	screen.fill(black_color)
	


##_______________________________________________________________________Game modes_______________________________________________________________________________##
	pressedkey = pygame.key.get_pressed() # keyinput		
	if gamemode == "intro": #run the intro game mode and displays the title and subtitle
		finishgame = False;
		title.blit(); subtitle.blit(); authornote.blit() #blit text surfaces
		
		if pressedkey[K_RETURN] or pressedkey[K_SPACE] or mouseclick == True: # if 'enter' or 'space' is pressed or the mouse is clicked on the screen, proceed
			gamemode = "settings"; kindchoice = "difficulty"; collisionsound("entergamemode")
			timebetweenintroandsettings = pygame.time.get_ticks()
	
	
	elif gamemode == "settings": #runs the settings panel for choosing difficulty and game mode
		title.blit(); comment.blit(); gameexplanation.blit(); toggles.blit((195,195,195)) # blit text surfaces
		timebetweensettingsandgame = pygame.time.get_ticks()
		
		if kindchoice == "difficulty":
			difficultychoice = changechoice_keys(difficultychoice, 1,3) #returns a number between 1 and 3
			if pygame.mouse.get_focused(): difficultychoice = changechoice_mouse(difficultychoice, difflist)	
		difflist[difficultychoice].outline()
			
		if kindchoice == "mode":
			modechoice = changechoice_keys(modechoice, 1,2) #returns a number between 1 and 2
			if pygame.mouse.get_focused(): modechoice = changechoice_mouse(modechoice, modelist)	
			modelist[modechoice].outline()
			if modechoice == 1: mode1player.blit()
			elif modechoice == 2: mode2player.blit()

		for i in range (len(difflist)): difflist[i].blit()
		for i in range (len(modelist)): modelist[i].blit()

		if kindchoice == "difficulty" and (pressedkey [K_RETURN] or pressedkey[K_SPACE] or mouseclick==True) and timebetweensettingsandgame - timebetweenintroandsettings >=250:
			kindchoice = "mode";  timechoicemade = pygame.time.get_ticks(); collisionsound("entergamemode")
		elif kindchoice == "difficulty" and (pressedkey[K_ESCAPE]or pressedkey[K_BACKSPACE]) and timebetweensettingsandgame - timechoicemade >=250:
			gamemode = "intro"; pygame.mouse.set_visible(True)
		elif kindchoice == "mode" and (pressedkey[K_ESCAPE] or pressedkey[K_BACKSPACE]) and timebetweensettingsandgame - timechoicemade >=250:
			kindchoice = "difficulty";  timechoicemade = pygame.time.get_ticks()
		elif kindchoice == "mode" and (pressedkey [K_RETURN] or pressedkey[K_SPACE] or mouseclick==True) and timebetweensettingsandgame - timechoicemade >=250: 
			score1.text = score2.text = "0"; scorelimit = originalscorelimit; collisionsound("entergamemode")
			difficultychanges(difficultychoice) # 1 corresponds to intermediate, 2 to hard, and 3 to expert
			if modechoice == 1: gamemode = "normal"; pygame.mouse.set_visible(False)
			elif modechoice == 2: gamemode = "twoplayers"; pygame.mouse.set_visible(False)
			
	
	elif gamemode == "normal" or gamemode == "twoplayers": #runs the game
		finishgame = int(score1.text) >= scorelimit or int(score2.text) >= scorelimit;
		if int(score1.text) == int(score2.text) == scorelimit - 1: scorelimit = scorelimit+1
		
		if finishgame == True and int(score1.text) >= scorelimit:
			gameover_lose.xpos += width/2; gameover_lose.blit(); gameover_lose.xpos -= width/2
			gameover_win.blit(); gameover_comment.blit()
		elif finishgame == True and int(score2.text) >= scorelimit:
			gameover_win.xpos += width/2; gameover_win.blit(); gameover_win.xpos -= width/2
			gameover_lose.blit(); gameover_comment.blit()
			
		if (finishgame == True and (pressedkey[K_RETURN] or pressedkey[K_SPACE] or mouseclick==True)):
			score1.text = score2.text = "0"; scorelimit = originalscorelimit; collisionsound("entergamemode") #makes finishgame false
			timeballout = pygame.time.get_ticks(); changescore = True; ballpositionwait = True; #waits for the ball to move, and displays it in the mean time
			
		elif (pressedkey[K_ESCAPE] or pressedkey[K_BACKSPACE]):
			gamemode = "intro"; pygame.mouse.set_visible(True)
			introballspeed[1] = ballspeed[1]/3   # when the "normal" or "twoplayers" game mode is exited, the y-movement of the ball is reduced so that the ball seems to move in the same direction
			if (introballspeed[0] > 0 and ballspeed[0] < 0) or (introballspeed[0] < 0 and ballspeed[0] > 0): introballspeed[0] = -introballspeed[0]

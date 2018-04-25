import pygame, sys
import random
import time

from pygame.locals import *


MAPWIDTH = 2560/2
MAPHEIGHT = 1440/2

class Room:

	def __init__(self, objects, hidingPlaces, doorIn, doorOut, colour, text = None):
		self.objects = objects
		self.hidingPlaces = hidingPlaces
		self.doorIn = doorIn
		self.doorOut = doorOut
		self.colour = colour
		self.text = pygame.mixer.Sound(text)
		self.playText = True


class Object:

	def __init__(self, imageFile, x, y, hidingCoordinates = None, text = None):
		self.name = imageFile.split(".png")[0]
		self.imageFile = pygame.image.load(imageFile).convert_alpha()
		self.width = self.imageFile.get_rect().size[0]/2 + 1 #The walls in the hall have to fit, and here in the test version the integers are made twice as small. When the number of pixels is odd, the new number will be 0.5 pixel to small, where integers are rounded below, which leads to cracks in the wall. Because of this, I give each object one pixel more, which you can hardly see in the result.
		self.height = self.imageFile.get_rect().size[1]/2 + 1
		self.x = x
		self.y = y
		self.image = pygame.transform.scale(self.imageFile, (self.width, self.height))
		self.hidingCoordinates = hidingCoordinates

		if text:
			self.text = pygame.mixer.Sound(text)

	def changeSizeImage(self, width, height):
		self.width = width
		self.height = height
		self.image = pygame.transform.scale(self.image, (self.width, self.height))


class Door:
	
	def __init__(self, imageFile, x, y):
		self.name = imageFile.split(".png")[0]
		self.imageFile = pygame.image.load(imageFile).convert_alpha()
		self.width = self.imageFile.get_rect().size[0]/2 + 2 # A marge because there absolutely has to be doors and the walls
		self.height = self.imageFile.get_rect().size[1]/2 + 2
		self.x = x
		self.y = y
		self.image = pygame.transform.scale(self.imageFile, (self.width, self.height))
		self.opened = False

	def changeSizeImage(self, width, height):
		self.width = width
		self.height = height
		self.image = pygame.transform.scale(self.image, (self.width, self.height))

	def open(self, side):
		self.opened = True
		self.image = pygame.transform.scale(self.image, (self.width / 2 + 1, self.height))

		if side == "right":
			self.x += self.width / 2

	def close(self, side):
		self.opened = False
		self.image = pygame.transform.scale(self.image, (self.width, self.height))

		if side == "right":
			self.x -= self.width / 2

	
def fillImages(filenameUntillNumber, numberOfFiles):
	images = []

	for i in range(1, numberOfFiles + 1):
		fileName = filenameUntillNumber + str(i) + ".png"
		image = pygame.image.load(fileName)

		width = image.get_rect().size[0] / 20 + image.get_rect().size[0] / 100
		height = image.get_rect().size[1] / 20 + image.get_rect().size[0] / 100				
		image = pygame.transform.scale(pygame.image.load(fileName), (width, height))

		images.append(image)
	
	return images

	
class Rat(pygame.sprite.Sprite):
		def __init__(self):
			super(Rat, self).__init__()

			self.images = self.fillImages("rat/rat", 8)
			self.index = 0		
			self.image = self.images[self.index]
			self.width = self.image.get_rect().size[0]
			self.height = self.image.get_rect().size[1]
			self.x = random.randint(-2400, MAPWIDTH + 2400)
			self.y = MAPHEIGHT - self.height - 10
			self.velocity = 10

		def fillImages(self, filenameUntillNumber, numberOfFiles):
			images = []

			for i in range(1, numberOfFiles + 1):
				fileName = filenameUntillNumber + str(i) + ".png"
				image = pygame.image.load(fileName)
				self.width = image.get_rect().size[0] / 3
				self.height = image.get_rect().size[1] / 3				
				image = pygame.transform.scale(image, (self.width, self.height))

				images.append(image)
	
			return images
			
		def changeDirection(self):
			change = random.randint(0, 250)
		
			if change == 250:
				return True
			else:
				return False
				
		def update(self):
			self.image = self.images[self.index]			
			self.index += 1
			self.width = self.image.get_rect().size[0]
			self.height = self.image.get_rect().size[1]
			self.x += self.velocity
			
			if self.changeDirection() or self.x < -2400 or self.x > MAPWIDTH + 2400:
				self.velocity = self.velocity * -1
			
			if self.velocity < 0:
				self.image = pygame.transform.flip(self.image, True, False)
			
			if self.index == len(self.images):
				self.index = 0
				
			self.rect = pygame.Rect(self.x, self.y, True, False)


class Man():

        def __init__(self):
                self.bodyImage = pygame.image.load("kammende man/lichaam.png")
                self.width = self.bodyImage.get_rect().size[0] / 2
                self.height = self.bodyImage.get_rect().size[1] / 2
                self.body = pygame.transform.scale(self.bodyImage, (self.width, self.height))

                self.headImage = pygame.image.load("kammende man/hoofd.png")
                self.head = pygame.transform.scale(self.headImage, (self.headImage.get_rect().size[0] / 2, self.headImage.get_rect().size[1] / 2))

                self.armImages = self.fillImages("kammende man/arm ", 8)
                self.arm = self.armImages[0]

                self.x = 5
                self.y = BATHROOM_DOOR.y - 5

                self.index = 0


        def fillImages(self, filenameUntillNumber, numberOfFiles):
		images = []

		for i in range(1, numberOfFiles + 1):
			fileName = filenameUntillNumber + str(i) + ".png"
			image = pygame.image.load(fileName)				
			width = image.get_rect().size[0] / 2
			height = image.get_rect().size[1] / 2
			image = pygame.transform.scale(image, (width, height))

			images.append(image)
	
		return images


	def updateImage(self):
                self.index += 0.3
                startOver = random.randint(1, 8)

                if self.index > 3:
                        if self.index > len(self.armImages) or startOver == 8:
                                self.index = 0

                self.arm = self.armImages[int(self.index)]

                
        def setY(self):
                heightArm = self.arm.get_rect().size[1]
                
                return self.y + (self.height) / 3 - heightArm + 40


        def setX(self):
                return int(self.x + self.width / 2 - self.index - 25 + 3)

        
	def comb(self):
                x = self.setX()
                y = self.setY()
                
                DISPLAYSURF.blit(self.arm, (x, y))
                self.updateImage()                
		
class Woman():

	def __init__(self):		
		self.bodyImage = pygame.image.load("vrouw/vrouw.png")
		self.width = self.bodyImage.get_rect().size[0] / 2
		self.height = self.bodyImage.get_rect().size[1] / 2
		self.body = pygame.transform.scale(self.bodyImage, (self.width, self.height))
		self.thumbImage = pygame.image.load("vrouw/duim.png")
		self.thumb = pygame.transform.scale(self.thumbImage, (self.thumbImage.get_rect().size[0] / 2, self.thumbImage.get_rect().size[1] / 2))
		self.screenImages = self.fillImages("vrouw/scherm ", 4)
		self.screen = self.screenImages[0]
		self.x = CHAIR_LEFT.x + CHAIR_LEFT.width - self.width
		self.y = CHAIR_LEFT.y - self.height / 2
		
	def fillImages(self, filenameUntillNumber, numberOfFiles):
		images = []

		for i in range(1, numberOfFiles + 1):
			fileName = filenameUntillNumber + str(i) + ".png"
			image = pygame.image.load(fileName)				
			width = image.get_rect().size[0] / 2 + 10
			height = image.get_rect().size[1] / 2 + 10
			image = pygame.transform.scale(image, (width, height))

			images.append(image)
	
		return images
		
	def changeScreen(self):
		self.screen = random.choice(self.screenImages)

		
class Girl():
	def __init__(self):
		self.bodyImage = pygame.image.load("lezend meisje/meisje achter.png")
		self.width = self.bodyImage.get_rect().size[0] / 2
		self.height = self.bodyImage.get_rect().size[1] / 2
		self.body = pygame.transform.scale(self.bodyImage, (self.width, self.height))
		self.handAndFeetImage = pygame.image.load("lezend meisje/meisje voor.png")
		self.handAndFeet = pygame.transform.scale(self.handAndFeetImage, (self.handAndFeetImage.get_rect().size[0] / 2, self.handAndFeetImage.get_rect().size[1] / 2))
		self.sheetImages = self.fillImages("lezend meisje/blad ", 5)
		self.sheet = self.sheetImages[4]
		self.x = BED_BACK.x + 50
		self.y = BED_BACK.y - 50
		self.index = 0
		
	def fillImages(self, filenameUntillNumber, numberOfFiles):
		images = []

		for i in range(1, numberOfFiles + 1):
			fileName = filenameUntillNumber + str(i) + ".png"
			image = pygame.image.load(fileName)
			width = image.get_rect().size[0] / 2
			height = image.get_rect().size[1] / 2
			image = pygame.transform.scale(image, (width, height))

			images.append(image)
	
		return images
		
	def movePage(self):
		if int(self.index) == len(self.sheetImages):
			self.index = 0
	
		self.sheet = self.sheetImages[int(self.index)]
		self.index += 0.2					

		
class Boy():
	def __init__(self):
		self.bodyImage = pygame.image.load("snoepend jongetje/jongen.png")
		self.width = self.bodyImage.get_rect().size[0] / 2
		self.height = self.bodyImage.get_rect().size[1] / 2
		self.body = pygame.transform.scale(self.bodyImage, (self.width, self.height))
		
		self.arm = self.loadImage("snoepend jongetje/likarm.png", 2)		
		self.hand = self.loadImage("snoepend jongetje/likhand.png", 2)
		self.handRest = self.loadImage("snoepend jongetje/rusthand.png", 2)
		
		self.x = CHAIR_YELLOW_RIGHT.x + 60
		self.y = CHAIR_YELLOW_RIGHT.y - 65
		self.index = 0
		
		
	def loadImage(self,  image, shortening):
		image = pygame.image.load(image)
		
		return pygame.transform.scale(image, (image.get_rect().size[0] / shortening, image.get_rect().size[1] / shortening))

		
	def bowArmDown(self):
		arm = pygame.transform.rotate(self.arm, self.index * -15)
		handX = self.x + arm.get_rect().size[0] - 15
		handY = TABLE_BACK.y + 8 * self.index + 7

		DISPLAYSURF.blit(arm,(self.x - 5, TABLE_BACK.y + 5))
		DISPLAYSURF.blit(self.hand, (handX, handY))
		
		
	def bowArmUp(self, endFrame):
		arm = pygame.transform.rotate(self.arm, (endFrame - self.index) * -15)
		hand = pygame.transform.rotate(self.hand, 105)
		handX = self.x + arm.get_rect().size[0] - 15
		handY = TABLE_BACK.y + 8 * (endFrame - self.index) + 7
		
		DISPLAYSURF.blit(arm, (self.x - 5, TABLE_BACK.y + 5))
		DISPLAYSURF.blit(hand, (handX, handY))
	
	
	def bowArmToMouth(self, startFrame):
		arm = pygame.transform.rotate(self.arm, (self.index - startFrame) * 15)
		hand = pygame.transform.rotate(self.hand, 105)
		handX = self.x + arm.get_rect().size[0] - 15
		handY = TABLE_BACK.y - 8 * (self.index - startFrame) + 7
		
		DISPLAYSURF.blit(arm,(self.x - 5, TABLE_BACK.y - 4.7 * (self.index - startFrame) + 5))
		DISPLAYSURF.blit(hand, (handX, handY))

		
	def bowArmFromMouth(self, endFrame):
		arm = pygame.transform.rotate(self.arm, endFrame - self.index * 15)
		handX = self.x + arm.get_rect().size[0] - 15
		handY = TABLE_BACK.y - 8 * (endFrame - self.index) + 7
		
		DISPLAYSURF.blit(arm,(self.x - 5, TABLE_BACK.y - 4.7 * (endFrame - self.index) + 5))
		DISPLAYSURF.blit(self.hand, (handX, handY))
		

	def munch(self):
		armToPotFrames = 6
		armToMouthFrames = 8		
		move = 5
		
		if self.index == armToPotFrames + armToMouthFrames:
			self.index = 0
		
		if self.index < armToPotFrames / 2:
			self.bowArmDown()
			
		elif self.index < armToPotFrames:
			self.bowArmUp(armToPotFrames)
			
		elif self.index < armToPotFrames + armToMouthFrames / 2:
			self.bowArmToMouth(armToPotFrames)			
		else:
			self.bowArmFromMouth(armToPotFrames + armToMouthFrames)
			
                if self.index == armToPotFrames + armToMouthFrames / 2 - 1:
                        move = random.randint(1, 5)

		if move == 5: 	
			self.index += 1
			
		
class Cat():
	def __init__(self):
		self.bodyImage = pygame.image.load("wantrouwende kat/kat.png")
		self.width = self.bodyImage.get_rect().size[0] / 5
		self.height = self.bodyImage.get_rect().size[1] / 5
		self.body = pygame.transform.scale(self.bodyImage, (self.width, self.height))
		self.tailImages = self.fillImages("wantrouwende kat/staart ", 4)
		self.tail = self.tailImages[0]
		self.tailWidth = self.tail.get_rect().size[0]
		self.x = BENCH.x + BENCH.width - self.width - 20
		self.y = BENCH.y - self.height + 15
		self.index = 0
		
	def fillImages(self, filenameUntillNumber, numberOfFiles):
		images = []

		for i in range(1, numberOfFiles + 1):
			fileName = filenameUntillNumber + str(i) + ".png"
			image = pygame.image.load(fileName)
			width = image.get_rect().size[0] / 5
			height = image.get_rect().size[1] / 5
			image = pygame.transform.scale(image, (width, height))

			images.append(image)
	
		return images
				
	def moveTail(self):
		self.index += random.randint(-1, 1)	

		if self.index < 0:
			self.index = 0

		elif self.index > len(self.tailImages) - 1:
			self.index = len(self.tailImages) - 1
			
		self.tail = self.tailImages[self.index]
		self.tailWidth = self.tail.get_rect().size[0]
		
		
class Bird(pygame.sprite.Sprite):

	def __init__(self):
		super(Bird, self).__init__()

		self.images = fillImages("vogeltje/vliegend vogeltje000", 8)
		self.index = 0		
		self.image = self.images[self.index]
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[1]
		self.x = random.randint(-600, MAPWIDTH + 600)
		self.y = random.randint(-200, int(MAPHEIGHT * 0.25))
		self.velocity = random.choice([-6, -5, -4, -3, 3, 4, 5, 6])
		self.flapping = False

	def updateVelocity(self):
		
		if self.flapping:
			if self.velocity < 0:
				self.velocity -= 1
			else:
				self.velocity +=1
		else:
			if self.velocity < 0:
				self.velocity += 1
			else:
				self.velocity -= 1
		return


	def updateIndex(self):
		if self.flapping == False:
			if self.velocity > -3 and self.velocity < 3:
				self.flapping = True
			else:
				self.flapping = random.choice([False, False, False, False, False, False, False, False, False, False, True])			

		else:
			self.index += 1

			if self.index == len(self.images):
				self.index = 0
				self.flapping = False					
		return

		
	def transformPicture(self, xDelta, yDelta):
		if xDelta > 0:
			self.image = pygame.transform.flip(self.image, True, False)

		return


	def update(self, xDelta, yDelta):		
		self.x += xDelta
		self.y += yDelta
		self.image = self.images[self.index]

		self.transformPicture(xDelta, yDelta)
		self.updateVelocity()
		self.updateIndex()

		self.rect = pygame.Rect(self.x, self.y, True, False)


	def changeDirection(self):
		change = random.randint(0, 500)
		
		if change == 500:
			return True
		else:
			return False


	def fly(self):
		changeDirection = self.changeDirection()

		if changeDirection or self.x < -600 or self.x > MAPWIDTH + 600:
			self.velocity = self.velocity * -1

		deltaX = self.velocity

		if self.y > PLAYHOUSE_BACK.y + PLAYHOUSE_BACK.height - self.height:
			deltaY = -3
		else:
			deltaY = random.randint(-3, 3)

		self.update(deltaX, deltaY)
 


class Head(pygame.sprite.Sprite):

	def __init__(self):
		super(Head, self).__init__()

		self.x = 0
		self.y = 0
		self.images = fillImages("Mickey staat stil/kop ", 5)

		self.index = 0
		self.image = self.images[self.index]
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[1]


	def update(self):

		self.index += random.randint(-1, 1)	

		if self.index < 0:
			self.index = 0

		elif self.index > len(self.images) - 1:
			self.index = len(self.images) - 1

		self.image = self.images[self.index]	
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[1]
		self.rect = pygame.Rect(self.x, self.y, True, False)

	def place(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, True, False)


class Tail(pygame.sprite.Sprite):

	def __init__(self):
		super(Tail, self).__init__()

		self.x = 0
		self.y = 0
		self.images = fillImages("Mickeys staart/staart ", 5)
		self.index = 0
		self.image = self.images[self.index]
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[1]


	def update(self, direction = 1):

		self.index += direction

		self.image = self.images[self.index]
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[1]
		self.rect = pygame.Rect(self.x, self.y, True, False)


	def place(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, True, False)

		

class Mickey(pygame.sprite.Sprite):

	def __init__(self):
		super(Mickey, self).__init__()

		self.x = DOOR_GARDEN.x - 10 #I make it as easy as possible for myself to let mickey run correctly through this door. Besides, it is approximately the middle of the screen
		self.y = MAPHEIGHT - 200
		#The size is no 10 times smaller than the originale / 2 + a part 100 times smaller than the original.
		self.width = 188 / 2 + 19 
		self.height = 134 / 2 + 13

		self.walkImages = fillImages("tekeningen/MickeyLoopt/MickeyLoopt000", 10)
		self.comeImages = fillImages("MickeyKomtEnGaat/MickeyKomtAnimate/MickeyKomt000", 10)
		self.goImages = fillImages("MickeyKomtEnGaat/MickeyGaatAnimate/MickeyGaat000", 10)
		self.jumpImages = fillImages("MickeySpringt/MickeySpringt_Animator/MickeySpringt000", 12)

		self.index = 0
		self.image = self.walkImages[self.index]
		self.rect = pygame.Rect(self.x, self.y, True, False)
		self.found = False
		

	def updateImage(self, images, action):

		if action == "slide":
			self.image = self.jumpImages[7]
		else:
			self.image = images[self.index]


	def chooseImages(self, action):
		
 		if action == "jump":
			return self.jumpImages
		
		elif action == "coming":
			return self.comeImages

		elif action == "going":
			return self.goImages
		else:
			return self.walkImages


	#Lets the sprite make a movement. For the update function it is beuid-in that we can use it for the sprite group (which is name mickey in the code). The parameters are the delta for x and the delta for y.
	def update(self, xDelta, yDelta, action = None):
		images = self.chooseImages(action)
		
		if self.index >= len(images) - 1 or self.index < 0:
			self.index = 0
		
		self.x += xDelta
		self.y += yDelta
		self.updateImage(images, action)
					
		if xDelta < 0:
			self.image = pygame.transform.flip(self.image, True, False)
	
		self.index += 1
		
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[1]
		self.rect = pygame.Rect(self.x, self.y, True, False)
		

	#Places the sprite on a x and y coordinate you give as parameters to this function.
	def place(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, True, False)


	#Changes particulair parameters to the start state of the sprite
	def reset(self):
		self.width = 188 / 2 + 19 
		self.height = 134 / 2 + 13 
		self.x = DOOR_GARDEN.x - 10
		self.y = MAPHEIGHT - 200
		self.rect = pygame.Rect(self.x, self.y, True, False)

		
clock = pygame.time.Clock()
FPS = 30

pygame.init()
pygame.mixer.init(channels = 4)

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH, MAPHEIGHT))
CHANNEL = pygame.mixer.find_channel()

VELOCITY_MICKEY = 6

SHOW_PATH = False
X_COORDINATES = []
Y_COORDINATES = []


START_PAGE = pygame.transform.scale(pygame.image.load("startpagina.png").convert_alpha(), (MAPWIDTH, MAPHEIGHT))

#Hall
HALL_MAP = 'halMap/'

FLOOR = Object(HALL_MAP + 'vloer.png' ,0, MAPHEIGHT - 270)
HAT_RACK = Object(HALL_MAP + 'kapstok.png', 200, 210)
LAMP = Object(HALL_MAP + 'lamp.png', MAPWIDTH/2 - 50, 64)
PLANT = Object(HALL_MAP + 'plantje.png', 700, 154)

WALL_LEFT_1 = Object(HALL_MAP + 'muurLinks1.png', 0, 0)
WALL_LEFT_2 = Object(HALL_MAP + 'muurLinks2.png', 70, 16)
WALL_LEFT_3 = Object(HALL_MAP + 'muurLinks3.png', 70 + 138, 48)
WALL_LEFT_4 = Object(HALL_MAP + 'muurLinks4.png', 70 + 138 + 91, 70)
WALL_RIGHT_1 = Object(HALL_MAP + 'muurRechts1.png', MAPWIDTH - 170, 0)
WALL_RIGHT_2 = Object(HALL_MAP + 'muurRechts2.png', MAPWIDTH - 170 - 117, 40)
WALL_RIGHT_3 = Object(HALL_MAP + 'muurRechts3.png', MAPWIDTH - 170 - 117 - 91, 68)
WALL_REAR = Object(HALL_MAP + 'Middel_32.png', 0, 0)

DOOR_BARN = Door(HALL_MAP + 'deurLinksVoor.png', 33, 100)
DOOR_TOILET = Door(HALL_MAP + 'deurLinksMidVoor.png', 179, 118)
DOOR_KITCHEN = Door(HALL_MAP + 'duerLinksMidAchter.png', 276, 127)
DOOR_LIVING_ROOM = Door(HALL_MAP + 'deurLinksAchter.png', 353, 139)
DOOR_BEDROOM = Door(HALL_MAP + 'deurRechtsVoor.png', 2130/2, 226/2)
DOOR_BATHROOM = Door(HALL_MAP + 'deurRechtsMidden.png',  1930/2, 256/2)
DOOR_CHILDRENSROOM = Door(HALL_MAP + 'deurRechtsAchter.png', 1774/2, 282/2)
DOOR_GARDEN = Door(HALL_MAP + 'deurAchter.png', 604, 149)


#bedroom
BEDROOM_MAP = 'Mickey261017/slaapkamer/'

BACKGROUND_BEDROOM = Object(BEDROOM_MAP +'achtergrond.png', 0, 0)
  
ELDERDOWN = Object(BEDROOM_MAP +'dekbed.png', 358, 408)
BED_REAR = Object(BEDROOM_MAP +'bedAchter.png', 380, 300)
PILLOW1 = Object(BEDROOM_MAP +'kussen1.png', 530, 361, (500, 380), "Geluidsopnamen/AchterHetKussen.ogg")
PILLOW2 = Object(BEDROOM_MAP +'kussen2.png', 625, 361, (650, 380), "Geluidsopnamen/AchterHetKussen.ogg")
DOG_UNDER_ELDERDOWN = Object(BEDROOM_MAP +'hondOnderDekbed.png', 549, 370, (600, 380), "Geluidsopnamen/OnderHetDekbed.ogg")

BEDROOM_DOOR = Object(BEDROOM_MAP +'deur.png', 123, 114)
 
CURTAIN_LEFT = Object(BEDROOM_MAP +'gordijnLinks.png', 1153, 55, (1120, 676 - 134 / 2), "Geluidsopnamen/tussenDeGordijnen.ogg")
CURTAIN_MID_LEFT = Object(BEDROOM_MAP +'gordijnMiddenLinks.png', 1133, 61, (1100, 657 - 134 / 2), "Geluidsopnamen/tussenDeGordijnen.ogg")
CURTAIN_MID_RIGHT = Object(BEDROOM_MAP +'gordijnMiddenRechts.png', 1113, 67, (1080, 642 - 134 / 2), "Geluidsopnamen/tussenDeGordijnen.ogg")
CURTAIN_RIGHT = Object(BEDROOM_MAP +'gordijnRechts.png', 1093, 76, (1060, 630 - 134 / 2), "Geluidsopnamen/AchterDeGordijnen.ogg")

CLOSET_CLOSED = Object(BEDROOM_MAP +'kastDicht.png', 330, 71)
CLOSET_OPEN = Object(BEDROOM_MAP +'kastOpen.png', 385, 71)
REAR_WALL_CLOSET = Object(BEDROOM_MAP +'achterwandKast.png', 320, 60)
FRONT_WALL_CLOSET = Object(BEDROOM_MAP +'voorwandKast.png', 223, 53, (223, 490), "Geluidsopnamen/InDeKast.ogg")

WALL_PART = Object(BEDROOM_MAP +'muurstukje.png', 5, 0) 
WALL_REST = Object(BEDROOM_MAP +'muurrest.png', 0, 0)

CHAIR_BACK = Object(BEDROOM_MAP +'stoelAchter.png', 855, 533, (865, 533 + 20), "Geluidsopnamen/AchterDeStoel.ogg") 
CHAIR_FRONT = Object(BEDROOM_MAP +'stoelVoor.png', 950, 413, (927, 533 - 134 / 2), "Geluidsopnamen/OpDeStoel.ogg")
 
TABLE = Object(BEDROOM_MAP +'tafel.png', 832, 334)

HAMPER_REAR = Object(BEDROOM_MAP +'wasmandAchter.png', 9, 575)
HAMPER_LID_CLOSED = Object(BEDROOM_MAP +'wasmandDekselDicht.png', 7, 575)
HAMPER_LID_OPEN = Object(BEDROOM_MAP +'wasmandDekselOpen.png', 7, 525)
HAMPER_FRONT = Object(BEDROOM_MAP +'wasmandVoor.png', 9, 575, (14, 575 + 134 / 2), "Geluidsopnamen/InDeWasmand.ogg") 


#BATHROOM
BATHROOM_MAP = 'badkamer/'

BACKGROUND_BATHROOM = Object(BATHROOM_MAP + 'achtergrond.png', 0, 0)

BATH_REAR = Object(BATHROOM_MAP + 'bad_achter.png', 986/2, 269/2)
BATH_FRONT = Object(BATHROOM_MAP + 'bad_voor.png', 986/2, 825/2, (986/2 + 982 / 4, 825/2), "Geluidsopnamen/InHetBad.ogg")

BATHROOM_DOOR = Object(BATHROOM_MAP + 'deur.png', 199/2, 224/2)

TOWEL_FLAT = Object(BATHROOM_MAP + 'handdoek_plat.png', 1105, 440, (1105, 400 + 510/2 - 134 / 2))
TOWEL_WIDE = Object(BATHROOM_MAP + 'handdoek_wijd.png', 1105, 440, (1105, 400 + 510/2 - 134 / 2), "Geluidsopnamen/OnderDeHanddoek.ogg")

STOOL = Object(BATHROOM_MAP + 'krukje.png', 1862/2, 902/2, (1830/2, 830/2 + 297/2 - 134 / 2, ), "Geluidsopnamen/AchterDeKruk.ogg")

BATHROOM_WALLS = Object(BATHROOM_MAP + 'muren.png', 0, 0)
BATHROOM_WALLPART = Object(BATHROOM_MAP + 'muurstukje.png', 0, 0)
BATHROOM_FLOOR = Object(BATHROOM_MAP + 'vloer.png', 0, MAPHEIGHT - 400/2)

SINK = Object(BATHROOM_MAP + 'wastafel.png', 1950/2, 413/2)
TOILET_BATHROOM = Object(BATHROOM_MAP + 'wc.png', 480/2, 632/2, (300, 632/2 + 492/2 - 134 / 2 - 20), "Geluidsopnamen/AchterDeWc.ogg")

MAT_HUMP = Object(BATHROOM_MAP + 'matje_bult.png', 1035/2, 1052/2, (1035/2 + 130, 1052/2), "Geluidsopnamen/OnderHetMatje.ogg")
MAT_FLAT = Object(BATHROOM_MAP + 'matje_plat.png', 1035/2, 1175/2)


#Children's room
CHILDRENS_ROOM_MAP = 'MickeyKinderkamer/'

BALL = Object(CHILDRENS_ROOM_MAP + 'bal.png', 902, 550, text = "Geluidsopnamen/AchterDeBal.ogg")

BED_BACK = Object(CHILDRENS_ROOM_MAP + 'bed_achter.png', 277, 155)
BED_FRONT = Object(CHILDRENS_ROOM_MAP + 'bed_voor.png', 305, 148)

BEAR = Object(CHILDRENS_ROOM_MAP + 'beer.png', 559, 105, (564, 165), "Geluidsopnamen/AchterDeBeer.ogg")
DOLL_WHITE = Object(CHILDRENS_ROOM_MAP + 'blanke_pop.png', 304, 454, (304, 449), "Geluidsopnamen/AchterDePoppen.ogg")
DOLL_BROWN = Object(CHILDRENS_ROOM_MAP + 'bruine_pop.png', 237, 469, (255, 484), "Geluidsopnamen/tussenDePoppen.ogg")

CHILDRENSROOM_DOOR = Object(CHILDRENS_ROOM_MAP + 'deur.png', 8, 80)

LITTLE_CLOSET = Object(CHILDRENS_ROOM_MAP + 'kastje.png', 1089, 454, (1069, 560), "Geluidsopnamen/AchterHetKastje.ogg")#Text file is missing
WALLS_CHILDRENSROOM = Object(CHILDRENS_ROOM_MAP + 'muren.png', -10, 1)
WALLPART_CHILDRENSROOM = Object(CHILDRENS_ROOM_MAP + 'muurstukje.png', 0, 0)

DOLL_CARRIAGE_BACK = Object(CHILDRENS_ROOM_MAP + 'poppenwagen_achter.png', 477, 544)
DOLL_CARRIAGE_FRONT = Object(CHILDRENS_ROOM_MAP + 'poppenwagen_voor.png', 460, 536, (480, 540), "Geluidsopnamen/InDePoppenwagen.ogg")

TENT_BACK = Object(CHILDRENS_ROOM_MAP + 'tent_achter.png', 787, 230)
TENT_CLOSED = Object(CHILDRENS_ROOM_MAP + 'tent_dicht.png', 777, 403)
TENT_OPEN = Object(CHILDRENS_ROOM_MAP + 'tent_open.png', 757, 403)
TENT_FRONT = Object(CHILDRENS_ROOM_MAP + 'tent_voor.png', 737, 227, (767, 227  + 744/2 - 134 / 2 - 50), "Geluidsopnamen/InDeTent.ogg")

TRAIN = Object(CHILDRENS_ROOM_MAP + 'trein.png', 850, 614)

#BARN
BARN_MAP = 'schuur/'

BACKGROUND_BARN = Object(BARN_MAP + 'achtergrond.png', 0, 0)
BARN_DOOR = Object(BARN_MAP + 'deur.png', 1087, 105)
BARN_WALL_PART = Object(BARN_MAP + 'muurstukje.png', 1151, 0)

BOX_BACK = Object(BARN_MAP + 'doos_achter.png', 462, 505, text = "Geluidsopnamen/AchterDeDoos.ogg")
BOX_FRONT = Object(BARN_MAP + 'doos_voor.png', 462, 545, (462 + 25, 565), "Geluidsopnamen/InDeDoos.ogg")

BICYCLE_BAG_BACK = Object(BARN_MAP + 'fiets_tas_achter.png', 5, 296)
BAG_FLAP_ALMOST_CLOSED = Object(BARN_MAP + 'tasklep_bijna_dicht.png', 65, 420)
BAG_FLAP_CLOSED = Object(BARN_MAP + 'tasklep_dicht.png', 65, 425)
BAG_FLAP_OPEN = Object(BARN_MAP + 'tasklep_open.png', 65, 370)
BAG_FRONT = Object(BARN_MAP + 'tas_voor.png', 122, 453, (122 + 50, 440), "Geluidsopnamen/InDeFietstas.ogg")

RAKE_BROOM_SHOVEL = Object(BARN_MAP + 'hark_veger_schep.png', 719, 207, (790, 480), text = "Geluidsopnamen/AchterDeHark.ogg")

WHEELBARROW = Object(BARN_MAP + 'kruiwagen.png', 893, 265, (893, 400), "Geluidsopnamen/InDeKruiwagen.ogg")

FOOTBALL = Object(BARN_MAP + 'voetbal.png', 280, 612)

GARBAGE_CAN = Object(BARN_MAP + 'vuilnisbak.png', 251, 305)

#WORK_TABLE_BIGGER = Object(BARN_MAP + 'werktafel_groter.png', 361, 421)
WORK_TABLE = Object(BARN_MAP + 'werktafel.png', 361, 421)


#TOILET
TOILET_MAP = "wc/"

BACKGROUND_TOILET = Object(TOILET_MAP + 'achtergrond.png', 0, 0)
TOILET_DOOR = Object(TOILET_MAP + 'deur.png', 919, 120)
WALLS_TOILET = Object(TOILET_MAP + 'muren.png', 0, 0)
WALL_PART_TOILET = Object(TOILET_MAP + 'muurstukje.png', 967, 0)

TOWEL_FLAT_TOILET = Object(TOILET_MAP + 'handdoek_plat.png', 514, 341, (478, 341 + 510/2 - 134 / 2))
TOWEL_WIDE_TOILET = Object(TOILET_MAP + 'handdoek_wijd.png', 478, 341, (478, 341 + 510/2 - 134 / 2), "Geluidsopnamen/OnderDeHanddoek.ogg")

TOILET_CLOSET_CLOSED = Object(TOILET_MAP + 'kast_dicht.png', 629, 384, text = "Geluidsopnamen/InDeKast.ogg")
TOILET_CLOSET_OPEN = Object(TOILET_MAP + 'kast_open.png', 629, 384)
TOILET_CLOSET = Object(TOILET_MAP + 'kast.png', 616, 144)

GARBAGE_CAN_TOILET = Object(TOILET_MAP + 'vuilnisbak.png', 1103, 546, text = "Geluidsopnamen/AchterDePrullenbak.ogg")

TOILET = Object(TOILET_MAP + 'wc.png', 187, 324, (290, 540), "Geluidsopnamen/AchterDeWc.ogg")
TOILET_ROLLS_MASS = Object(TOILET_MAP + 'wcrollenberg.png', 35, 515)
TOILET_ROLLS_PILE = Object(TOILET_MAP + 'wcrollenstapel.png', 65, 510, (150, 550), "Geluidsopnamen/AchterDeWcRollen.ogg")


#KITCHEN
KITCHEN_MAP = "keuken/"

BACKGROUND_KITCHEN = Object(KITCHEN_MAP + 'achtergrond.png', 0, 0)
KITCHEN_DOOR = Object(KITCHEN_MAP + 'deur.png', 1031, 121)
WALLS_KITCHEN = Object(KITCHEN_MAP + 'muren.png', 0, 0)
WALL_PART_KITCHEN = Object(KITCHEN_MAP + 'muurstukje.png', 1077, 0)

CASES_BACK = Object(KITCHEN_MAP + 'kratten achter.png', 1121, 232)
CASES_FRONT = Object(KITCHEN_MAP + 'kratten voor.png', 1129, 232, text = "Geluidsopnamen/InHetKrat.ogg")

DRAWER_OPEN_BACK = Object(KITCHEN_MAP + 'la open achterkant.png', 834, 453)
DRAWER_OPEN_FRONT = Object(KITCHEN_MAP + 'la open voorkant.png', 834, 453, text = "Geluidsopnamen/InDeLa.ogg")

KITCHEN_PLANT = Object(KITCHEN_MAP + 'plant.png', 5, 174, (55, 174 + 400), "Geluidsopnamen/AchterDePlant.ogg")

CHAIR_BLUE_LEFT_BACK = Object(KITCHEN_MAP + 'stoel blauw links achterkant.png', 357, 547, (357, 557), text = "Geluidsopnamen/OnderDeTafel.ogg")
CHAIR_BLUE_LEFT_FRONT = Object(KITCHEN_MAP + 'stoel blauw links voorkant.png', 350, 447, (350, 560 - 134/2), "Geluidsopnamen/OpDeStoel.ogg")
CHAIR_BLUE_RIGHT_BACK = Object(KITCHEN_MAP + 'stoel blauw rechts achterkant.png', 500, 539, (500, 556), text = "Geluidsopnamen/OnderDeTafel.ogg")
CHAIR_BLUE_RIGHT_FRONT = Object(KITCHEN_MAP + 'stoel blauw rechts voorkant.png', 489, 434, (500, 550 - 134/2), "Geluidsopnamen/OpDeStoel.ogg")
CHAIR_YELLOW_LEFT = Object(KITCHEN_MAP + 'stoel geel links.png', 564, 359)
CHAIR_YELLOW_RIGHT = Object(KITCHEN_MAP + 'stoel geel rechts.png', 658, 372)

TABLE_BACK = Object(KITCHEN_MAP + 'tafel achterkant.png', 491, 385)
TABLE_FRONT = Object(KITCHEN_MAP + 'tafel voorkant.png', 373, 365)


#Living room
LIVING_ROOM_MAP = "zitkamer/"

BENCH = Object(LIVING_ROOM_MAP + 'bank.png', 350, 400, (490, 480), "Geluidsopnamen/OnderDeBank.ogg")
PILLOW_BLUE = Object(LIVING_ROOM_MAP + 'kussen blauw.png', 380, 420, (370, 400), "Geluidsopnamen/AchterDeKussens.ogg")
PILLOW_GREEN = Object(LIVING_ROOM_MAP + 'kussen groen.png', 370, 435)
PILLOW_YELLOW = Object(LIVING_ROOM_MAP + 'kussen geel.png', 385, 450)
PILLOW_PURPLE = Object(LIVING_ROOM_MAP + 'kussen paars.png', 420, 445)

DESK_BACK = Object(LIVING_ROOM_MAP + 'bureau achterkant.png', 910, 395, (905, 450), "Geluidsopnamen/AchterHetBureau.ogg")
OFFICE_CHAIR = Object(LIVING_ROOM_MAP + 'bureaustoel.png', 885, 380, (930, 410), "Geluidsopnamen/OpDeBureaustoel.ogg")
DESK_FRONT = Object(LIVING_ROOM_MAP + 'bureau voorkant.png', 950, 320, (950, 320 + 293 - 84), "Geluidsopnamen/OnderHetBureau.ogg")#DESK_FRONT.x + DESK_FRONT.height - mickey.height - 12

LIVING_ROOM_DOOR = Object(LIVING_ROOM_MAP + 'deur.png', 1100, 100)
WALLS_LIVING_ROOM = Object(LIVING_ROOM_MAP + 'muren.png', 0, 0)
WALL_PART_LIVING_ROOM = Object(LIVING_ROOM_MAP + 'muurstukje.png', 1142, 0)

PLANT_LIVING_ROOM = Object(LIVING_ROOM_MAP + 'plant.png', 3, 460, (10, 460 + 30), "Geluidsopnamen/InDePlant.ogg")

CHAIR_LEFT = Object(LIVING_ROOM_MAP + 'stoel links.png', 160, 460, (200, 460), "Geluidsopnamen/OpDeStoel.ogg")
CHAIR_RIGHT = Object(LIVING_ROOM_MAP + 'stoel rechts.png', 550, 440, (670, 420), "Geluidsopnamen/OpDeLeuning.ogg")

COFFEE_TABLE_BACK = Object(LIVING_ROOM_MAP + 'salontafel achter.png', 435, 535)
COFFEE_TABLE_FRONT = Object(LIVING_ROOM_MAP + 'salontafel voor.png', 380, 505)


#GARDEN
GARDEN_MAP = "tuin/"

BACKGROUND_GARDEN = Object(GARDEN_MAP + 'achtergrond.png', 0, 0)

TREE = Object(GARDEN_MAP + 'boom.png', 0, 0, (450, 25), "Geluidsopnamen/InDeBoom.ogg")

WATERING_CAN = Object(GARDEN_MAP + 'gieter.png', 703, 571, (800, 600), "Geluidsopnamen/AchterDeGieter.ogg")
GRASS = Object(GARDEN_MAP + 'gras.png', 0, 650, (100, 690), "Geluidsopnamen/TussenHetGras.ogg")

HAMMOCK_BACK = Object(GARDEN_MAP + 'hangmat achter.png', 145, 190)
HAMMOCK_FRONT = Object(GARDEN_MAP + 'hangmat voor.png', 180, 215, text = "Geluidsopnamen/InDeHangmat.ogg")

PARASOL = Object(GARDEN_MAP + 'parasol.png', 1060, 370, (1065, 460), "Geluidsopnamen/OnderDeParasol.ogg")
STICK_PARASOL = Object(GARDEN_MAP + 'parasolsteel.png', 1035, 435)

PLAYHOUSE_BACK = Object(GARDEN_MAP + 'speelhut achter.png', 875, 5)
PLAYHOUSE_FRONT = Object(GARDEN_MAP + 'speelhut voor.png', 705, 5, (955, 120), "Geluidsopnamen/OpDeGlijbaan.ogg")

BEACHCHAIR_BACK = Object(GARDEN_MAP + 'strandstoel achter.png', 740, 430, (740, 500), "Geluidsopnamen/AchterDeStrandstoel.ogg")
BEACHCHAIR_FRONT = Object(GARDEN_MAP + 'strandstoel voor.png', 740, 438, (840, 478), "Geluidsopnamen/OpDeStrandstoel.ogg")

BUSH_WITH_RED_FLOWERS = Object(GARDEN_MAP + 'struik met rode bloemen.png', 0, 335, (205, 425), "Geluidsopnamen/AchterDeStruik.ogg")
BUSH_WITH_WHITE_FLOWERS = Object(GARDEN_MAP + 'struik met witte bloemen.png', 1050, 510, (1110, MAPHEIGHT - 130), "Geluidsopnamen/InDeStruik.ogg")

SANDBOX_BACK = Object(GARDEN_MAP + 'zandbak achter.png', 20, 485)
SANDBOX_FRONT = Object(GARDEN_MAP + 'zandbak voor.png', 15, 465, (275, 515), "Geluidsopnamen/InDeZandbak.ogg")

#Mickey
MICKEY = Mickey()

HEAD = pygame.sprite.Group(Head())
BODY = Object("Mickey staat stil/lichaam stil.png", MAPWIDTH / 2, MAPHEIGHT - 200)
TAIL = pygame.sprite.Group(Tail())

HAMMOCK_MICKEY = Object("Mickey in hangmat.png", HAMMOCK_FRONT.x , HAMMOCK_FRONT.y + HAMMOCK_FRONT.height - 60)#height hammock mickey is +/- 83


#Rooms
BEDROOM_OBJECTS = [BACKGROUND_BEDROOM, WALL_REST, REAR_WALL_CLOSET, CLOSET_CLOSED, FRONT_WALL_CLOSET, TABLE, BED_REAR, PILLOW1, PILLOW2, ELDERDOWN, CURTAIN_RIGHT, CURTAIN_MID_RIGHT, CURTAIN_MID_LEFT, CURTAIN_LEFT, WALL_PART, BEDROOM_DOOR, CHAIR_BACK, CHAIR_FRONT,HAMPER_REAR, HAMPER_LID_CLOSED, HAMPER_FRONT]
HIDING_PLACES_BEDROOM = (FRONT_WALL_CLOSET, CURTAIN_LEFT, CURTAIN_MID_LEFT, CURTAIN_MID_RIGHT, CURTAIN_RIGHT, CHAIR_BACK, CHAIR_FRONT, PILLOW1, PILLOW2, ELDERDOWN, HAMPER_FRONT)
  
BATHROOM_OBJECTS = [BACKGROUND_BATHROOM, BATHROOM_WALLS, BATHROOM_FLOOR, BATH_REAR, TOILET_BATHROOM, BATH_FRONT, STOOL, SINK, TOWEL_FLAT, MAT_FLAT, BATHROOM_WALLPART, BATHROOM_DOOR, Man()]
HIDING_PLACES_BATHROOM = (TOILET_BATHROOM, BATH_FRONT, STOOL, TOWEL_FLAT, MAT_FLAT)

CHILDRENSROOM_OBJECTS = [WALLS_CHILDRENSROOM, BED_BACK, BEAR, Girl(), BED_FRONT, TENT_BACK, TENT_FRONT, TENT_CLOSED, DOLL_WHITE, DOLL_BROWN, BALL, TRAIN, WALLPART_CHILDRENSROOM, CHILDRENSROOM_DOOR, DOLL_CARRIAGE_BACK, LITTLE_CLOSET, DOLL_CARRIAGE_FRONT]
HIDING_PLACES_CHILDRENSROOM = (BEAR, TENT_FRONT, DOLL_WHITE, DOLL_BROWN, BALL, DOLL_CARRIAGE_FRONT, LITTLE_CLOSET)
	
BARN_OBJECTS = [BACKGROUND_BARN, GARBAGE_CAN, RAKE_BROOM_SHOVEL, WHEELBARROW, WORK_TABLE, BICYCLE_BAG_BACK, BAG_FRONT, BAG_FLAP_CLOSED, FOOTBALL, BARN_WALL_PART, BARN_DOOR, BOX_BACK, BOX_FRONT, Rat()]
HIDING_PLACES_BARN = (WHEELBARROW, RAKE_BROOM_SHOVEL, BAG_FRONT, BOX_FRONT, BOX_BACK)
	
TOILET_OBJECTS = [BACKGROUND_TOILET, WALLS_TOILET, TOWEL_FLAT_TOILET, TOILET_CLOSET, TOILET_CLOSET_CLOSED, WALL_PART_TOILET, TOILET_DOOR, TOILET, GARBAGE_CAN_TOILET, TOILET_ROLLS_PILE]
HIDING_PLACES_TOILET = (TOWEL_FLAT_TOILET, TOILET_CLOSET_CLOSED, TOILET, GARBAGE_CAN_TOILET, TOILET_ROLLS_PILE)
	
KITCHEN_OBJECTS = [BACKGROUND_KITCHEN, WALLS_KITCHEN, DRAWER_OPEN_BACK, DRAWER_OPEN_FRONT, CHAIR_YELLOW_LEFT, CHAIR_YELLOW_RIGHT, TABLE_BACK, WALL_PART_KITCHEN, KITCHEN_DOOR, Boy(), TABLE_FRONT, CHAIR_BLUE_LEFT_BACK, CHAIR_BLUE_LEFT_FRONT, CHAIR_BLUE_RIGHT_BACK,  CHAIR_BLUE_RIGHT_FRONT, KITCHEN_PLANT, CASES_BACK, CASES_FRONT]
HIDING_PLACES_KITCHEN = (DRAWER_OPEN_FRONT, CHAIR_BLUE_RIGHT_BACK, CHAIR_BLUE_LEFT_FRONT, CHAIR_BLUE_RIGHT_FRONT, KITCHEN_PLANT, CASES_FRONT)

LIVINGROOM_OBJECTS = [WALLS_LIVING_ROOM, DESK_BACK, BENCH, Cat(), PILLOW_BLUE, PILLOW_GREEN, PILLOW_YELLOW, PILLOW_PURPLE, COFFEE_TABLE_BACK, COFFEE_TABLE_FRONT, OFFICE_CHAIR, DESK_FRONT, CHAIR_RIGHT, Woman(), CHAIR_LEFT, WALL_PART_LIVING_ROOM, LIVING_ROOM_DOOR, PLANT_LIVING_ROOM]
HIDING_PLACES_LIVINGROOM = (DESK_BACK, BENCH, PILLOW_BLUE, OFFICE_CHAIR, DESK_FRONT, CHAIR_LEFT, CHAIR_RIGHT, PLANT_LIVING_ROOM)
	
GARDEN_OBJECTS = [BACKGROUND_GARDEN, Bird(), PLAYHOUSE_BACK, HAMMOCK_BACK, HAMMOCK_FRONT, PLAYHOUSE_FRONT, Bird(), Bird(), TREE, Bird(), Bird(), BUSH_WITH_RED_FLOWERS,  STICK_PARASOL, PARASOL, BEACHCHAIR_BACK, BEACHCHAIR_FRONT, SANDBOX_BACK, SANDBOX_FRONT, WATERING_CAN, GRASS, BUSH_WITH_WHITE_FLOWERS]
HIDING_PLACES_GARDEN = (HAMMOCK_FRONT, PLAYHOUSE_FRONT, TREE, BUSH_WITH_RED_FLOWERS, PARASOL, BEACHCHAIR_BACK, SANDBOX_FRONT, WATERING_CAN, GRASS, BUSH_WITH_WHITE_FLOWERS)


#Colours rooms

BLACK = (0, 0, 0)
TURQUOISE = (0, 150, 150) #sleeping room bathroom
BLUE = (0, 0, 105)
GREY = (75, 75, 75)
INDIGO = (60, 0, 100)
VIOLET = (100, 0, 160)
BROWN = (100, 50, 0)
GREEN = (0, 75, 50)
PINK = (219, 119, 141)
LIGHTPINK = (235, 185, 195)
WHITE = (250, 250, 250)
	
BEDROOM = Room(BEDROOM_OBJECTS, HIDING_PLACES_BEDROOM, BEDROOM_DOOR, DOOR_BEDROOM, TURQUOISE,"Geluidsopnamen/Slaapkamer.ogg")
BATHROOM = Room(BATHROOM_OBJECTS, HIDING_PLACES_BATHROOM, BATHROOM_DOOR, DOOR_BATHROOM, TURQUOISE, "Geluidsopnamen/Badkamer.ogg")
CHILDRENSROOM = Room(CHILDRENSROOM_OBJECTS, HIDING_PLACES_CHILDRENSROOM, CHILDRENSROOM_DOOR, DOOR_CHILDRENSROOM, BLUE, "Geluidsopnamen/Kinderkamer.ogg")
BARN = Room(BARN_OBJECTS, HIDING_PLACES_BARN, BARN_DOOR,  DOOR_BARN, GREY, "Geluidsopnamen/Schuur.ogg")
TOILET = Room(TOILET_OBJECTS, HIDING_PLACES_TOILET, TOILET_DOOR, DOOR_TOILET, INDIGO, "Geluidsopnamen/WC.ogg")
KITCHEN = Room(KITCHEN_OBJECTS, HIDING_PLACES_KITCHEN, KITCHEN_DOOR, DOOR_KITCHEN, VIOLET, "Geluidsopnamen/Eetkamer.ogg")
LIVINGROOM = Room(LIVINGROOM_OBJECTS, HIDING_PLACES_LIVINGROOM, LIVING_ROOM_DOOR, DOOR_LIVING_ROOM, BLUE, "Geluidsopnamen/Zitkamer.ogg")
GARDEN = Room(GARDEN_OBJECTS, HIDING_PLACES_GARDEN, None, DOOR_GARDEN, BROWN,"Geluidsopnamen/Tuin.ogg")

#Texts
WELCOME = pygame.mixer.Sound("Geluidsopnamen/welkom.ogg")
HIDE_AND_SEEK = pygame.mixer.Sound("Geluidsopnamen/verstoppertje.ogg")
MICKEY_WAS = pygame.mixer.Sound("Geluidsopnamen/mickeyZat....ogg")

FOUND = pygame.mixer.Sound("Geluidsopnamen/gevonden.ogg")
WELL_DONE = pygame.mixer.Sound("Geluidsopnamen/HeelGoed.ogg")
JAAA = pygame.mixer.Sound("Geluidsopnamen/Jaaa.ogg")

OPEN_DOOR = pygame.mixer.Sound("Geluidsopnamen/maakEenDeurOpen.ogg")
WHERE_IS_MICKEY = pygame.mixer.Sound("Geluidsopnamen/WaarIsMickey.ogg")
TAIL_NOSE = pygame.mixer.Sound("Geluidsopnamen/staart_neusje.ogg")
HELLO = pygame.mixer.Sound("Geluidsopnamen/HalloDitIsMickey.ogg")


#Chooses the hiding places given some objects to choose between
def chooseHidingPlace(mickey, objects):
	index = random.randint(0, len(objects) - 1)
	
	return objects[index]


#Adjusts the size of the current image, which makes the image shown smaller if the y coordinate is smaller, to make it look like the sprite is smaller when it goes further away. It returns the new image.
def adjustSizeByY(startY, endY):
	
	if MICKEY.y <= endY:
		currentY = endY
	else:
		currentY = MICKEY.y

	if MICKEY.y < startY:
		newWidth = int(MICKEY.image.get_rect().size[0] * currentY / startY)
		newHeight = int(MICKEY.image.get_rect().size[1] * currentY / startY)

		return pygame.transform.scale(MICKEY.image, (newWidth, newHeight)) 

	return MICKEY.image


#Changes the size of a sprite.
def changeSizesByY(startY, endY):

	if MICKEY.y <= endY:
		currentY = endY
	else:
		currentY = MICKEY.y

	if MICKEY.y < startY:
		newWidth = MICKEY.image.get_rect().size[0] * currentY / startY
		newHeight = MICKEY.image.get_rect().size[1] * currentY / startY

		return newWidth, newHeight

	return MICKEY.width, MICKEY.height


#Makes the image of a sprite a given fraction larger
def adjustSize(fraction):
	newWidth = MICKEY.image.get_rect().size[0] + MICKEY.image.get_rect().size[0] / fraction
	newHeight = MICKEY.image.get_rect().size[1] + MICKEY.image.get_rect().size[1] / fraction

	return pygame.transform.scale(MICKEY.image, (newWidth, newHeight))


def showPath():
	X_COORDINATES.append(int(MICKEY.x))
	Y_COORDINATES.append(int(MICKEY.y))

	for i in range(len(X_COORDINATES)):
		pygame.draw.circle(DISPLAYSURF, (100, 0, 0), (X_COORDINATES[i], Y_COORDINATES[i]), 5)
	return

	
#Draws the current image of mickeys given the sprite group, the sprite, and the objects drawn around Mickey (which are needed to see in which room Mickey is at the moment.
def drawMickey(mickey, objects):
	#If you applied the size changes incrementally to the previous images, you would lose detail. Instead, always begin with the original image and scale to the desired size.
	
	if objects[0] == BACKGROUND_TOILET:
		image = adjustSize(6)

		DISPLAYSURF.blit(image, (MICKEY.x, MICKEY.y))

	elif (objects[0] == FLOOR or objects[0] == BACKGROUND_GARDEN) and MICKEY.y < MAPHEIGHT - 200: #FLOOR is the first objects in the hallList
		image = adjustSizeByY(MAPHEIGHT - 200, FLOOR.y) #MAPHEIGHT - 200 is the place where mickey always starts in the hall

		DISPLAYSURF.blit(image, (MICKEY.x, MICKEY.y))
	else:
		mickey.draw(DISPLAYSURF)

	if SHOW_PATH:
		showPath()
	return 


def openDoor(door):
	x = door.x
	y = door.y

	if door.x >= DOOR_GARDEN.x:
		x = door.x + door.width / 2

	#door.opened = True
	image = pygame.transform.scale(door.image, (door.width / 2 + 1, door.height))
			
	DISPLAYSURF.blit(image, (x, y))
	return


def defineDirectionSprite(door):

	if door.x <= DOOR_GARDEN.x:
		return VELOCITY_MICKEY * -1
	else:
		return VELOCITY_MICKEY


def defineMoveParameters(door, sprite):
	doorPlace = door.y + door.height - 25
	doorMarge = door.width + 10
	delay = 3
	xAlpha = defineDirectionSprite(door)
	yAlpha = 0
	action = None
	marge = 134 / 2 + 13 #Start height of Mickey. Mickey's height has to be the same every time, because the difference with the door tells in which direction Mickey runs.
	
	if MICKEY.y + marge < doorPlace - VELOCITY_MICKEY:
		xAlpha -= delay
		yAlpha = delay
		action = "coming"
		
		if abs(door.x - MICKEY.x) < doorMarge:
			xAlpha = 0

	elif MICKEY.y + marge > doorPlace + VELOCITY_MICKEY:
		xAlpha += delay
		yAlpha = -delay
		action = "going"
		
		if abs(door.x - MICKEY.x) < doorMarge:
			xAlpha = 0

	return xAlpha, yAlpha, action


def drawDoor(door, wallPart):
	DISPLAYSURF.blit(wallPart.image, (wallPart.x, wallPart.y))

	#Because the door images in the hall can open, they are door instances. The room doors are always drawn open, so I made these instances of the class object and not of the class door.
	if door.__class__.__name__ == "Door":
		openDoor(door)	
	else:
		DISPLAYSURF.blit(door.image, (door.x, door.y))
	return
		


#Lets the sprite move in the direction of the door, given the sprite group, the sprite, the door (object or door class), and the list of objects of the current room.
def runThroughDoor(mickey, door, objects):
	xAlpha, yAlpha, action = defineMoveParameters(door, mickey.sprites()[0])
	
	mickey.update(xAlpha, yAlpha, action)
	
	if door.__class__.__name__ == "Door":#Which means that mickey is in the hall
		if MICKEY.y < MAPHEIGHT - 200:	
			MICKEY.width, MICKEY.height = changeSizesByY(MAPHEIGHT - 200, FLOOR.y)#The place in the hall where Mickey is drawn first is given as star

	drawMickey(mickey, objects)
	return


def leaveScreen(mickey, objects):
	velocityDiagonal = 3

	if MICKEY.x < MAPWIDTH / 2 - VELOCITY_MICKEY:
		xAlpha = velocityDiagonal
		yAlpha = velocityDiagonal

	elif MICKEY.x > MAPWIDTH / 2 - VELOCITY_MICKEY:
		xAlpha = -velocityDiagonal
		yAlpha = velocityDiagonal
		
	else:
		xAlpha = 0
		yAlpha = VELOCITY_MICKEY
	
	mickey.update(xAlpha, yAlpha, "coming")
	drawMickey(mickey, objects)
	
	return

def drawMickeyStanding():
	TAIL.draw(DISPLAYSURF)
	DISPLAYSURF.blit(BODY.image, (BODY.x, BODY.y))
	HEAD.draw(DISPLAYSURF)

	return


def wagTail(direction = 1):

	for i in range(4):
		TAIL.update(direction)
		drawMickeyStanding()
		clock.tick(FPS)
		pygame.display.update()
	return
	
def updatePic():
	lookAround = random.choice([True, False])
	wag = random.choice([True, False])

	if lookAround:
		HEAD.update()

	if wag:
		wagTail()
		wagTail(-1)	
	return
	


def stand():
	HEAD.sprites()[0].place(BODY.x - HEAD.sprites()[0].width/2 + 8, BODY.y - HEAD.sprites()[0].height / 2 - 2)
	TAIL.sprites()[0].place(BODY.x + BODY.width - TAIL.sprites()[0].width / 2 - 5, BODY.y - TAIL.sprites()[0].height / 2)	
	updatePic()
	drawMickeyStanding()		
	return


def putMickeyInImage(mickey, objects, hidingPlace):

	if hidingPlace == HAMMOCK_FRONT and MICKEY.found == False:
		DISPLAYSURF.blit(HAMMOCK_MICKEY.image, (HAMMOCK_MICKEY.x, HAMMOCK_MICKEY.y))
	else:	
		drawMickey(mickey, objects)
	return


#Displays the objects and Mickey in the first room, while the sprite does not do any action yet, given the sprite group, the sprite, the objects of the current room, and the hidingPlace as an optional parameter.
def drawImage(mickey, objects, hidingPlace = None):

	if hidingPlace:
		if objects == GARDEN.objects:
			DISPLAYSURF.fill(GREEN)

		draw(objects[:objects.index(hidingPlace)])		
		putMickeyInImage(mickey, objects, hidingPlace)
		draw(objects[objects.index(hidingPlace):])
	else:

		#This is the start position in the hall
		draw(objects)
		stand()

	return


#Plays a look to shown all images of Mickey when he moves through a door, given the sprite group, the sprite, the objects of the room and the door (Object or Door class). 
def leaveRoom(mickey, objects, door, backgroundColour = None):

	while MICKEY.x >= 0 - VELOCITY_MICKEY and MICKEY.x <= MAPWIDTH + VELOCITY_MICKEY:
		#The index of the wall part around the door is needed, because the sprite of mickey has to run behind this wallpart. The wallpart is drawn earlier than the door for optical reasons. For this reason, everything until the wall part has to be drawn before the sprite of mickey is placed.

		wallPartindex = objects.index(door) - 1

		if backgroundColour:			
			DISPLAYSURF.fill(backgroundColour)

		draw(objects[:wallPartindex])
		runThroughDoor(mickey, door, objects)
		drawDoor(door, objects[wallPartindex])
		draw(objects[objects.index(door) + 1:])

		clock.tick(FPS)
		pygame.display.update()	
	return


#Verifies whether a given object (o) is selected, with the given mouse position. Return a boolean value.
def selectObject(o, mousePosition):
	objectRectFound = o.image.get_rect(topleft=(o.x, o.y))

	if objectRectFound.collidepoint(mousePosition):
		return True

	return False


#Returns the selected Door object, given a list of objects and the mouse position.
def selectDoor(objects, mousePosition):

	for o in objects:
		if isinstance(o, Door):
			doorRect = o.image.get_rect(topleft=(o.x, o.y))

			if doorRect.collidepoint(mousePosition):
				return o

				
def showRat(rat, objects):
		
	rat.update()
	DISPLAYSURF.blit(rat.image, (rat.x, rat.y))
	return

	
def showBird(bird):
	bird.fly()	
	DISPLAYSURF.blit(bird.image, (bird.x, bird.y)) #The group is drawn by this function
 	return

	
def showCat(cat):
	moving = random.choice([True, False])
	
	if moving:
		cat.moveTail()
		
	DISPLAYSURF.blit(cat.tail, (cat.x + cat.width - cat.tailWidth, cat.y + cat.height - 12))
	DISPLAYSURF.blit(cat.body, (cat.x, cat.y))	
	
	return
	
def showWoman(woman):
	changeScreen = random.randint(1, 10)
	
	if changeScreen == 10:
		woman.changeScreen()
		
	DISPLAYSURF.blit(woman.body, (woman.x, woman.y))
	DISPLAYSURF.blit(woman.screen, (woman.x + 85, woman.y + 75))
	DISPLAYSURF.blit(woman.thumb, (woman.x + 85, woman.y + 95))	
	return
	
	
def showGirl(girl):
	changePage = 20
	sheetWidth = girl.sheet.get_rect().size[0]
	
	if int(girl.index) == 4:
		changePage = random.randint(1, 20)

	if changePage == 20 and int(girl.index) <= len(girl.sheetImages):
		girl.movePage()
	
	DISPLAYSURF.blit(girl.body, (girl.x, girl.y))
	DISPLAYSURF.blit(girl.sheet, (girl.x + 143 - sheetWidth, girl.y + girl.height / 2 - 25))		
	DISPLAYSURF.blit(girl.handAndFeet, (girl.x + girl.width / 4 - 18, girl.y + girl.height / 2 + 20))
	
	return

	
def showBoy(boy):	
	DISPLAYSURF.blit(boy.body, (boy.x, boy.y))
	DISPLAYSURF.blit(TABLE_FRONT.image, (TABLE_FRONT.x, TABLE_FRONT.y))
	DISPLAYSURF.blit(boy.handRest, (boy.x + boy.width - 48, TABLE_FRONT.y + 58))
	
	boy.munch()
	
	return


def showMan(man):
        DISPLAYSURF.blit(man.head, (man.x + man.width - 125, man.y + 90))
        man.comb()
        DISPLAYSURF.blit(man.body, (man.x, man.y))
        
        return

	
def draw(objects):

	for o in objects:
		if o.__class__.__name__ == "Bird":
			showBird(o)
		elif o.__class__.__name__ == "Rat":
			showRat(o, objects)
		elif o.__class__.__name__ == "Cat":
			showCat(o)
		elif o.__class__.__name__ == "Woman":
			showWoman(o)
		elif o.__class__.__name__ == "Girl":
			showGirl(o)
		elif o.__class__.__name__ == "Boy":
			showBoy(o)
                elif o.__class__.__name__ == "Man":
			showMan(o)                
		elif o != TABLE_FRONT:#Already drawn in showBoy()
			DISPLAYSURF.blit(o.image, (o.x, o.y))
	return


#I used Numpy to make the calculations for Mickey's slide. Because the dependencies of the numpy library took a lot of space, I calculated these values in another script, CalcYSlide.py, which is not included in de folder.			   
def retrieveYValuesSlide():

	return [165, 165.0, 163.28206422099083, 163.06120258557894, 164.23683364620229, 166.70837595529883, 170.37524806531292, 175.13686852867522, 180.8926558978228, 187.54202872519727, 194.98440556323658, 203.11920496437688, 211.84584548105158, 221.06374566570594, 230.6723240707688, 240.57099924869, 250.65918975189197, 260.8363141328273, 271.00179094391933, 281.0550387376197, 290.8954760663546, 300.4225214825674, 309.53559353869605, 318.1341107871749, 326.11749178044374, 333.3851550709387, 339.8365192110996, 345.3710027533634, 349.8880242501691, 353.28700225394823, 355.4673553171451]


def slide(mickey, objects, hidingPlace, startX, startY):
	endX = hidingPlace.x - MICKEY.width
	endY = hidingPlace.y + hidingPlace.height - MICKEY.height + 10
	slopeStart = 0.25
	slopeEnd = 0.1
	deltaX = - 10
	yValues = retrieveYValuesSlide()
	y = startY
	slideVelocity = 20 #FPS
	i = 0

	MICKEY.place(startX, startY)

	for x in range(startX, endX - deltaX, deltaX):
		deltaY = yValues[i] - y
		y = yValues[i]
		
		slideVelocity += 10
		move(mickey, objects, objects[objects.index(hidingPlace) + 1], deltaX, deltaY, "slide")
		clock.tick(slideVelocity)
		pygame.display.update()
		
		if i != len(yValues) - 1:
                        i += 1

	MICKEY.x = int(MICKEY.x)
	MICKEY.y = int(MICKEY.y)

	return


#Calculates the a, b, and c values to calculate a parabola, given the x and y values for the start coordinates(1), highest point(2), and end coordinates(3).
def calcParabolaABC(x1, y1, x2, y2, x3, y3):
		nom = (x1-x2) * (x1-x3) * (x2-x3)

		a = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / nom
		b = (x3 * x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / nom
		c = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / nom

		return a,b,c


#Calculates the y value given a x-value, a value, b value, and c value.
def calcYJump(x, a, b, c):
	return a * x**2 + b * x + c


def move(mickey, objects, hidingPlace, deltaX, deltaY, action):
	mickey.update(deltaX, deltaY, action)
	drawImage(mickey, objects, hidingPlace)

	return
	
	
def floatRange(start, end, step):
	result = []
	x = start
	
	while abs(end - x) >= abs(step):
		yield x
		x += step


def jumpOver(objects, hidingPlace):                                                
        if hidingPlace == BEAR:
               return objects[objects.index(BED_FRONT) + 1]
        
        return objects[objects.index(hidingPlace) + 1]


#Lets the sprite move in the form of a parabola, with the correct images to jump, hiven the sprite group, the sprite, the objects of the current room, the object where the sprite was hided, and the values of three points in the parabola.
def jump(mickey, objects, hidingPlace, x1, y1, x2, y2, x3, y3):
	MICKEY.index = 0
	finalY = BED_REAR.y + BED_REAR.height
	numberOfJumpImages = 12
	deltaX = (x3 - x1) / (numberOfJumpImages - 1)
	y = y1
	jumpVelocity = 20 #FPS
	#The images for jumping are a little bit smaller than for walking, and Mickey always lowers a little when he starts jumping. Because of this, I make the y of Mickey a little bit higher before he starts jumping.
	MICKEY.y -= 20
	a,b,c = calcParabolaABC(x1, y1, x2, y2, x3, y3)

	for x in list(floatRange(x1, x3 + deltaX, deltaX)):
		deltaY = calcYJump(x, a, b, c) - y
		y = calcYJump(x, a, b, c)
			
		move(mickey, objects, hidingPlace, deltaX, deltaY, "jump")
		clock.tick(jumpVelocity)
		pygame.display.update()
		
                if hidingPlace == BATH_FRONT or hidingPlace == DRAWER_OPEN_FRONT or hidingPlace == BEAR:
                        if x3 < x1 and x2 > x:        
                                hidingPlace = jumpOver(objects, hidingPlace)
                                                                              
	MICKEY.x = int(MICKEY.x)
	MICKEY.y = int(MICKEY.y)
	return	


#Changes the an objects designated as hiding place with another objects, It returns directly the new object. It is used for example to change towel flat, when Mickey is not hided here, to towel wide. The parameters are the list of the objects of the current room, mikcey's hiding place, and the new layout for the hiding place.
def changeLayoutHidingPlace(objects, hidingPlace, newLayout):
	if hidingPlace in objects:
		objects[objects.index(hidingPlace)] = newLayout

	return newLayout


#Moves to Mickey sprite to a particular x coordinate, given the sprite groupl, the sprite, the objects of the current room, the hiding place, the end x, and thhe velocity in frames per second.
def walk(mickey, objects, hidingPlace, end):

	if MICKEY.x < end:
		velocity = VELOCITY_MICKEY
	else:
		velocity = VELOCITY_MICKEY * -1

	while abs(MICKEY.x - end) > abs(velocity):
		mickey.update(velocity, 0)
		drawImage(mickey, objects, hidingPlace)
		clock.tick(FPS)
		pygame.display.update()
	return


def jumpOutOfBed(mickey, objects, hidingPlace, startX, startY, marge):

	if hidingPlace == BEAR:
		topX = startX - 10
		topY = BED_FRONT.y - MICKEY.height
		endX = startX - 20
		endY = CHILDRENSROOM_DOOR.y + CHILDRENSROOM_DOOR.height - MICKEY.height

	else:
		topX = ELDERDOWN.x
		topY = ELDERDOWN.y - 10
		endX = BED_REAR.x - MICKEY.width
		
		if hidingPlace == PILLOW2:
			endY = BEDROOM_DOOR.y + BEDROOM_DOOR.height - MICKEY.height + 50
		else:		
			endY = BEDROOM_DOOR.y + BEDROOM_DOOR.height - MICKEY.height

	if DOG_UNDER_ELDERDOWN in objects:
		objects.remove(DOG_UNDER_ELDERDOWN)

		hidingPlace = ELDERDOWN

	jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	return


def calcTopXRight(hidingPlace):
	if hidingPlace.x + hidingPlace.width <= MICKEY.x or hidingPlace == GRASS: 
		return MICKEY.x + 10

	if hidingPlace == TREE or hidingPlace == GRASS:
		return MICKEY.x + (MICKEY.x - hidingPlace.x) / 2 	
		
	return hidingPlace.x + hidingPlace.width


def calcTopYRight(hidingPlace):
	if hidingPlace == TREE:
		return TREE.y + TREE.height / 2

	elif hidingPlace == TOILET_CLOSET_OPEN or hidingPlace == HAMMOCK_FRONT or hidingPlace == CHAIR_BLUE_RIGHT_FRONT:
		return MICKEY.y - 10
	
	elif hidingPlace == GRASS:
		return hidingPlace.y - MICKEY.height - 10

	return hidingPlace.y - MICKEY.height - 50


def calcEndXRight(hidingPlace):

	if hidingPlace == TREE:
		return	hidingPlace.x + hidingPlace.width

	elif hidingPlace == CHAIR_RIGHT:
		return LIVING_ROOM_DOOR.x - MICKEY.width - 10	

	elif hidingPlace == SANDBOX_FRONT:
		return MAPWIDTH / 2

	elif hidingPlace == GRASS:
		return MICKEY.x + 20
			
	elif hidingPlace == DOLL_BROWN:
		return hidingPlace.x + hidingPlace.width * 3

	return hidingPlace.x + hidingPlace.width * 2


def calcEndYRight(hidingPlace):	
	if hidingPlace == BAG_FRONT:
		return BICYCLE_BAG_BACK.y + BICYCLE_BAG_BACK.height - MICKEY.height

	elif hidingPlace == TREE or hidingPlace == HAMMOCK_FRONT:
		return TREE.y + TREE.height - 100

	elif hidingPlace == CHAIR_BLUE_RIGHT_FRONT:
		return CHAIR_BLUE_RIGHT_BACK.y + CHAIR_BLUE_RIGHT_BACK.height - MICKEY.height

	elif hidingPlace == PILLOW_BLUE:
		return COFFEE_TABLE_BACK.y + COFFEE_TABLE_BACK.height - MICKEY.height + 50
		
	elif hidingPlace == GRASS:
		return WATERING_CAN.y + WATERING_CAN.height - MICKEY.height - 5
		
	elif hidingPlace == CHAIR_LEFT:
		return CHAIR_RIGHT.y + CHAIR_RIGHT.height + 50

	else:
		return hidingPlace.y + hidingPlace.height - MICKEY.height + 50


def jumpToTheRight(mickey, objects, hidingPlace, startX, startY, marge):
	topX = calcTopXRight(hidingPlace)
	topY = calcTopYRight(hidingPlace)
	endX = calcEndXRight(hidingPlace)
	endY = calcEndYRight(hidingPlace)

	jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	if hidingPlace == BAG_FRONT:
		objects[objects.index(BAG_FLAP_OPEN)] = BAG_FLAP_ALMOST_CLOSED
	return


def calcTopXLeft(objects, hidingPlace):

	if hidingPlace == PLAYHOUSE_FRONT or hidingPlace == OFFICE_CHAIR or hidingPlace == WHEELBARROW or hidingPlace == CHAIR_BLUE_LEFT_FRONT:
		return MICKEY.x - 10

	elif hidingPlace == BATH_FRONT:
		return MICKEY.x - ((MICKEY.x - BATH_FRONT.x) / 2)
		
	return hidingPlace.x - MICKEY.width


def calcTopYLeft(objects, hidingPlace):

	if hidingPlace == PLAYHOUSE_FRONT or hidingPlace == CASES_FRONT or hidingPlace == OFFICE_CHAIR or hidingPlace == WHEELBARROW or hidingPlace == CHAIR_BLUE_LEFT_FRONT:

		return MICKEY.y - 10		

	return hidingPlace.y - MICKEY.height


def calcEndXLeft(objects, hidingPlace):
	if hidingPlace == DRAWER_OPEN_FRONT:
		return MAPWIDTH / 2

	elif hidingPlace == PLAYHOUSE_FRONT:
		return 910 #Estimated as the correct place just by selecting the place in the example image of the garden.
	
	elif hidingPlace == OFFICE_CHAIR or hidingPlace == WHEELBARROW or hidingPlace == CHAIR_BLUE_LEFT_FRONT:
		return hidingPlace.x - MICKEY.width + 10

	elif hidingPlace == BATH_FRONT: 		
		return BATH_FRONT.x

	return hidingPlace.x - (MICKEY.width * 2)


def calcEndYLeft(objects, hidingPlace, topY):

	if hidingPlace == PILLOW_BLUE:
		return BENCH.y + BENCH.height - MICKEY.height

	elif hidingPlace == CHAIR_FRONT or hidingPlace == CHAIR_BLUE_LEFT_FRONT:
		return  objects[objects.index(hidingPlace) - 1].y + objects[objects.index(hidingPlace) - 1].height - MICKEY.height

	elif hidingPlace == PLAYHOUSE_FRONT:
		return 200 - MICKEY.height
	
	elif hidingPlace == WHEELBARROW:
		return RAKE_BROOM_SHOVEL.y + RAKE_BROOM_SHOVEL.height

	return hidingPlace.y + hidingPlace.height - MICKEY.height


def jumpToTheLeft(mickey, objects, hidingPlace, startX, startY):
	topX = calcTopXLeft(objects, hidingPlace)
	topY = calcTopYLeft(objects, hidingPlace)
	endX = calcEndXLeft(objects, hidingPlace)
	endY = calcEndYLeft(objects, hidingPlace, topY)

	jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	return


#Verifies whether the jump funcion needs to be used and initializes it when needed, given the sprite group, the sprite, the objects in the room, the hiding place, the cx and y coordinates of the place where the sprite starts moving.
def jumpWhenNeeded(mickey, objects, hidingPlace, startX, startY):
	marge = 10

	if hidingPlace == DOG_UNDER_ELDERDOWN or hidingPlace == PILLOW1 or hidingPlace == PILLOW2 or hidingPlace == BEAR:
		jumpOutOfBed(mickey, objects, hidingPlace, startX, startY, marge)

	elif hidingPlace == HAMPER_FRONT or hidingPlace == DOLL_CARRIAGE_FRONT or hidingPlace == BOX_FRONT or hidingPlace == DOLL_BROWN or hidingPlace == BAG_FRONT or hidingPlace == CHAIR_LEFT or hidingPlace == CHAIR_RIGHT or hidingPlace == PLANT_LIVING_ROOM or hidingPlace == HAMMOCK_FRONT or hidingPlace == TREE or hidingPlace == TOILET_CLOSET_OPEN or hidingPlace == CHAIR_BLUE_RIGHT_FRONT or hidingPlace == SANDBOX_FRONT or hidingPlace == BEACHCHAIR_FRONT or hidingPlace == PILLOW_BLUE or hidingPlace == GRASS:
		jumpToTheRight(mickey, objects, hidingPlace, startX, startY, marge)

	elif hidingPlace == DRAWER_OPEN_FRONT or hidingPlace == WHEELBARROW or hidingPlace == CASES_FRONT or hidingPlace == OFFICE_CHAIR or hidingPlace == BATH_FRONT or hidingPlace == CHAIR_FRONT or hidingPlace == CHAIR_BLUE_LEFT_FRONT or hidingPlace == BUSH_WITH_WHITE_FLOWERS or hidingPlace == PLAYHOUSE_FRONT:
		jumpToTheLeft(mickey, objects, hidingPlace, startX, startY)
	return


def comeOut(mickey, objects, hidingPlace, startX, startY):
	marge = 100	
	
	jumpWhenNeeded(mickey, objects, hidingPlace, startX, startY)

	if hidingPlace == CURTAIN_LEFT or hidingPlace == CURTAIN_RIGHT or hidingPlace == CURTAIN_MID_RIGHT or hidingPlace == CURTAIN_MID_LEFT or hidingPlace == DESK_FRONT:
		walk(mickey, objects, hidingPlace, hidingPlace.x - marge + 10)

	elif hidingPlace == DESK_BACK:
		walk(mickey, objects, hidingPlace, hidingPlace.x - marge - 40)	
			
	elif hidingPlace == DOLL_WHITE:	
		walk(mickey, objects, hidingPlace, DOLL_WHITE.x + DOLL_WHITE.width + 60)
		#I have put 10 pixels extra by the marge, because otherwise mickey runs partly under the foot of the brown doll.	

	elif hidingPlace == FRONT_WALL_CLOSET:
		walk(mickey, objects, hidingPlace, hidingPlace.x + hidingPlace.width + 10)

	elif hidingPlace == RAKE_BROOM_SHOVEL:
		walk(mickey, objects, hidingPlace, hidingPlace.x + hidingPlace.width)

	elif hidingPlace == STOOL or hidingPlace == BALL or hidingPlace == LITTLE_CLOSET:
		walk(mickey, objects, hidingPlace, hidingPlace.x - marge)
	
	elif hidingPlace == GARBAGE_CAN_TOILET:
		walk(mickey, objects, hidingPlace, hidingPlace.x - marge - TOILET_DOOR.width)

	elif hidingPlace == CASES_FRONT:
		walk(mickey, objects, hidingPlace, CASES_FRONT.x - KITCHEN_DOOR.width - MICKEY.width)

	elif hidingPlace == BENCH or hidingPlace == PILLOW_BLUE:

		if hidingPlace == BENCH:
			MICKEY.place(MICKEY.x, BENCH.y + BENCH.height - MICKEY.height)

		walk(mickey, objects, COFFEE_TABLE_BACK, DESK_BACK.x - marge - 40)

	elif hidingPlace == PLAYHOUSE_FRONT:
		slide(mickey, objects, hidingPlace, 900, 245 - MICKEY.height)
	return


def leaveGarden(mickey, hidingPlace):
	
	if hidingPlace == PLAYHOUSE_FRONT:
		hidingPlace = GARDEN.objects[GARDEN.objects.index(hidingPlace) + 1]

	elif hidingPlace == GRASS:
		hidingPlace = GARDEN.objects[GARDEN.objects.index(hidingPlace) - 1]

	while MICKEY.y < PLAYHOUSE_FRONT.y + PLAYHOUSE_FRONT.height:
		move(mickey, GARDEN.objects, hidingPlace, 0, VELOCITY_MICKEY, "coming")
		clock.tick(FPS)
		pygame.display.update()

	walk(mickey, GARDEN.objects, hidingPlace, MAPWIDTH + VELOCITY_MICKEY) #Adding the velocity lets Mickeys walk until the end of the screen, which is needed to go to the hall.

	return


def hideAndSeek(mickey, hidingPlace, room):
	#default jump values, little jump
	startX = MICKEY.x
	startY = MICKEY.y
	topX = MICKEY.x + 5
	topY = MICKEY.y - 5
	endX = MICKEY.x + 10
	endY = MICKEY.y + 10
		
	if MICKEY.found:			

		if hidingPlace == TOWEL_WIDE:
			hidingPlace = changeLayoutHidingPlace(room.objects, TOWEL_WIDE, TOWEL_FLAT)

		elif hidingPlace == TOWEL_WIDE_TOILET:
			hidingPlace = changeLayoutHidingPlace(room.objects, TOWEL_WIDE_TOILET, TOWEL_FLAT_TOILET) 

		elif hidingPlace == MAT_HUMP:
			hidingPlace = changeLayoutHidingPlace(room.objects, MAT_HUMP, MAT_FLAT)

			jump(mickey, room.objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

		elif hidingPlace == TOILET_CLOSET_CLOSED:
			hidingPlace = changeLayoutHidingPlace(room.objects, TOILET_CLOSET_CLOSED, TOILET_CLOSET_OPEN)

		comeOut(mickey, room.objects, hidingPlace, startX, startY)
		
		if room.doorIn == None:
			leaveGarden(mickey, hidingPlace)
		else:
			leaveRoom(mickey, room.objects, room.doorIn)
	else:

		if hidingPlace == TOILET_CLOSET_CLOSED and TOILET_CLOSET_OPEN in room.objects:
			hidingPlace = TOILET_CLOSET_OPEN
			
		drawImage(mickey, room.objects, hidingPlace)
	return


def checkMouseClick(hidingPlace, objects, objectsClosed = [], objectsOpen = [], hidingPlaceObjectsClosed = []):

	for i in range(len(objectsClosed)):
		if objectsClosed[i] in objects:
			if selectObject(objectsClosed[i], pygame.mouse.get_pos()):
				objects[objects.index(objectsClosed[i])] = objectsOpen[i]
						
				if hidingPlace == hidingPlaceObjectsClosed[i]:
					return True

	return selectObject(MICKEY, pygame.mouse.get_pos())


def chooseBox():
	boxes = ["blue box", "red box", "yellow box"]
	boxToHide = random.choice(boxes)

	if boxToHide == "blue box":
		return (1163, 290)
	elif boxToHide == "red box":
		return (1160, 440)
	else:
		return (1165, 580)


def prepare(mickey, objects, possibleHidingplaces, objectsToCheck = [], resetValues = [], layoutNoHiding = [], layoutHiding = []):

	for i in range(len(objectsToCheck)):
		if objectsToCheck[i] in objects:
			objects[objects.index(objectsToCheck[i])] = resetValues[i]

	hidingPlace = chooseHidingPlace(mickey, possibleHidingplaces)

	for i in range(len(layoutNoHiding)):
		if layoutNoHiding[i] == hidingPlace:
			hidingPlace = changeLayoutHidingPlace(objects, layoutNoHiding[i], layoutHiding[i])		
	
	if hidingPlace == ELDERDOWN:
		hidingPlace = DOG_UNDER_ELDERDOWN

		objects.insert(objects.index(ELDERDOWN), DOG_UNDER_ELDERDOWN)

	if hidingPlace == CASES_FRONT:
		hidingPlace.hidingCoordinates = chooseBox()

	return hidingPlace


def findMickey(door, hidingPlace):

	if door == DOOR_BEDROOM:
		return checkMouseClick(hidingPlace, BEDROOM.objects, [CLOSET_CLOSED, HAMPER_LID_CLOSED], [CLOSET_OPEN, HAMPER_LID_OPEN], [FRONT_WALL_CLOSET, HAMPER_FRONT])

	elif door == DOOR_BATHROOM:
		return checkMouseClick(hidingPlace, BATHROOM.objects)

	elif door == DOOR_CHILDRENSROOM:
		return checkMouseClick(hidingPlace, CHILDRENSROOM.objects, [TENT_CLOSED], [TENT_OPEN], [TENT_FRONT])
	
	elif door == DOOR_BARN:
		return checkMouseClick(hidingPlace, BARN.objects, [BAG_FLAP_CLOSED], [BAG_FLAP_OPEN], [BAG_FRONT])

	elif door == DOOR_TOILET:
		return checkMouseClick(hidingPlace, TOILET.objects, [TOILET_CLOSET_CLOSED, TOILET_ROLLS_PILE], [TOILET_CLOSET_OPEN, TOILET_ROLLS_MASS], [TOILET_CLOSET_CLOSED, TOILET_ROLLS_PILE])

	elif door == DOOR_KITCHEN:
		return checkMouseClick(hidingPlace, KITCHEN.objects)

	elif door == DOOR_LIVING_ROOM:
		return checkMouseClick(hidingPlace, LIVINGROOM.objects)

	elif door == DOOR_GARDEN:
		return checkMouseClick(hidingPlace, GARDEN.objects)
		
	else:
		sys.exit()


#Displays a room with the correct objects and the sprite.
def displayRoom(mickey, door, hidingPlace, rooms):

	for room in rooms:
		if door == room.doorOut:
			hideAndSeek(mickey, hidingPlace, room)
			return


#Assigns a hiding place for mickey given all the objects, choosing the correct objects for the correct rooms.			
def assignHidingPlace(mickey, door):

	if door == DOOR_BEDROOM:					
		return prepare(mickey, BEDROOM.objects, BEDROOM.hidingPlaces, [CLOSET_OPEN, HAMPER_LID_OPEN], [CLOSET_CLOSED, HAMPER_LID_CLOSED])

	elif door == DOOR_BATHROOM:			
		HIDING_PLACES_BATHROOM = TOILET_CLOSET_CLOSED, #(TOILET_BATHROOM, BATH_FRONT, STOOL, TOWEL_FLAT, MAT_FLAT)

		return prepare(mickey, BATHROOM.objects, BATHROOM.hidingPlaces, [], [], [TOWEL_FLAT, MAT_FLAT], [TOWEL_WIDE, MAT_HUMP])

	elif door == DOOR_CHILDRENSROOM:
		
		return prepare(mickey, CHILDRENSROOM.objects, CHILDRENSROOM.hidingPlaces, [TENT_OPEN], [TENT_CLOSED])

	elif door == DOOR_BARN:

		return prepare(mickey, BARN.objects, BARN.hidingPlaces, [BAG_FLAP_ALMOST_CLOSED], [BAG_FLAP_CLOSED])

	elif door == DOOR_TOILET:

		return prepare(mickey, TOILET.objects, TOILET.hidingPlaces, [TOILET_CLOSET_OPEN, TOILET_ROLLS_MASS], [TOILET_CLOSET_CLOSED, TOILET_ROLLS_PILE], [TOWEL_FLAT_TOILET], [TOWEL_WIDE_TOILET])

	elif door == DOOR_KITCHEN:

		return prepare(mickey, KITCHEN.objects, KITCHEN.hidingPlaces)

	elif door == DOOR_LIVING_ROOM:

		return prepare(mickey, LIVINGROOM.objects, LIVINGROOM.hidingPlaces)

	elif door == DOOR_GARDEN:

		return prepare(mickey, GARDEN.objects, GARDEN.hidingPlaces)

	return "Not in room!"
	

def resetParameters(inRoom, door, textPlayed):
	MICKEY.reset()

	if inRoom:
		inRoom = False
		MICKEY.found = False
		hidingPlace = None
		door = None
		textPlayed = True				
	else:
		inRoom = True
		
	return inRoom, door, textPlayed


def playTextsOnce(texts):
	if CHANNEL.get_sound() == None:
		texts[0].play()

	for i in range(len(texts) - 1):
			
		if CHANNEL.get_sound() == texts[i]:
			CHANNEL.queue(texts[i + 1])
	

	if CHANNEL.get_sound() == texts[len(texts) - 1]:
		return True

	return False


def search(door, hidingPlace):
	MICKEY.found = findMickey(door, hidingPlace)

	if MICKEY.found:
		compliment = random.randint(1, 8)

		pygame.mixer.stop()
		
		if compliment == 8:
			text = random.choice([FOUND, WELL_DONE, JAAA])
			textPlayed = playTextsOnce([text, hidingPlace.text])			
		else:		
			textPlayed = playTextsOnce([hidingPlace.text])
	return


def displayHall(mickey, hallObjects, rooms, door):
	colour = None

	if door:
		for room in rooms:
			if room.doorOut == door:
				colour = room.colour

		leaveRoom(mickey, hallObjects, door, colour)
		
	else:
		drawImage(mickey, hallObjects)
	return


def hideMickey(hidingPlace):
	
	if hidingPlace.hidingCoordinates:
		MICKEY.place(hidingPlace.hidingCoordinates[0], hidingPlace.hidingCoordinates[1])
	else:
		MICKEY.place(hidingPlace.x, hidingPlace.y + hidingPlace.height - MICKEY.image.get_rect().size[1] - 20)
		#Because mickey stands behind the objects, the y coordinaat has to be a little bit lower than the coodinate of the object
	return


def setStartTextRoom(rooms, hidingPlace):
	
	for room in rooms:
		if hidingPlace in room.objects:
			if room.playText:
				room.playText = False

				return [room.text, WHERE_IS_MICKEY], False
			else:
				return [], True

				
def setButtonColours(intro):
	if intro:
		return PINK, INDIGO
	else:
		return LIGHTPINK, WHITE

		
def drawStartButton(size, intro):
	buttonColour, textColour = setButtonColours(intro)	
	font = pygame.font.Font("Roboto-Regular.ttf", 13)
	label = font.render("START", 1, textColour)
	x = MAPWIDTH / 2
	y = MAPHEIGHT / 2 + 22
					
	pygame.draw.circle(DISPLAYSURF, buttonColour, (x, y), size)
	DISPLAYSURF.blit(label, (x - size / 2 - 7, y - 7))
		
	return

	
def checkButtonClick(size):
	x = MAPWIDTH / 2 - size / 2
	y = MAPHEIGHT / 2 - size / 2
	buttonPosition = Rect(x, y, size, size)

	return buttonPosition.collidepoint(pygame.mouse.get_pos())
	
	
def intro():
	intro = True
	buttonSize = 25

	while intro:	
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			elif event.type == pygame.MOUSEBUTTONDOWN:
					intro = checkButtonClick(buttonSize)
				
		DISPLAYSURF.blit(START_PAGE,(0, 0))
		drawStartButton(buttonSize, intro)
		pygame.display.update()
		clock.tick(FPS)				
	return			

		
def start():
	hallObjects = [FLOOR, WALL_REAR, DOOR_GARDEN, PLANT, LAMP, DOOR_LIVING_ROOM, WALL_LEFT_4, DOOR_CHILDRENSROOM, WALL_RIGHT_3, DOOR_KITCHEN, WALL_LEFT_3,  DOOR_BATHROOM, WALL_RIGHT_2,DOOR_TOILET, WALL_LEFT_2, DOOR_BEDROOM, WALL_RIGHT_1, DOOR_BARN, WALL_LEFT_1, HAT_RACK]
	rooms = [BEDROOM, BATHROOM, CHILDRENSROOM, BARN, TOILET, KITCHEN, LIVINGROOM, GARDEN]
	mickey = pygame.sprite.Group(MICKEY)
	inRoom = False
	door = None
	textPlayed = False
	texts = [HELLO]

	BODY.changeSizeImage(BODY.width  / 10 + BODY.width / 50, BODY.height / 10 + BODY.height / 50)	#The image is already made the half of its size, because it is an object instance
	HAMMOCK_MICKEY.changeSizeImage(HAMMOCK_MICKEY.width  / 6, HAMMOCK_MICKEY.height / 6)	
	pygame.display.set_caption('Zoek Mickey!')
	pygame.mixer.music.set_volume(0.3)
	pygame.mixer.music.load("Geluidsopnamen/Mickey's Thema 1.mp3")
	pygame.mixer.music.play(-1)

	while True:

		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == pygame.MOUSEBUTTONDOWN:

				if inRoom:
					search(door, hidingPlace)
				else:				
					door = selectDoor(hallObjects, pygame.mouse.get_pos())
					
					if door:
						pygame.mixer.stop()
						textPlayed = True
	
		if inRoom and hidingPlace:
			displayRoom(mickey, door, hidingPlace, rooms)

		else:
			displayHall(mickey, hallObjects, rooms, door)
			
		if BAG_FLAP_OPEN in BARN.objects:
			BARN.objects[BARN.objects.index(BAG_FLAP_OPEN)] = BAG_FLAP_ALMOST_CLOSED
				
		if MICKEY.x <= 0  or  MICKEY.x >= MAPWIDTH:
			inRoom, door, textPlayed = resetParameters(inRoom, door, textPlayed)

			if inRoom:
				hidingPlace = assignHidingPlace(mickey, door)
				texts, textPlayed = setStartTextRoom(rooms, hidingPlace)

				hideMickey(hidingPlace)	
		
			DISPLAYSURF.fill(BLACK)

		pygame.display.update()

		if textPlayed == False:
			textPlayed = playTextsOnce(texts)
	return

intro()
start()

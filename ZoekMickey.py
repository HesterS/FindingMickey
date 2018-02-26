import pygame, sys
import random
import time
import sys
import numpy

from pygame.locals import *

class Object:
	def __init__(self, image, x, y, hidingCoordinates = None):
		self.image = image
		self.width = image.get_rect().size[0]/2 + 1 #The walls in the hall have to fit, and here in the test version the integers are made twice as small. When the number of pixels is odd, the new number will be 0.5 pixel to small, where integers are rounded below, which leads to cracks in the wall. Because of this, I give each object one pixel more, which you can hardly see in the result.
		self.height = image.get_rect().size[1]/2 + 1
		self.x = x
		self.y = y
		self.appearance = pygame.transform.scale(self.image, (self.width, self.height))
		self.hidingCoordinates = hidingCoordinates

	def changeSizeImage(self):
		self.appearance = pygame.transform.scale(self.image, (self.width, self.height))


class Door:
	
	def __init__(self, image, x, y):
		self.image = image
		self.width = image.get_rect().size[0]/2 + 2 # A marge because there absolutely has to be doors and the walls
		self.height = image.get_rect().size[1]/2 + 2
		self.x = x
		self.y = y
		self.appearance = pygame.transform.scale(image, (self.width, self.height))
		self.opened = False
	
	def changeSizeImage(self):
		self.appearance = pygame.transform.scale(self.image, (self.width, self.height))

	def open(self, side):
		self.opened = True
		self.appearance = pygame.transform.scale(self.image, (self.width / 2 + 1, self.height))

		if side == "right":
			self.x += self.width / 2

	def close(self, side):
		self.opened = False
		self.appearance = pygame.transform.scale(self.image, (self.width, self.height))

		if side == "right":
			self.x -= self.width / 2


MAPWIDTH = 2560/2
MAPHEIGHT = 1440/2

BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 30

pygame.init()

DISPLAYSURF = pygame.display.set_mode((MAPWIDTH, MAPHEIGHT))


#Hall
HALL_MAP = 'halMap/'

FLOOR = Object(pygame.image.load(HALL_MAP + 'vloer.png').convert_alpha(),0, MAPHEIGHT - 270)
HAT_RACK = Object(pygame.image.load(HALL_MAP + 'kapstok.png').convert_alpha(), 250, 200)
LAMP = Object(pygame.image.load(HALL_MAP + 'lamp.png').convert_alpha(), MAPWIDTH/2, 64)
PLANT = Object(pygame.image.load(HALL_MAP + 'plantje.png').convert_alpha(), 700, 154)

WALL_LEFT_1 = Object(pygame.image.load(HALL_MAP + 'muurLinks1.png').convert_alpha(), 0, 0)
WALL_LEFT_2 = Object(pygame.image.load(HALL_MAP + 'muurLinks2.png').convert_alpha(), 70, 16)
WALL_LEFT_3 = Object(pygame.image.load(HALL_MAP + 'muurLinks3.png').convert_alpha(), 70 + 138, 48)
WALL_LEFT_4 = Object(pygame.image.load(HALL_MAP + 'muurLinks4.png').convert_alpha(), 70 + 138 + 91, 70)
WALL_RIGHT_1 = Object(pygame.image.load(HALL_MAP + 'muurRechts1.png').convert_alpha(), MAPWIDTH - 170, 0)
WALL_RIGHT_2 = Object(pygame.image.load(HALL_MAP + 'muurRechts2.png').convert_alpha(), MAPWIDTH - 170 - 117, 40)
WALL_RIGHT_3 = Object(pygame.image.load(HALL_MAP + 'muurRechts3.png').convert_alpha(), MAPWIDTH - 170 - 117 - 91, 68)
WALL_REAR = Object(pygame.image.load(HALL_MAP + 'Middel_32.png').convert_alpha(), 0, 0)

DOOR_BARN = Door(pygame.image.load(HALL_MAP + 'deurLinksVoor.png').convert_alpha(), 33, 100)
DOOR_TOILET = Door(pygame.image.load(HALL_MAP + 'deurLinksMidVoor.png').convert_alpha(), 179, 118)
DOOR_KITCHEN = Door(pygame.image.load(HALL_MAP + 'duerLinksMidAchter.png').convert_alpha(), 276, 127)
DOOR_LEFT_REAR = Door(pygame.image.load(HALL_MAP + 'deurLinksAchter.png').convert_alpha(), 353, 139)
DOOR_BEDROOM = Door(pygame.image.load(HALL_MAP + 'deurRechtsVoor.png').convert_alpha(), 2130/2, 226/2)
DOOR_BATHROOM = Door(pygame.image.load(HALL_MAP + 'deurRechtsMidden.png').convert_alpha(),  1930/2, 256/2)
DOOR_CHILDRENSROOM = Door(pygame.image.load(HALL_MAP + 'deurRechtsAchter.png').convert_alpha(), 1774/2, 282/2)
DOOR_REAR = Door(pygame.image.load(HALL_MAP + 'deurAchter.png').convert_alpha(), 604, 149)


#bedroom
BEDROOM_MAP = 'Mickey261017/slaapkamer/'

BACKGROUND_BEDROOM = Object(pygame.image.load(BEDROOM_MAP +'achtergrond.png').convert_alpha(), 0, 0)
  
ELDERDOWN = Object(pygame.image.load(BEDROOM_MAP +'dekbed.png').convert_alpha(), 358, 410)
BED_REAR = Object(pygame.image.load(BEDROOM_MAP +'bedAchter.png').convert_alpha(), 380, 300)
PILLOW1 = Object(pygame.image.load(BEDROOM_MAP +'kussen1.png').convert_alpha(), 530, 361, (530, 361))
PILLOW2 = Object(pygame.image.load(BEDROOM_MAP +'kussen2.png').convert_alpha(), 625, 361, (625, 361))
DOG_UNDER_ELDERDOWN = Object(pygame.image.load(BEDROOM_MAP +'hondOnderDekbed.png').convert_alpha(), 549, 370, (600, 370))

BEDROOM_DOOR = Object(pygame.image.load(BEDROOM_MAP +'deur.png').convert_alpha(), 123, 114)
 
CURTAIN_LEFT = Object(pygame.image.load(BEDROOM_MAP +'gordijnLinks.png').convert_alpha(), 1153, 55, (1120, 686 - 134 / 2))
CURTAIN_MID_LEFT = Object(pygame.image.load(BEDROOM_MAP +'gordijnMiddenLinks.png').convert_alpha(), 1133, 61, (1100, 667 - 134 / 2))
CURTAIN_MID_RIGHT = Object(pygame.image.load(BEDROOM_MAP +'gordijnMiddenRechts.png').convert_alpha(), 1113, 67, (1080, 652 - 134 / 2))
CURTAIN_RIGHT = Object(pygame.image.load(BEDROOM_MAP +'gordijnRechts.png').convert_alpha(), 1093, 76, (1060, 640 - 134 / 2))

CLOSET_CLOSED = Object(pygame.image.load(BEDROOM_MAP +'kastDicht.png').convert_alpha(), 330, 71)
CLOSET_OPEN = Object(pygame.image.load(BEDROOM_MAP +'kastOpen.png').convert_alpha(), 385, 71)
REAR_WALL_CLOSET = Object(pygame.image.load(BEDROOM_MAP +'achterwandKast.png').convert_alpha(), 320, 60)
FRONT_WALL_CLOSET = Object(pygame.image.load(BEDROOM_MAP +'voorwandKast.png').convert_alpha(), 223, 53, (223, 500))

WALL_PART = Object(pygame.image.load(BEDROOM_MAP +'muurstukje.png').convert_alpha(), 0, 0) 
WALL_REST = Object(pygame.image.load(BEDROOM_MAP +'muurrest.png').convert_alpha(), 0, 0)

CHAIR_BACK = Object(pygame.image.load(BEDROOM_MAP +'stoelAchter.png').convert_alpha(), 855, 533, (865, 533 + 20)) 
CHAIR_FRONT = Object(pygame.image.load(BEDROOM_MAP +'stoelVoor.png').convert_alpha(), 950, 413, (927, 533 - 134 / 2))
 
TABLE = Object(pygame.image.load(BEDROOM_MAP +'tafel.png').convert_alpha(), 832, 334)

HAMPER_REAR = Object(pygame.image.load(BEDROOM_MAP +'wasmandAchter.png').convert_alpha(), 9, 575)
HAMPER_LID_CLOSED = Object(pygame.image.load(BEDROOM_MAP +'wasmandDekselDicht.png').convert_alpha(), 7, 575)
HAMPER_LID_OPEN = Object(pygame.image.load(BEDROOM_MAP +'wasmandDekselOpen.png').convert_alpha(), 7, 525)
HAMPER_FRONT = Object(pygame.image.load(BEDROOM_MAP +'wasmandVoor.png').convert_alpha(), 9, 575, (14, 575 + 134 / 2)) 


#bathroom
BATHROOM_MAP = 'badkamer/'

BACKGROUND_BATHROOM = Object(pygame.image.load(BATHROOM_MAP + 'achtergrond.png').convert_alpha(), 0, 0)

BATH_REAR = Object(pygame.image.load(BATHROOM_MAP + 'bad_achter.png').convert_alpha(), 986/2, 269/2)
BATH_FRONT = Object(pygame.image.load(BATHROOM_MAP + 'bad_voor.png').convert_alpha(), 986/2, 825/2, (986/2 + 982 / 4, 825/2))

BATHROOM_DOOR = Object(pygame.image.load(BATHROOM_MAP + 'deur.png').convert_alpha(), 199/2, 224/2)

TOWEL_FLAT = Object(pygame.image.load(BATHROOM_MAP + 'handdoek_plat.png').convert_alpha(), 1105, 440, (1105, 400 + 510/2 - 134 / 2))
TOWEL_WIDE = Object(pygame.image.load(BATHROOM_MAP + 'handdoek_wijd.png').convert_alpha(), 1105, 440, (1105, 400 + 510/2 - 134 / 2))

STOOL = Object(pygame.image.load(BATHROOM_MAP + 'krukje.png').convert_alpha(), 1862/2, 902/2, (1840/2, 830/2 + 297/2 - 134 / 2))

BATHROOM_WALLS = Object(pygame.image.load(BATHROOM_MAP + 'muren.png').convert_alpha(), 0, 0)
BATHROOM_WALLPART = Object(pygame.image.load(BATHROOM_MAP + 'muurstukje.png').convert_alpha(), 0, 0)
BATHROOM_FLOOR = Object(pygame.image.load(BATHROOM_MAP + 'vloer.png').convert_alpha(), 0, MAPHEIGHT - 400/2)

SINK = Object(pygame.image.load(BATHROOM_MAP + 'wastafel.png').convert_alpha(), 1950/2, 413/2)
TOILET_BATHROOM = Object(pygame.image.load(BATHROOM_MAP + 'wc.png').convert_alpha(), 480/2, 632/2, (300, 632/2 + 492/2 - 134 / 2))

MAT_HUMP = Object(pygame.image.load(BATHROOM_MAP + 'matje_bult.png').convert_alpha(), 1035/2, 1052/2, (1035/2 + 125, 1052/2))
MAT_FLAT = Object(pygame.image.load(BATHROOM_MAP + 'matje_plat.png').convert_alpha(), 1035/2, 1175/2, (1035/2 + 125, 1052/2))


#Children's room
CHILDRENS_ROOM_MAP = 'MickeyKinderkamer/'

BALL = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'bal.png').convert_alpha(), 902, 550)

BED_BACK = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'bed_achter.png').convert_alpha(), 282, 148)
BED_FRONT = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'bed_voor.png').convert_alpha(), 270, 148, (270 + 844 / 4, 165))

BEAR = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'beer.png').convert_alpha(), 559, 105, (559, 165))
DOLL_WHITE = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'blanke_pop.png').convert_alpha(), 304, 454, (304, 449))
DOLL_BROWN = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'bruine_pop.png').convert_alpha(), 237, 469, (255, 484))

CHILDRENSROOM_DOOR = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'deur.png').convert_alpha(), 20, 100)

LITTLE_CLOSET = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'kastje.png').convert_alpha(), 1089, 454, (1079, 560))

WALLS_CHILDRENSROOM = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'muren.png').convert_alpha(), 0, 0)
WALLPART_CHILDRENSROOM = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'muurstukje.png').convert_alpha(), 0, 0)

DOLL_CARRIAGE_BACK = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'poppenwagen_achter.png').convert_alpha(), 477, 544)
DOLL_CARRIAGE_FRONT = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'poppenwagen_voor.png').convert_alpha(), 460, 536, (490, 540))

TENT_BACK = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'tent_achter.png').convert_alpha(), 787, 230)
TENT_CLOSED = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'tent_dicht.png').convert_alpha(), 777, 403)
TENT_OPEN = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'tent_open.png').convert_alpha(), 757, 403)
TENT_FRONT = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'tent_voor.png').convert_alpha(), 737, 227, (767, 227  + 744/2 - 134 / 2 - 50))

TRAIN = Object(pygame.image.load(CHILDRENS_ROOM_MAP + 'trein.png').convert_alpha(), 850, 614)

#Barn
BARN_MAP = 'schuur/'

BACKGROUND_BARN = Object(pygame.image.load(BARN_MAP + 'achtergrond.png').convert_alpha(), 0, 0)
BARN_DOOR = Object(pygame.image.load(BARN_MAP + 'deur.png').convert_alpha(), 1087, 105)
BARN_WALL_PART = Object(pygame.image.load(BARN_MAP + 'muurstukje.png').convert_alpha(), 1151, 0)

BOX_BACK = Object(pygame.image.load(BARN_MAP + 'doos_achter.png').convert_alpha(), 462, 505)
BOX_FRONT = Object(pygame.image.load(BARN_MAP + 'doos_voor.png').convert_alpha(), 462, 545, (462 + 25, 565))

BICYCLE_BAG_BACK = Object(pygame.image.load(BARN_MAP + 'fiets_tas_achter.png').convert_alpha(), 5, 296)
BAG_FLAP_ALMOST_CLOSED = Object(pygame.image.load(BARN_MAP + 'tasklep_bijna_dicht.png').convert_alpha(), 65, 420)
BAG_FLAP_CLOSED = Object(pygame.image.load(BARN_MAP + 'tasklep_dicht.png').convert_alpha(), 65, 425)
BAG_FLAP_OPEN = Object(pygame.image.load(BARN_MAP + 'tasklep_open.png').convert_alpha(), 65, 370)
BAG_FRONT = Object(pygame.image.load(BARN_MAP + 'tas_voor.png').convert_alpha(), 122, 453, (122 + 50, 453))

RAKE_BROOM_SHOVEL = Object(pygame.image.load(BARN_MAP + 'hark_veger_schep.png').convert_alpha(), 719, 207)

WHEELBARROW = Object(pygame.image.load(BARN_MAP + 'kruiwagen.png').convert_alpha(), 893, 265, (893, 400))

FOOTBALL = Object(pygame.image.load(BARN_MAP + 'voetbal.png').convert_alpha(), 280, 612)

GARBAGE_CAN = Object(pygame.image.load(BARN_MAP + 'vuilnisbak.png').convert_alpha(), 251, 305)

WORK_TABLE_BIGGER = Object(pygame.image.load(BARN_MAP + 'werktafel_groter.png').convert_alpha(), 361, 421)
WORK_TABLE = Object(pygame.image.load(BARN_MAP + 'werktafel.png').convert_alpha(), 361, 421, (361, 421 + 100))


#toilet
TOILET_MAP = "wc/"

BACKGROUND_TOILET = Object(pygame.image.load(TOILET_MAP + 'achtergrond.png').convert_alpha(), 0, 0)
TOILET_DOOR = Object(pygame.image.load(TOILET_MAP + 'deur.png').convert_alpha(), 919, 121)
WALLS_TOILET = Object(pygame.image.load(TOILET_MAP + 'muren.png').convert_alpha(), 0, 0)
WALL_PART_TOILET = Object(pygame.image.load(TOILET_MAP + 'muurstukje.png').convert_alpha(), 962, 0)

TOWEL_FLAT_TOILET = Object(pygame.image.load(TOILET_MAP + 'handdoek_plat.png').convert_alpha(), 514, 341, (478, 341 + 510/2 - 134 / 2))
TOWEL_WIDE_TOILET = Object(pygame.image.load(TOILET_MAP + 'handdoek_wijd.png').convert_alpha(), 478, 341, (478, 341 + 510/2 - 134 / 2))

TOILET_CLOSET_CLOSED = Object(pygame.image.load(TOILET_MAP + 'kast_dicht.png').convert_alpha(), 629, 384)
TOILET_CLOSET_OPEN = Object(pygame.image.load(TOILET_MAP + 'kast_open.png').convert_alpha(), 629, 384)
TOILET_CLOSET = Object(pygame.image.load(TOILET_MAP + 'kast.png').convert_alpha(), 616, 144)

GARBAGE_CAN_TOILET = Object(pygame.image.load(TOILET_MAP + 'vuilnisbak.png').convert_alpha(), 1103, 546)

TOILET = Object(pygame.image.load(TOILET_MAP + 'wc.png').convert_alpha(), 187, 324)
TOILET_ROLLS_MASS = Object(pygame.image.load(TOILET_MAP + 'wcrollenberg.png').convert_alpha(), 35, 515)
TOILET_ROLLS_PILE = Object(pygame.image.load(TOILET_MAP + 'wcrollenstapel.png').convert_alpha(), 35, 510, (150, 550))


#kitchen
KITCHEN_MAP = "keuken/"

BACKGROUND_KITCHEN = Object(pygame.image.load(KITCHEN_MAP + 'achtergrond.png').convert_alpha(), 0, 0)
KITCHEN_DOOR = Object(pygame.image.load(KITCHEN_MAP + 'deur.png').convert_alpha(), 1031, 121)
WALLS_KITCHEN = Object(pygame.image.load(KITCHEN_MAP + 'muren.png').convert_alpha(), 0, 0)
WALL_PART_KITCHEN = Object(pygame.image.load(KITCHEN_MAP + 'muurstukje.png').convert_alpha(), 1077, 0)

CASES_BACK = Object(pygame.image.load(KITCHEN_MAP + 'kratten achter.png').convert_alpha(), 1121, 232)
CASES_FRONT = Object(pygame.image.load(KITCHEN_MAP + 'kratten voor.png').convert_alpha(), 1129, 232)

DRAWER_OPEN_BACK = Object(pygame.image.load(KITCHEN_MAP + 'la open achterkant.png').convert_alpha(), 834, 453)
DRAWER_OPEN_FRONT = Object(pygame.image.load(KITCHEN_MAP + 'la open voorkant.png').convert_alpha(), 834, 453)

KITCHEN_PLANT = Object(pygame.image.load(KITCHEN_MAP + 'plant.png').convert_alpha(), 5, 174, (55, 174 + 400))

CHAIR_BLUE_LEFT_BACK = Object(pygame.image.load(KITCHEN_MAP + 'stoel blauw links achterkant.png').convert_alpha(), 357, 547, (357, 557))
CHAIR_BLUE_LEFT_FRONT = Object(pygame.image.load(KITCHEN_MAP + 'stoel blauw links voorkant.png').convert_alpha(), 350, 447, (350, 560 - 134/2))
CHAIR_BLUE_RIGHT_BACK = Object(pygame.image.load(KITCHEN_MAP + 'stoel blauw rechts achterkant.png').convert_alpha(), 500, 539, (500, 556))
CHAIR_BLUE_RIGHT_FRONT = Object(pygame.image.load(KITCHEN_MAP + 'stoel blauw rechts voorkant.png').convert_alpha(), 489, 434, (500, 550 - 134/2))
CHAIR_YELLOW_LEFT = Object(pygame.image.load(KITCHEN_MAP + 'stoel geel links.png').convert_alpha(), 564, 359)
CHAIR_YELLOW_RIGHT = Object(pygame.image.load(KITCHEN_MAP + 'stoel geel rechts.png').convert_alpha(), 658, 372)

TABLE_BACK = Object(pygame.image.load(KITCHEN_MAP + 'tafel achterkant.png').convert_alpha(), 491, 385)
TABLE_FRONT = Object(pygame.image.load(KITCHEN_MAP + 'tafel voorkant.png').convert_alpha(), 373, 369)


VELOCITY_MICKEY = 6

		
class Mickey(pygame.sprite.Sprite):
	def __init__(self):
		super(Mickey, self).__init__()

		self.x = MAPWIDTH / 2
		self.y = MAPHEIGHT - 200
		#The size is no 10 times smaller than the originale / 2 + a part 100 times smaller than the original.
		self.width = 188 / 2 + 19 
		self.height = 134 / 2 + 13
		self.jumpFinished = False
		self.numberOfWalkFiles = 10
		self.numberOfJumpFiles = 12
		self.walkImages = self.fillImages(self.numberOfWalkFiles, "tekeningen/MickeyLoopt/MickeyLoopt000", self.width, self.height)
		self.comeImages = self.fillImages(self.numberOfWalkFiles, "MickeyKomtEnGaat/MickeyKomtAnimate/MickeyKomt000", 104/2 + 10, 152/2 + 15)
		self.goImages = self.fillImages(self.numberOfWalkFiles, "MickeyKomtEnGaat/MickeyGaatAnimate/MickeyGaat000", 121/2 + 12, 137/2 + 14)
		self.jumpImages = self.fillImages(self.numberOfJumpFiles, "MickeySpringt/MickeySpringt_Animator/MickeySpringt000", 222/2 + 22, 190/2 + 19)
		self.index = 0
		self.image = self.walkImages[self.index]
		self.rect = pygame.Rect(self.x, self.y, True, False)
		self.found = False


        #Returns a list of images which are displayed after each to let the sprite perform a particular act (like walking). The parameters are the number of files, the filename until a number displayed in the filename, (all filenames must end with a number, f.e. for walk1.png...walk10.png teh filename untill number is walk), the width and the height you wish for this image array.
	def fillImages(self, numberOfFiles, filenameUntillNumber, width, height):
		images = []

		for i in range(1, numberOfFiles + 1):
			fileName = filenameUntillNumber + str(i) + ".png"			
			self.appearance = pygame.transform.scale(pygame.image.load(fileName), (width, height))
			images.append(self.appearance)

		return images


	#Lets the sprite make a movement. For the update function it is beuid-in that we can use it for the sprite group (which is name mickey in the code). The parameters are the delta for x and the delta for y.
	def update(self, xDelta, yDelta, action = None):		
		self.x += xDelta
		self.y += yDelta

 		if action == "jump":
			images = self.jumpImages
		
		elif action == "coming":
			images = self.comeImages

		elif action == "going":
			images = self.goImages

		else:
			images = self.walkImages

		if self.index == len(images) - 1:
			if action == "jump":
				self.jumpFinished = True

			self.index = 0

		self.image = images[self.index]
					
		if x < 0:
			self.image = pygame.transform.flip(self.image, True, False)

		self.rect = pygame.Rect(self.x, self.y, True, False)
		self.index += 1


	#Places the sprite on a x and y coordinate you give a parameters to this function.
	def place(self, x, y):
		self.x = x
		self.y = y
		self.rect = pygame.Rect(self.x, self.y, True, False)


	#Changes particulair parameters to the start state of the sprite
	def reset(self):
		self.width = 188 / 2 + 19 
		self.height = 134 / 2 + 13 
		self.x = MAPWIDTH / 2
		self.y = MAPHEIGHT - 200
		self.rect = pygame.Rect(self.x, self.y, True, False)


#Chooses the hiding places given some objects to choose between
def chooseHidingPlace(mickey, objects):
	index = random.randint(0, len(objects) - 1)
	
	return objects[index]


#Adjusts the size of the current image, which makes the image shown smaller if the y coordinate is smaller, to make it look like the sprite is smaller when it goes further away. It returns the new image.
def adjustSizeByY(sprite, startY):
	currentY = sprite.y
	newWidth = sprite.image.get_rect().size[0] * currentY / startY
	newHeight = sprite.image.get_rect().size[1] * currentY / startY

	return pygame.transform.scale(sprite.image, (newWidth, newHeight))


#Changes the size of a sprite.
def changeSizesByY(sprite, startY):
	currentY = sprite.y
	sprite.newWidth = sprite.image.get_rect().size[0] * currentY / startY
	sprite.newHeight = sprite.image.get_rect().size[1] * currentY / startY

	return


#Makes the image of a sprite a given fraction larger
def adjustSize(sprite, fraction):
	newWidth = sprite.image.get_rect().size[0] + sprite.image.get_rect().size[0] / fraction
	newHeight = sprite.image.get_rect().size[1] + sprite.image.get_rect().size[1] / fraction

	return pygame.transform.scale(sprite.image, (newWidth, newHeight))

	
#Draws the current image of mickeys given the sprite group, the sprite, and the objects drawn around Mickey (which are needed to see in which room Mickey is at the moment.
def drawMickey(mickey, sprite, objects):
	#If you applied the size changes incrementally to the previous images, you would lose detail. Instead, always begin with the original image and scale to the desired size.
	
	if objects[0] == BACKGROUND_TOILET:
		image = adjustSize(sprite, 6)

		DISPLAYSURF.blit(image, (sprite.x, sprite.y))

	elif objects[0] == FLOOR and (sprite.y < MAPHEIGHT - 200 or mickeySprite.y < FLOOR.y): #FLOOR is the first objects in the hallList
		image = adjustSizeByY(sprite, MAPHEIGHT - 200) #MAPHEIGHT - 200 is the place where mickey always starts in the hall

		DISPLAYSURF.blit(image, (sprite.x, sprite.y))
	else:
		mickey.draw(DISPLAYSURF)
	return		


#Lets the sprite move in the direction of the door, given the sprite group, the sprite, the door (object or door class), and the list of objects of the current room.
def runThroughDoor(mickey, sprite, door, objects):
	doorPlace = door.y + door.height - 25
	doorMarge = door.width + 10
	action = None
	delay = 3
	yAlpha = 0

	#Because the door images in the hall can open, they are door instances. The room doors are always drawn open, so I made these instances of the class object and not of the class door.
	if door.__class__.__name__ == "Door":
		if door.opened == False:
			if door.x < MAPWIDTH / 2:
				door.open("left")
			else:
				door.open("right")

		if sprite.y < MAPHEIGHT - 200:	
			changeSizesByY(sprite, MAPHEIGHT - 200)#The place in the hall where Mickey is drawn first is given as start height

	if door.x < MAPWIDTH / 2:
		xAlpha = VELOCITY_MICKEY * -1
	else:
		xAlpha = VELOCITY_MICKEY

	if sprite.y + sprite.height < doorPlace - VELOCITY_MICKEY:
		xAlpha -= delay
		yAlpha = delay
		action = "coming"
		
		if abs(door.x - mickeySprite.x) < doorMarge:
			xAlpha = 0

	elif sprite.y + sprite.height > doorPlace + VELOCITY_MICKEY:
		xAlpha += delay
		yAlpha = -delay
		action = "going"
		
		if abs(door.x - sprite.x) < doorMarge:
			xAlpha = 0
		
	mickey.update(xAlpha, yAlpha, action)
	drawMickey(mickey, sprite, objects)
	return


#Displays the objects and Mickey in the first room, while the sprite does not do any action yet, given the sprite group, the sprite, the objects of the current room, and the hidingPlace as an optional parameter.
def drawStartImage(mickey, sprite, objects, hidingPlace = None):

	if hidingPlace:
		draw(objects[:objects.index(hidingPlace)])
		drawMickey(mickey, sprite, objects)
		draw(objects[objects.index(hidingPlace):])
	else:
		#This is the start position in the hall
		draw(objects)
		mickey.draw(DISPLAYSURF)
	return


#Plays a look to shown all images of Mickey when he movew through a door, given the sprite group, the sprite, the objects of the room and the door (Object or Door class). 
def leaveRoom(mickey sprite, objects, door):

	while sprite.x >= 0 - VELOCITY_MICKEY and sprite.x <= MAPWIDTH + VELOCITY_MICKEY:
		#The index of the wall part around the door is needed, because the sprite of mickey has to run behind this wallpart. The wallpart is drawn earlier than the door for optical reasons. For this reason, everything until the wall part has to be drawn before the sprtie of mickey is placed.
		wallPartIndex = objects.index(door) - 1

		DISPLAYSURF.fill(BLACK)
		draw(objects[:wallPartIndex])
		runThroughDoor(mickey, door, objects)
		draw(objects[wallPartIndex:])
		clock.tick(FPS)
		pygame.display.update()
	return


#Verifies whether a given object (o) is selected, with the given mouse position. Return a boolean value.
def selectObject(o, mousePosition):
	objectRectFound = o.appearance.get_rect(topleft=(o.x, o.y))

	if objectRectFound.collidepoint(mousePosition):
		return True

	return False


#Returns the selected Door object, given a list of objects and the mouse position.
def selectDoor(objects, mousePosition):

	for o in objects:
		if isinstance(o, Door):
			doorRect = o.appearance.get_rect(topleft=(o.x, o.y))

			if doorRect.collidepoint(mousePosition):
				return o


#Displays a list of objects on the rihts plays on the screen. 
def draw(objects):

	for o in objects:
		DISPLAYSURF.blit(o.appearance, (o.x, o.y))
	return


#Calculates the a, b, and c values to calculate a parabola, given the x and y values for the start coordinates(1), highest point(2), and end coordinates(3).
def calcParabolaABC(x1, y1, x2, y2, x3, y3):
		nom = (x1-x2) * (x1-x3) * (x2-x3)

		a = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / nom
		b = (x3 * x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / nom
		c = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / nom

		return a,b,c

#Calculates the y value given a x-value, a value, b value, and c value.
def calculateY(x, a, b, c):
	return a * x**2 + b * x + c


#Lets the sprite move in the form of a parabola, with the correct images to jump, hiven the sprite group, the sprite, the objects of the current room, the object where the sprite was hided, and the values of three points in the parabola.
def jump(mickey, sprite, objects, hidingPlace, x1, y1, x2, y2, x3, y3):
	sprite.index = 0
	finalY = BED_REAR.y + BED_REAR.height
	numberOfJumpImages = 12
	deltaX = (x3 - x1) / (numberOfJumpImages - 1)
	y = y1
	jumpVelocity = 20 #FPS
	#The images for jumping are a littlr bit smaller than for walking, and Mickey always lowers a little when he starts jumping. Because of this, I make the y of Mickey a little bit higher before he starts jumping.
	sprite.y -= 20

	for x in numpy.arange(x1, x3 + deltaX, deltaX):
		a,b,c = calcParabolaABC(x1, y1, x2, y2, x3, y3)
		deltaY = calculateY(x, a, b, c) - y
		y = calculateY(x, a, b, c)

		mickey.update(deltaX, deltaY, "jump")
		draw(objects[:objects.index(hidingPlace)])
		drawMickey(mickey, sprite, objects)
		draw(objects[objects.index(hidingPlace):])
		clock.tick(jumpVelocity)
		pygame.display.update()
	return	


#Changes the an objects designated as hiding place with another objects, It returns directly the new object. It is used for example to change towel flat, when Mickey is not hided here, to towel wide. The parameters are the list of the objects of the current room, mikcey's hiding place, and the new layout for the hiding place.
def changeLayoutHidingPlace(objects, hidingPlace, newLayout):
	if hidingPlace in objects:
		objects[objects.index(hidingPlace)] = newLayout

	return newLayout


#Moves to Mickey sprite to a particular x coordinate, given the sprite groupl, the sprite, the objects of the current room, the hiding place, the end x, and thhe velocity in frames per second.
def walk(mickey, sprite, objects, hidingPlace, end, velocity):

	while abs(mickeySprite.x - end) > abs(velocity):
		mickey.update(velocity, 0)
		draw(objects[:objects.index(hidingPlace)])
		drawMickey(mickey, sprite, objects)
		draw(objects[objects.index(hidingPlace):])
		clock.tick(FPS)
		pygame.display.update()
	return


#Verifeis whether the jump funcion needs to be used and initializes it when needed, given the sprite group, the sprite, the objects in the room, the hiding place, the cx and y coordinates of the place where the sprite starts moving.
def jumpWhenNeeded(mickey, sprite, objects, hidingPlace, startX, startY):
	marge = 100

	if hidingPlace == DOG_UNDER_ELDERDOWN or hidingPlace == PILLOW1 or hidingPlace == PILLOW2:
		topX = ELDERDOWN.x
		topY = ELDERDOWN.y - 10
		endX = BED_REAR.x - sprite.width
		endY = BED_REAR.y + BED_REAR.height - sprite.height

		if DOG_UNDER_ELDERDOWN in objects:
			objects.remove(DOG_UNDER_ELDERDOWN)

			hidingPlace = ELDERDOWN

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	elif hidingPlace == HAMPER_FRONT or hidingPlace == DOLL_CARRIAGE_FRONT or hidingPlace == BOX_FRONT or hidingPlace == DOLL_BROWN or hidingPlace == BAG_FRONT:
		topX = hidingPlace.x + hidingPlace.width
		topY = hidingPlace.y - sprite.height
		endX = hidingPlace.x +  hidingPlace.width + marge

		if hidingPlace == BAG_FRONT:
			endY = BICYCLE_BAG_BACK.y + BICYCLE_BAG_BACK.height - sprite.height

		else:
			endY = hidingPlace.y + hidingPlace.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

		if hidingPlace == BAG_FRONT:
			objects[objects.index(BAG_FLAP_OPEN)] = BAG_FLAP_ALMOST_CLOSED

	elif hidingPlace == DRAWER_OPEN_FRONT:
		topX = hidingPlace.x - 10
		topY = hidingPlace.y - 50
		endX = hidingPlace.x - marge
		endY = hidingPlace.y + hidingPlace.height - sprite.height
			
		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))
		
	elif hidingPlace == BEAR:
		topX = startX - marge
		topY = BED_FRONT.y + sprite.height
		endX = DOLL_WHITE.x + DOLL_WHITE.width
		endY = BED_FRONT.y + BED_FRONT.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	elif hidingPlace == BATH_FRONT:
		topX = hidingPlace.x
		topY = hidingPlace.y - 10
		endX = hidingPlace.x - marge
		endY = hidingPlace.y + hidingPlace.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	elif hidingPlace == WHEELBARROW or hidingPlace == CASES_FRONT:
		topX = hidingPlace.x - marge/2
		topY = startY - 10
		endX = hidingPlace.x - marge
		endY = hidingPlace.y + hidingPlace.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

		if hidingPlace == CASES_FRONT:
			walk(mickey, sprite, objects, hidingPlace, endX - KITCHEN_DOOR.width, VELOCITY_MICKEY * -1)

	elif hidingPlace == CHAIR_FRONT:
		topX = CHAIR_BACK.x
		topY = CHAIR_BACK.y - 20
		endX = CHAIR_BACK.x - marge
		endY = CHAIR_BACK.y + CHAIR_BACK.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	elif hidingPlace == CHAIR_BLUE_LEFT_FRONT:
		topX = CHAIR_BLUE_LEFT_BACK.x - 50
		topY = CHAIR_BLUE_LEFT_BACK.y - 50
		endX = CHAIR_BLUE_LEFT_BACK.x - marge
		endY = CHAIR_BLUE_LEFT_BACK.y + CHAIR_BLUE_LEFT_BACK.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

	elif hidingPlace == CHAIR_BLUE_RIGHT_FRONT:
		topX = CHAIR_BLUE_RIGHT_BACK.x + 50
		topY = CHAIR_BLUE_RIGHT_BACK.y - 50
		endX = CHAIR_BLUE_RIGHT_BACK.x + marge
		endY = CHAIR_BLUE_RIGHT_BACK.y + CHAIR_BLUE_RIGHT_BACK.height - sprite.height

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))
					
	elif hidingPlace == TOILET_CLOSET_CLOSED:
		hidingPlace = changeLayoutHidingPlace(objects, TOILET_CLOSET_CLOSED, TOILET_CLOSET_OPEN)
		topX = TOILET_CLOSET_OPEN.x + TOILET_CLOSET_OPEN.width
		topY = TOILET_CLOSET_OPEN.y
		endX = TOILET_CLOSET_OPEN.x + TOILET_CLOSET_OPEN.width + sprite.image.get_rect().size[0]
		endY = TOILET_CLOSET.y + TOILET_CLOSET.height - sprite.image.get_rect().size[1]

		jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))	
	return


def comeOut(mickey, sprite, objects, hidingPlace, startX, startY):
	marge = 100	
	
	jumpWhenNeeded(mickey, sprite, objects, hidingPlace, startX, startY)

	if hidingPlace == CURTAIN_LEFT or hidingPlace == CURTAIN_RIGHT or hidingPlace == CURTAIN_MID_RIGHT or hidingPlace == CURTAIN_MID_LEFT:
			walk(mickey, sprite, objects, hidingPlace, hidingPlace.x - marge + 10, VELOCITY_MICKEY * -1)		
			
	elif hidingPlace == DOLL_WHITE or hidingPlace == BEAR:	
		walk(mickey, sprite, objects, hidingPlace, DOLL_WHITE.x + DOLL_WHITE.width + 60, VELOCITY_MICKEY)
		#I have put 10 pixels extra by the marge, because otherwise mickey runs partly under the foot of the brown doll.	

	elif hidingPlace == RAKE_BROOM_SHOVEL or hidingPlace == FRONT_WALL_CLOSET or hidingPlace == FOOTBALL or hidingPlace == WORK_TABLE:
		walk(mickey, sprite, objects, hidingPlace, hidingPlace.x + hidingPlace.width + 10, VELOCITY_MICKEY)

	elif hidingPlace == STOOL or hidingPlace == BALL or hidingPlace == LITTLE_CLOSET:
		walk(mickey, sprite, objects, hidingPlace, hidingPlace.x - marge, VELOCITY_MICKEY * -1)

	elif hidingPlace == GARBAGE_CAN_TOILET:
		walk(mickey, sprite, objects, hidingPlace, hidingPlace.x - marge - TOILET_DOOR.width, VELOCITY_MICKEY * -1)
	return
			

def hideAndSeek(mickey, sprite, objects, hidingPlace, door):
	#default jump values, little jump
	startX = mickeySprite.x
	startY = mickeySprite.y
	topX = mickeySprite.x + 5
	topY = mickeySprite.y - 5
	endX = mickeySprite.x + 10
	endY = mickeySprite.y + 10

	#when found in the hamper or box, mickey's front paws go through the hamper when he starts jumping. This has to be made better			
	if mickeySprite.found:
		if hidingPlace == TOWEL_WIDE:
			hidingPlace = changeLayoutHidingPlace(objects, TOWEL_WIDE, TOWEL_FLAT)

		elif hidingPlace == TOWEL_WIDE_TOILET:
			hidingPlace = changeLayoutHidingPlace(objects, TOWEL_WIDE_TOILET, TOWEL_FLAT_TOILET) 

		elif hidingPlace == MAT_HUMP:
			hidingPlace = changeLayoutHidingPlace(objects, MAT_HUMP, MAT_FLAT)

			jump(mickey, objects, hidingPlace, float(startX), float(startY), float(topX), float(topY), float(endX), float(endY))

		comeOut(mickey, sprite, objects, hidingPlace, startX, startY)
		leaveRoom(mickey, sprite, objects, door)
	else:
		if hidingPlace == TOILET_CLOSET_CLOSED and TOILET_CLOSET_OPEN in objects:
			hidingPlace = TOILET_CLOSET_OPEN
			
		drawStartImage(mickey, objects, hidingPlace)
	return


def checkMouseClick(mickeySprite, door, hidingPlace, objects, objectsClosed = [], objectsOpen = [], hidingPlaceObjectsClosed = []):

	for i in range(len(objectsClosed)):
		if objectsClosed[i] in objects:
			if selectObject(objectsClosed[i], pygame.mouse.get_pos()):
				objects[objects.index(objectsClosed[i])] = objectsOpen[i]
							
			if hidingPlace == hidingPlaceObjectsClosed[i]:
				return selectObject(objectsClosed[i], pygame.mouse.get_pos())

	return  selectObject(mickeySprite, pygame.mouse.get_pos())


def prepare(mickey, objects, possibleHidingPlaces, objectsToCheck = [], resetValues = [], layoutNoHiding = [], layoutHiding = []):

	for i in range(len(objectsToCheck)):
		if objectsToCheck[i] in objects:
			objects[objects.index(objectsToCheck[i])] = resetValues[i]

	hidingPlace = chooseHidingPlace(mickey, possibleHidingPlaces)

	for i in range(len(layoutNoHiding)):
		if layoutNoHiding[i] == hidingPlace:
			hidingPlace = changeLayoutHidingPlace(objects, layoutNoHiding[i], layoutHiding[i])		
	
	if hidingPlace == ELDERDOWN:
		hidingPlace = DOG_UNDER_ELDERDOWN

		bedroomObjects.insert(bedroomObjects.index(ELDERDOWN), DOG_UNDER_ELDERDOWN)

	if hidingPlace == CASES_FRONT:
		boxes = ["blue box", "red box", "yellow box"]
		boxToHide = random.choice(boxes)

		if boxToHide == "blue box":
			hidingPlace.hidingCoordinates = (1163, 290)
		elif boxToHide == "red box":
			hidingPlace.hidingCoordinates = (1160, 440)
		else:
			hidingPlace.hidingCoordinates = (1165, 580)

	return hidingPlace


def findMickey(sprite, door, hidingPlace, bedroomObjects, bathroomObjects, childrensroomObjects, barnObjects, toiletObjects, kitchenObjects):
	if door == DOOR_BEDROOM:
		return checkMouseClick(sprite, door, hidingPlace, bedroomObjects, [CLOSET_CLOSED, HAMPER_LID_CLOSED], [CLOSET_OPEN, HAMPER_LID_OPEN], [FRONT_WALL_CLOSET, HAMPER_FRONT])

	elif door == DOOR_BATHROOM:
		return checkMouseClick(sprite, door, hidingPlace, bathroomObjects)

	elif door == DOOR_CHILDRENSROOM:
		return checkMouseClick(sprite, door, hidingPlace, childrensroomObjects, [TENT_CLOSED], [TENT_OPEN], [TENT_FRONT])
	
	elif door == DOOR_BARN:
		return checkMouseClick(sprite, door, hidingPlace, barnObjects, [BAG_FLAP_CLOSED], [BAG_FLAP_OPEN], [BAG_FRONT])

	elif door == DOOR_TOILET:
		return checkMouseClick(sprite, door, hidingPlace, toiletObjects, [TOILET_CLOSET_CLOSED, TOILET_ROLLS_PILE], [TOILET_CLOSET_OPEN, TOILET_ROLLS_MASS], [CLOSET_CLOSED, TOILET_ROLLS_PILE])

	elif door == DOOR_KITCHEN:
		return checkMouseClick(sprite, door, hidingPlace, kitchenObjects)


def displayRoom(mickey, sprite, door, hidingPlace, bedroomObjects, bathroomObjects, childrensroomObjects, barnObjects, toiletObjects, kitchenObjects):
	if door == DOOR_BEDROOM:
		hideAndSeek(mickey, sprite, bedroomObjects, hidingPlace, BEDROOM_DOOR)

	elif door == DOOR_BATHROOM:
		hideAndSeek(mickey, sprite, bathroomObjects, hidingPlace, BATHROOM_DOOR)

	elif door == DOOR_CHILDRENSROOM:
		hideAndSeek(mickey, sprite, childrensroomObjects, hidingPlace, CHILDRENSROOM_DOOR)

	elif door == DOOR_BARN:
		hideAndSeek(mickey, sprite, barnObjects, hidingPlace, BARN_DOOR)

	elif door == DOOR_TOILET:
		hideAndSeek(mickey, sprite, toiletObjects, hidingPlace, TOILET_DOOR)

	elif door == DOOR_KITCHEN:
		hideAndSeek(mickey, sprite, kitchenObjects, hidingPlace, KITCHEN_DOOR)
	else:
		sys.exit()
	return
			

	
def start():
	mickeySprite = Mickey()
	mickey = pygame.sprite.Group(mickeySprite)
	inRoom = False
	selected = False
	toiletSize = False

	hallObjects = [FLOOR, WALL_REAR, DOOR_REAR, PLANT, LAMP, DOOR_LEFT_REAR, WALL_LEFT_4, DOOR_CHILDRENSROOM, WALL_RIGHT_3, DOOR_KITCHEN, WALL_LEFT_3,  DOOR_BATHROOM, WALL_RIGHT_2,DOOR_TOILET, WALL_LEFT_2, DOOR_BEDROOM, WALL_RIGHT_1, DOOR_BARN, WALL_LEFT_1, HAT_RACK]
 
	bedroomObjects = [BACKGROUND_BEDROOM, WALL_REST, REAR_WALL_CLOSET, CLOSET_CLOSED, FRONT_WALL_CLOSET, TABLE, BED_REAR, PILLOW1, PILLOW2, ELDERDOWN, CURTAIN_RIGHT, CURTAIN_MID_RIGHT, CURTAIN_MID_LEFT, CURTAIN_LEFT, WALL_PART, BEDROOM_DOOR, CHAIR_BACK, CHAIR_FRONT,HAMPER_REAR, HAMPER_LID_CLOSED, HAMPER_FRONT]
  
	bathroomObjects = [BACKGROUND_BATHROOM, BATHROOM_WALLS, BATHROOM_FLOOR, BATH_REAR, TOILET_BATHROOM, BATH_FRONT, STOOL, SINK, TOWEL_FLAT, MAT_FLAT, BATHROOM_WALLPART, BATHROOM_DOOR]

	childrensroomObjects = [WALLS_CHILDRENSROOM, BED_BACK, BEAR, BED_FRONT, TENT_BACK, TENT_FRONT, TENT_CLOSED, DOLL_WHITE, DOLL_BROWN, BALL, TRAIN, WALLPART_CHILDRENSROOM, CHILDRENSROOM_DOOR, DOLL_CARRIAGE_BACK, LITTLE_CLOSET, DOLL_CARRIAGE_FRONT]
	
	barnObjects = [BACKGROUND_BARN, GARBAGE_CAN, RAKE_BROOM_SHOVEL, WHEELBARROW, WORK_TABLE, BICYCLE_BAG_BACK, BAG_FRONT, BAG_FLAP_CLOSED, FOOTBALL, BARN_WALL_PART, BARN_DOOR, BOX_BACK, BOX_FRONT]
	
	toiletObjects = [BACKGROUND_TOILET, WALLS_TOILET, TOWEL_FLAT_TOILET, TOILET_CLOSET, TOILET_CLOSET_CLOSED, WALL_PART_TOILET, TOILET_DOOR, TOILET, GARBAGE_CAN_TOILET, TOILET_ROLLS_PILE]
	
	kitchenObjects = [BACKGROUND_KITCHEN, WALLS_KITCHEN, DRAWER_OPEN_BACK, DRAWER_OPEN_FRONT, CHAIR_YELLOW_LEFT, CHAIR_YELLOW_RIGHT, TABLE_BACK, WALL_PART_KITCHEN, KITCHEN_DOOR, TABLE_FRONT, CHAIR_BLUE_LEFT_BACK, CHAIR_BLUE_RIGHT_BACK, CHAIR_BLUE_LEFT_FRONT, CHAIR_BLUE_RIGHT_FRONT, KITCHEN_PLANT, CASES_BACK, CASES_FRONT]
			
	pygame.display.set_caption('Zoek Mickey!')
	
	while True:
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

       	            	elif event.type == pygame.MOUSEBUTTONDOWN:
				if inRoom:
					mickeySprite.found = findMickey(mickeySprite, door, hidingPlace, bedroomObjects, bathroomObjects, childrensroomObjects, barnObjects, toiletObjects, kitchenObjects)
				else:				
					door = selectDoor(hallObjects, pygame.mouse.get_pos())

					if door != None:
						selected = True			
		if inRoom and hidingPlace:
			displayRoom(mickey, mickeySprite, door, hidingPlace, bedroomObjects, bathroomObjects, childrensroomObjects, barnObjects, toiletObjects, kitchenObjects)			
		else:
			if selected:
				DISPLAYSURF.fill(BLACK)
				leaveRoom(mickey, sprite, hallObjects, door) 
			else:
				drawStartImage(mickey, hallObjects)
			
		if BAG_FLAP_OPEN in barnObjects:
			barnObjects[barnObjects.index(BAG_FLAP_OPEN)] = BAG_FLAP_ALMOST_CLOSED
				
		if mickeySprite.x <= 0  or  mickeySprite.x >= MAPWIDTH:
			mickeySprite.reset()
	
			#reset all parameters
			if inRoom:
				inRoom = False
				mickeySprite.found = False
				hidingPlace = None				
			else:
				inRoom = True
				selected = False
				
				if door.x > MAPWIDTH / 2:
					door.close("right")
				else:
					door.close("left")
			
				if door == DOOR_BEDROOM:					
					possibleHidingPlaces = (FRONT_WALL_CLOSET, CURTAIN_LEFT, CURTAIN_MID_LEFT, CURTAIN_MID_RIGHT, CURTAIN_RIGHT, CHAIR_BACK, CHAIR_FRONT, PILLOW1, PILLOW2, ELDERDOWN, HAMPER_FRONT)
					hidingPlace = prepare(mickey, bedroomObjects, possibleHidingPlaces, [CLOSET_OPEN, HAMPER_LID_OPEN], [CLOSET_CLOSED, HAMPER_LID_CLOSED])

				elif door == DOOR_BATHROOM:			
					possibleHidingPlaces = (TOILET_BATHROOM, BATH_FRONT, STOOL, TOWEL_FLAT, MAT_FLAT)
					hidingPlace = prepare(mickey, bathroomObjects, possibleHidingPlaces, [], [], [TOWEL_FLAT, MAT_FLAT], [TOWEL_WIDE, MAT_HUMP])

				elif door == DOOR_CHILDRENSROOM:
					possibleHidingPlaces = (BEAR, TENT_FRONT, DOLL_WHITE, DOLL_BROWN, BALL, DOLL_CARRIAGE_BACK, DOLL_CARRIAGE_FRONT, LITTLE_CLOSET)
					hidingPlace = prepare(mickey, childrensroomObjects, possibleHidingPlaces, [TENT_OPEN], [TENT_CLOSED])

				elif door == DOOR_BARN:
					possibleHidingPlaces = (WHEELBARROW, RAKE_BROOM_SHOVEL, WORK_TABLE, BAG_FRONT, BOX_FRONT, BOX_BACK)
					hidingPlace = prepare(mickey, barnObjects, possibleHidingPlaces, [BAG_FLAP_ALMOST_CLOSED], [BAG_FLAP_CLOSED])

				elif door == DOOR_TOILET:
					possibleHidingPlaces = (TOWEL_FLAT_TOILET, TOILET_CLOSET_CLOSED, TOILET, GARBAGE_CAN_TOILET, TOILET_ROLLS_PILE)
					hidingPlace = prepare(mickey, toiletObjects, possibleHidingPlaces, [TOILET_CLOSET_OPEN, TOILET_ROLLS_MASS], [TOILET_CLOSET_CLOSED, TOILET_ROLLS_PILE], [TOWEL_FLAT_TOILET], [TOWEL_WIDE_TOILET])

				elif door == DOOR_KITCHEN:
					possibleHidingPlaces = (DRAWER_OPEN_FRONT, CHAIR_YELLOW_LEFT, CHAIR_YELLOW_RIGHT, TABLE_BACK, CHAIR_BLUE_LEFT_BACK, CHAIR_BLUE_RIGHT_BACK, CHAIR_BLUE_LEFT_FRONT, CHAIR_BLUE_RIGHT_FRONT, KITCHEN_PLANT, CASES_FRONT)
					hidingPlace = prepare(mickey, kitchenObjects, possibleHidingPlaces)

				print hidingPlace.x

				if hidingPlace.hidingCoordinates:
					mickeySprite.place(hidingPlace.hidingCoordinates[0], hidingPlace.hidingCoordinates[1])
				else:
					mickeySprite.place(hidingPlace.x, hidingPlace.y + hidingPlace.height - mickeySprite.image.get_rect().size[1] - 20)
					#Because mickey stands behind the objects, the y coordinaat has to be a little bit lower than the coodinate of the object
			
			DISPLAYSURF.fill(BLACK)

		pygame.display.update()
	return

start()

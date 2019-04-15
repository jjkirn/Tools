# Originally from the HTB "not_art" challenge
# Modified extensively to show various potential stenagorapy layers
# JKirn 3/20/19

import numpy as np
from PIL import Image

#################################################################################
# GLOBALS
#################################################################################

LSB_R   = "" #string representing the binary data obtained from R channel LSBs
LSB_G   = "" #string representing the binary data obtained from G channel LSBs
LSB_B   = "" #string representing the binary data obtained from B channel LSBs
LSB_RGB = "" #string representing the binary data obtained from RGB channel LSBs
LSB_BGR = "" #string representing the binary data obtained from BGR channel LSBs

LNIB_R   = ""
LNIB_G   = ""
LNIB_B   = ""
LNIB_RGB = ""

LSB2_R   = "" #string representing the binary data obtained from R channel LSB bit 2
LSB2_G   = "" #string representing the binary data obtained from G channel LSB bit 2
LSB2_B   = "" #string representing the binary data obtained from B channel LSB bit 2
LSB2_RGB = "" #string representing the binary data obtained from RGB channel LSB bit 2
LSB2_BGR = "" #string representing the binary data obtained from BGR channel LSB bit 2

MSB_R   = "" #string representing the binary data obtained from R channel MSBs
MSB_G   = "" #string representing the binary data obtained from G channel MSBs
MSB_B   = "" #string representing the binary data obtained from B channel MSBs
MSB_RGB = "" #string representing the binary data obtained from RGB channel MSBs
MSB_BGR = "" #string representing the binary data obtained from BGR channel MSBs

RGB_HEX    = "" #HEX string representing the binary values obtained from RGB values (each color byte is added as hex value)
RGB_TUPLES = "" #Ternary string representing the RGB values of the image 

IMAGE_ARRAY = None #multi dimensional array containing image data [X][Y][RGB] (X = width, Y = height, RGB = pixel colors)

MAX_X = 0 #width of the image, it represent the maximum value for X (should be 30)
MAX_Y = 0 #height of the image, it represent the maximum value for Y (should be 30)

NUM_PIXELS = 0 #total number of colored pixel elaborated (should be 479)

CURR_X = 0; CURR_Y = 0 #current position in the multi dimensional array [X][Y][RGB]

#################################################################################
# CONSTANTS
#################################################################################

#constants for indexes of R, G and B used while accessing the RGB tuple
#the tuple's elements can be accessed with array like notation 
# rgb_tuple[0] -> R
# rgb_tuple[1] -> G
# rgb_tuple[2] -> B
R = 0; G = 1; B = 2 

#constant for directions
RIGHT = 0; DOWN = 1; LEFT = 2; UP = 3

def get_color():
	global LSB_R, LSB_G, LSB_B, LSB_RGB, LSB_BGR
	global LSB2_B, LSB2_G, LSB2_R, LSB2_RGB, LSB2_BGR
	global MSB_B, MSB_G, MSB_R, MSB_RGB, MSB_BGR
	global LNIB_R, LNIB_G, LNIB_B, LNIB_RGB
	global RGB_HEX, RGB_TUPLES
	global NUM_PIXELS
	
	rgb_tuple = IMAGE_ARRAY[CURR_Y][CURR_X]

	#Look at LSB (bit 0)
	LSB_R   += str(rgb_tuple[R] & 1)
	LSB_G   += str(rgb_tuple[G] & 1)
	LSB_B   += str(rgb_tuple[B] & 1)
	LSB_RGB += str(rgb_tuple[R] & 1) + str(rgb_tuple[G] & 1) + str(rgb_tuple[B] & 1)
	LSB_BGR += str(rgb_tuple[B] & 1) + str(rgb_tuple[G] & 1) + str(rgb_tuple[R] & 1)

	#Look at 3rd bit (bit 2)
	LSB2_R   += str((rgb_tuple[R] & 0x04) >> 2)
	LSB2_G   += str((rgb_tuple[G] & 0x04) >> 2)
	LSB2_B   += str((rgb_tuple[B] & 0x04) >> 2)
	LSB2_RGB += str((rgb_tuple[R] & 0x04) >> 2) + str((rgb_tuple[G] & 0x04) >> 2) + str((rgb_tuple[B] & 0x04) >> 2)
	LSB2_BGR += str((rgb_tuple[B] & 0x04) >> 2) + str((rgb_tuple[G] & 0x04) >> 2) + str((rgb_tuple[R] & 0x04) >> 2)

	#Look at Lower Nibble (bits 0-3)
	LNIB_R += '{:04b}'.format(rgb_tuple[R] & 0xf)  
        LNIB_G += '{:04b}'.format(rgb_tuple[G] & 0xf)
	LNIB_B += '{:04b}'.format(rgb_tuple[B] & 0xf)
	LNIB_RGB += '{:04b}'.format(rgb_tuple[R] & 0xf) + '{:04b}'.format(rgb_tuple[G] & 0xf) + '{:04b}'.format(rgb_tuple[B] & 0xf)

	#Look at MSB (bit 7)
	MSB_R   += str((rgb_tuple[R] & 0x80) >> 7)
	MSB_G   += str((rgb_tuple[G] & 0x80) >> 7)
	MSB_B   += str((rgb_tuple[B] & 0x80) >> 7)
	MSB_RGB += str((rgb_tuple[R] & 0x80) >> 7) + str((rgb_tuple[G] & 0x80) >> 7) + str((rgb_tuple[B] & 0x80) >> 7)
	MSB_BGR += str((rgb_tuple[B] & 0x80) >> 7) + str((rgb_tuple[G] & 0x80) >> 7) + str((rgb_tuple[R] & 0x80) >> 7)

	RGB_HEX += '{:02x}'.format(rgb_tuple[R]) + '{:02x}'.format(rgb_tuple[G]) + '{:02x}'.format(rgb_tuple[B])
	RGB_TUPLES += str(rgb_tuple)
	
	NUM_PIXELS+=1
	#print "(X=" + str(CURR_X) +",Y=" + str(CURR_Y) + ") r = " +str(rgb_tuple[R]) + " g = " +str(rgb_tuple[G]) + " b = " +str(rgb_tuple[B])
    
def is_color(rgb_tuple):

	if ((rgb_tuple[R] == 0) and (rgb_tuple[G] == 0) and (rgb_tuple[B] == 0)):
		return False

	return True


def next_x_is_color():

	if ((CURR_X+1) == MAX_Y):
		#print "CURR_X+1 = MAX"
		return False

	return is_color(IMAGE_ARRAY[CURR_Y][CURR_X+1])


def prev_x_is_color():

	if ((CURR_X-1) < 0):
		#print "CURR_X-1 = min"
		return False

	return is_color(IMAGE_ARRAY[CURR_Y][CURR_X-1])


def next_y_is_color():
	
	if ((CURR_Y+1) == MAX_X):
		#print "CURR_Y+1 = MAX"
		return False

	return is_color(IMAGE_ARRAY[CURR_Y+1][CURR_X])


def prev_y_is_color():

	if ((CURR_Y-1) < 0):
		return False

	return is_color(IMAGE_ARRAY[CURR_Y-1][CURR_X])


def print_results():
	#Note: 	binary data displayed as '0'&'1' string, shall be converted to a real binay
	#		the string can be converted to ASCII online for first inspection
	#		Example: https://www.rapidtables.com/convert/number/binary-to-ascii.html
	
	print "Info: total color pixels = " + str(NUM_PIXELS)
	
	print ">>>LSB_R<<<"
	print LSB_R

	print ">>>LSB_G<<<"
	print LSB_G

	print ">>>LSB_B<<<"
	print LSB_B

	print ">>>LSB_RGB<<<"
	print LSB_RGB

	print ">>>LSB_BGR<<<"
	print LSB_BGR

#	print ">>>LSB2_R<<<"
#	print LSB2_R

#	print ">>>LSB2_G<<<"
#	print LSB2_G

#	print ">>>LSB2_B<<<"
#	print LSB2_B

#	print ">>>LSB2_RGB<<<"
#	print LSB2_RGB

#	print ">>>LSB2_BGR<<<"
#	print LSB2_BGR


#	print ">>>MSB_R<<<"
#	print MSB_R

#	print ">>>MSB_G<<<"
#	print MSB_G

#	print ">>>MSB_B<<<"
#	print MSB_B

#	print ">>>MSB_RGB<<<"
#	print MSB_RGB

#	print ">>>MSB_BGR<<<"
#	print MSB_BGR

#	print ">>>RGB_HEX<<<"
#	print RGB_HEX
	
#	print ">>>RGB_TUPLES<<<"
#	print RGB_TUPLES
	
#	print ">>>LNIB_R<<<"   #Lower Nibbles
#	print LNIB_R

#	print ">>>LNIB_G<<<"
#	print LNIB_G

#	print ">>>LNIB_B<<<"
#	print LNIB_B

#	print ">>>LNIB_RGB<<<"
#	print LNIB_RGB
	
def main():
	
	global CURR_X, CURR_Y, dir, IMAGE_ARRAY, MAX_X , MAX_Y
	
	# note: image = massacre.png  (HTB) -- Program modifed for this challenge
	#	
	#	Original image 4032 x 3024 (x,y)
	# 	Current position in the multi dimensional array [X][Y][RGB]
	#	The Python Imaging Library uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner.
	#	Coordinates are passed to the library as 2-tuples (x, y)
	#	This program has been modifiled to look at LSB of bits in the Left column of image.
	#	CURR_X and CURR_Y were intially set to 0.
	#	It prints out LSB(RGB) of each pixel
	#	Followed by RGB HEX
	#
	#	Verified as correct by JJK 3/15/19
	#

	img = Image.open('massacre.png')
	IMAGE_ARRAY = np.array(img)
	MAX_Y , MAX_X, depth = np.shape(IMAGE_ARRAY)

	print ("MAX_X:")
	print MAX_X
	print ("MAX_Y:")
	print MAX_Y
	
	direction = DOWN  #initial directions
	for y in range(0,MAX_Y):
		get_color()
		CURR_Y+=1

	print_results()
	exit()            #skip everything below

###################################################################################
# Nothing below here is used in this version - remniants of "not_art" HTB challenge
###################################################################################

	NUM_PIXELS = 0
	direction = RIGHT #initial directions
	
	#note: 	exit condition is not elegant, but gets the job done: 
	#		last pixel of the spiral is at pos 15,15 in the minified image
	
	while ((CURR_X != 15) or (CURR_Y != 15)):	
		
		if (direction == RIGHT):
			get_color()

			if (True == next_x_is_color()):
				CURR_X+=1
			else:
				#print "New direction = DOWN"
				direction = DOWN
				CURR_Y+=1
				continue

		if (direction == DOWN):
			get_color()

			if (True == next_y_is_color()):
				CURR_Y+=1
			else:
				#print "New direction = LEFT"
				direction = LEFT
				CURR_X=CURR_X-1
				continue

		if (direction == LEFT):
			get_color()

			if (True == prev_x_is_color()):
				CURR_X=CURR_X-1
			else:
				#print "New direction = UP"
				direction = UP
				CURR_Y=CURR_Y-1
				continue

		if (direction == UP):
			get_color()

			if (True == prev_y_is_color()):
				CURR_Y=CURR_Y-1
			else:
				#print "New direction = RIGHT"
				direction = RIGHT
				CURR_X=CURR_X+1
				continue

				
	#the while cycle exits when CURR_X and CURR_Y are at position 15,15
	#but we still need to read the RGB values of the color
	#in that position
	if ((CURR_X == 15) and (CURR_Y ==15)):
		get_color()
		print "Finished!"
	
	print_results()


if __name__ == "__main__":
	main()
 

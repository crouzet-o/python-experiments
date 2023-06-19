#!/home/crouzet-o/anaconda3/envs/expe/bin/python3
# -*- coding: utf-8 -*-
#
#
# Display sequences for reading
#
# Initializes a black surface in a window and displays white text on this
# surface from "recording.csv". Manage pauses, interruptions from user and exit
# from the program. The list is randomized.
#

VERSION = "0.0.5"
debug = 0
import wx
tmp = wx.App(False)
screen_size = wx.GetDisplaySize()

blocksize = 72

import datetime
expeStart = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')


import argparse

parser = argparse.ArgumentParser(description='Display text strings for reading from a csv file.', epilog='Copyleft O. Crouzet (2012)')

parser.add_argument('--id', dest='subject', nargs=1,
                   help='Subject ID. Will create a file named "results-"ID".res". If the file exists, it will append data to it (no data will be erased).')

parser.add_argument('--col', dest='n', nargs=1, default='1',
			  help='Select which column number of the file should be displayed (we start at 1, default: N=1 - first column)')

parser.add_argument('--sampa', dest='sampa', nargs=1, default='1',
                   help='Select which column number of the file will be used for recording the SAMPA transcription (default: first column).')

parser.add_argument('--lang', dest='lang', nargs=1, default='fr',
                   help='Select which language (font) we will use for displaying stimuli (default: lang=\'fr\', available = lang=\'ar\')')

parser.add_argument('--rep', dest='nbrep', nargs=1, default='1',
                   help='Select number of repetitions (default: nbrep = 1)')

parser.add_argument('--stimdur', dest='STIMDUR', nargs=1, default='2000',
                   help='Stimulus duration (in ms., default: stimdur = 2000)')

parser.add_argument('--isi', dest='ISI', nargs=1, default='500',
                   help='Inter-Stimulus Interval (ISI) (in ms., default: isi = 500)')

parser.add_argument('--sep', dest='csvsep', nargs=1, default=';',
                   help='Select CSV separator (default: nbrep = \';\')')


parser.add_argument('filename', metavar='file', nargs=1,
                   help='The (CSV) file to be read.')

args = parser.parse_args()
if debug==1:
	print(args.lang,args.n,args.nbrep,args.filename)

subjectid = args.subject[0]
column = int(args.n[0])-1
sampacol = int(args.sampa[0])-1
nbrep = int(args.nbrep[0])
infile = args.filename[0]
language = args.lang[0]
csvsep = args.csvsep[0]

STIMDUR = int(args.STIMDUR[0])
ITI = int(args.ISI[0])

if debug==1:
	print(language,column,nbrep,infile)

try:
	import Caterpyllar as pyl
	import sys
	import string
	import textwrap
	import re
	import random
	import math
	import os
	import getopt
	import pygame
	import time
	import pyfribidi
	from pyfribidi import RTL,LTR,ON
	# from socket import *
	from pygame.locals import * # events, key names (MOUSEBUTTONDOWN,K_r...)
	# from pygame.font import *
	


except ImportError, err:
    print "couldn't load module. %s" % (err)
    sys.exit(2)



resultsfile = 'results-'+subjectid+'.res'
print resultsfile
resdata = pyl.init_resultsfile(resultsfile)


black = 0, 0, 0
white = 250,250,250
bgcolor = white
fgcolor = black

if debug == 1:
	STIMDUR = 180 # Stimulus duration
	ITI = 50 # Instantiate the Inter-Trial Interval duration (in ms.)



# Initialise screen
pygame.init()
##screen = pygame.display.set_mode((1280, 1024)) # Set window size
screen = pygame.display.set_mode(screen_size) # Set window size
pygame.display.set_caption(pyl.__name__+' - Version '+pyl.version)

# Blank Surface
blank = pygame.Surface(screen.get_size())
blank = blank.convert()
blank.fill(bgcolor) # Background color

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bgcolor) # Background color

# Setup fonts for display

# Default parameters
myexpefont = pygame.font.match_font('freeserif,times,freesans,arial')
myexpefontsize = 38
textdirection='LTR'

if language == 'ar':
	#myexpefont = pygame.font.match_font('arab,kacstbook,scheherazade,alarabiya,kacst')
	myexpefont = pygame.font.match_font('timesnewroman,arial,tholoth,scheherazade,tholoth,kacstqurn')
	myexpefontsize = 88
	textdirection='RTL'

if language == 'jp':
    myexpefont = pygame.font.match_font('ipaexmincho,japan')
    myexpefontsize = 48
    textdirection='LTR'

#unicode = pygame.font.Font(unicode, 48)
print myexpefont

myfont = pygame.font.match_font('freesans,arial')
myfontsize = 28

#font = pygame.font.Font(myexpefont, myexpefontsize) # Font name and size
#text = font.render("", 1, fgcolor) # Set text to display, antialiasing and color
#textpos = text.get_rect() # Get surface size information
#textpos.centerx = background.get_rect().centerx # set x position
#textpos.centery = background.get_rect().centery # set y position
#background.blit(text, textpos)

pygame.mouse.set_visible(0)
#pygame.event.set_grab(1) # Grab all events




def main():
	# Blit everything to the screen (Launch the display)
#	screen.blit(background, (0, 0))
#	pygame.display.flip()
	if debug == 0: pygame.display.toggle_fullscreen() # Really necessary?

	stimuli = pyl.read_data_2D(infile,csvsep,1)
	print len(stimuli)
	
	splash()

	for j in range(0,nbrep):
		random.shuffle(stimuli)
		if debug==1:
			print j
		runtheexperiment(stimuli, column)
	
	endsplash()



	
def splash():
	pygame.time.wait(2000)
	display_instruction("Vous allez bientôt commencer l'enregistrement. Vous pouvez à tout moment faire une pause en appuyant sur la barre espace. Pour reprendre l'enregistrement, il vous suffit alors d'appuyer à nouveau sur la barre espace. Vous allez pouvoir commencer. Appuyez sur n'importe quelle touche pour commencer l'enregistrement.")
	waitforkeypress()
	display_instruction("")
	pygame.time.wait(2000)

def runthetraining():
	pygame.time.delay(3000)


def runtheexperiment(data, displaycol):
	trial = 0
	for i in range(0,len(data)):
		catchpause()
		pygame.event.pump()
		pygame.event.clear()
		trial = trial + 1
		tic = starttimer()
		display_text(unicode(data[i][displaycol],'utf8'),textdirection)
		resdata.write(str(expeStart)+data[i][displaycol]+";"+data[i][sampacol]+"\n")
		waittimer(tic,STIMDUR)
		pyl.blank_screen(bgcolor)
		if trial == blocksize:
			trial = 0
			blockpause()
		pygame.time.delay(ITI)
		
	pyl.blank_bg(bgcolor)


def getemergencyquit():
	for event in pygame.event.get():
		if event.type == KEYDOWN:
			pygame.time.wait(100)
			pygame.event.clear()
			quitthegame()

def catchpause():
	pygame.event.pump()
	for event in pygame.event.get():
		if event.type == KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
			if event.key == K_ESCAPE or event.key == K_SPACE:
				display_instruction("Appuyez sur une touche pour reprendre l'enregistrement")
				while 1:
					for event in pygame.event.get():
						if event.type == KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
							if event.key == K_q:
								quitthegame()
							else:
								display_instruction("")
								pygame.time.wait(2000)
								return							
				display_instruction("")
				pygame.time.wait(2000)
				pygame.event.clear()
				return
			return
	pygame.event.clear()


def blockpause():
	pygame.event.pump()
	display_instruction("Appuyez sur une touche pour reprendre l'enregistrement")
	waitforkeypress()
	display_instruction("")
	pygame.time.wait(2000)
	pygame.event.clear()

def waitforkeypress():
	pygame.event.pump()
	while 1:
		for event in pygame.event.get():
			if event.type == KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
				pygame.time.wait(100)
				pygame.event.clear()
				return
	pygame.event.clear()
	
def endsplash():
	pygame.time.wait(2000)
	display_instruction("Merci de votre participation.")
	waitforkeypress()
	if debug == 0: pygame.display.toggle_fullscreen()
	quitthegame()

def quitthegame():
	sys.exit('\ninterrupted by the user !!!')
##	quit()

def display_instruction(string):
	string = textwrap.wrap(string,width=60)
	font = pygame.font.Font(myfont, myfontsize) # Font name and size
	ypos = 100
	screen.fill(bgcolor)
	for i in range(0,len(string)):
		text = font.render(unicode(string[i],'utf8'), 1, fgcolor) # Set text to display, antialiasing and color
		textpos = text.get_rect() # Get surface size information
		textpos.centerx = background.get_rect().centerx # set x position
		textpos.centery = background.get_rect().centery - ypos # set y position
		screen.blit(text, textpos)
		ypos = ypos - (1.5*myfontsize)
	pygame.display.flip()

def display_text(string,direction):
	pygame.font.init()
	font = pygame.font.Font(myexpefont, myexpefontsize) # Font name and size
	#text = font.render(string, 1, (250, 250, 250)) # Set text to display, antialiasing and color
	if direction=='RTL':
		text = font.render(pyfribidi.log2vis(string), 1, fgcolor) # Set text to display, antialiasing and color
		print string,pyfribidi.log2vis(string)
	else:
		text = font.render(string, 1, fgcolor) # Set text to display, antialiasing and color
		print string
	textpos = text.get_rect() # Get surface size information
	textpos.centerx = background.get_rect().centerx # set x position
	textpos.centery = background.get_rect().centery # set y position
	screen.fill(bgcolor)
	screen.blit(text, textpos)
	pygame.display.flip()
	
def randomize(list):
	data = read_data()

def starttimer():
	timer = time.time()*1000 # time in ms
	return timer

def waittimer(timer,duration):
	while ((time.time()*1000)-timer) < duration:
		pygame.time.wait(10)

## 	while 1:
## 		tic = time.time()*1000
## 		if (tic-timer) >= duration:
## 			return

def readtimer(timer,reference):
	timer = (time.time()*1000)-reference
	return timer

if __name__ == '__main__': main()
    
    
# if event.type == QUIT: # QUIT event or keypressed or keydepressed
# Add a test in order to know whether were are in a fullscreen or windowed state
# pygame.display.toggle_fullscreen()

# v_user=raw_input("Enter Username :")
# v_pwd=raw_input("Enter Password :")

## for event in pygame.event.get():
## 	if event.type == QUIT:
## 		return
## 	elif event.type == KEYDOWN:
## 		if event.key == K_UP:
## 			player.moveup()
## 		if event.key == K_DOWN:
## 			player.movedown()
## 	elif event.type == KEYUP:
## 		if event.key == K_UP or event.key == K_DOWN:
## 			player.movepos = [0,0]
## 			player.state = "still"
        
        
    
        
        
## def load_png(name):
##     """ Load image and return image object"""
##     fullname = os.path.join('data', name)
##     try:
##         image = pygame.image.load(fullname)
##         if image.get_alpha() is None:
##             image = image.convert()
##         else:
##             image = image.convert_alpha()
##     except pygame.error, message:
##         print 'Cannot load image:', fullname
##         raise SystemExit, message
##     return image, image.get_rect()

# set font encoding ? (see beginning of the file but != external file encoding
#setdefaultencoding('iso-8859-1') # unrecognized

## Random numbers
## import random
## random.sample(xrange(N),N)
## Extract length of list : len(N)
## cards = range(50)
## random.shuffle(cards)
## cards est randomisé
##
## Define a block size (pause at end of block, wait for keypress, restart...)



#!/usr/bin/python
# -*- coding: utf-8 -*-

# Comment lancer le programme
# ./progression.py --col 1 --sylls 2 --sampa --id essai --rep 5 --timepersyll 200 --blocksize 30 --isi 500 list-nasals-EVA.csv 

VERSION = "0.0.6"
debug = 1

import wx
tmp = wx.App(False)
window_size = wx.GetDisplaySize()
#screen_size = (1280, 1024)



import argparse

parser = argparse.ArgumentParser(description='Display text strings (words, sentences) for reading from a csv file. A progression bar aimed at manipulating the rate of speech production is displayed during reading.', epilog='Copyleft O. Crouzet (2013)')

parser.add_argument('--col', dest='n', nargs=1, default="1",
			  help='Select which column number of the file should be displayed (we start at 1, default: N=1 - first column)')

parser.add_argument('--sampa', dest='sampa', nargs=1, default="2",
                   help='Select which column number of the file will be used for recording the SAMPA transcription (default: second column).')

parser.add_argument('--sylls', dest='sylls', nargs=1, default="3",
                   help='Select which column number of the file contains the number of syllables used for controlling display rate (default: third column).')

parser.add_argument('--fontsize', dest='fontsize', nargs=1, default="30",
                   help='Select font size for displaying stimuli (default: fontsize="30")')

parser.add_argument('--lang', dest='lang', nargs=1, default='fr',
                   help='Select which language (font) we will use for displaying stimuli (default: lang=\'fr\', available = lang=\'ar\')')

parser.add_argument('--read', dest='read', nargs=1, default='False',
                   help='Select whether we start with a reading familiarisation phase (default: read=\'False\', available = read=\'True\')')

parser.add_argument('--id', dest='subject', nargs=1,
                   help='Subject ID. Will create a file named "results-"ID".res". If the file exists, it will append data to it (no data will be erased).')

parser.add_argument('--rep', dest='nbrep', nargs=1, default="1",
                   help='Select number of repetitions (default: nbrep = 1)')

#parser.add_argument('--stimdur', dest='STIMDUR', nargs=1, default=2000,
#                   help='Stimulus duration (in ms., default: stimdur = 2000)')

parser.add_argument('--timepersyll', dest='timepersyll', nargs=1, default="200",
                   help='Time per syllable for computing display speed (in ms., default: timepersyll = 200)')

parser.add_argument('--blocksize', dest='blocksize', nargs=1, default="20",
                   help='Number of trials until a pause is automatically inserted (default: 20)')

parser.add_argument('--isi', dest='ISI', nargs=1, default=500,
                   help='Inter-Stimulus Interval (ISI) (in ms., default: isi = 500)')


parser.add_argument('filename', metavar='file', nargs=1,
                   help='The (CSV) file to be read.')

args = parser.parse_args()
if debug==1:
	print("Arguments = ",args.lang,args.n,args.lang,args.fontsize,args.nbrep,args.filename,args.ISI,args.timepersyll,args.sylls)

column = int(args.n[0])-1
sampacol = int(args.sampa[0])-1
nbsylls = int(args.sylls[0])-1
blocksize = int(args.blocksize[0])
fontsize = int(args.fontsize[0])

nbrep = int(args.nbrep[0])

infile = args.filename[0]
language = args.lang[0]
subjectid = args.subject[0]
read = args.read[0]

#STIMDUR = int(args.STIMDUR)
ITI = int(args.ISI[0])
timepersyll = int(args.timepersyll[0])

if debug==1:
	print(language,column,nbrep,infile,read)

    
#from string import replace
#import pygame
#import time
#from pygame.locals import * # events, key names (MOUSEBUTTONDOWN,K_r...)
#from pygame import *



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
    print("couldn't load module. %s" % (err))
    SystemExit(2)


pyl.sayhi()

resultsfile = 'resultats-'+subjectid+'.res'
print("Results file = ",resultsfile,"\n")
resdata = pyl.init_resultsfile(resultsfile)


# Miscellaneous color definitions (Vectors with 3 values, 0 -> 255,
# RGB color format)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (125, 125, 125)
red = (255, 0, 0)
blue = (136,162,183)
bgcolor = white
fgcolor = black

# Pre-initialisation of the Sound Mixer (need to be loaded before
# other initialisations)
pygame.mixer.pre_init()

# Graphical window initialization. "window" is the parent Surface. All
# these lines must be placed outside functions as the corresponding
# objects / variables have to be "global", i.e. globally available for
# any function.



pygame.init() # Initialize Pygame (call pygame.display.init())

#window_size = (800,600) # Either we set a fixed resolution, either we
# select the best one from available modes
#resolutions = pygame.display.list_modes()
#print resolutions
#best_resolution = resolutions[0]
#window_size = best_resolution


# Set window size and launch this window as the parent surface
# (automatically with a black background).
#window = pygame.display.set_mode(window_size, pygame.HWSURFACE)
window = pygame.display.set_mode(window_size, pygame.FULLSCREEN) # pygame.OPENGL


pygame.mouse.set_visible(0) # Make the mouse cursor invisible (0) or
# visible (1)
pygame.event.set_grab(0) # If 1, catch all input events (keyboard and
# mouse), prevent mouse from leaving the
# Pygame window

# Note that the variables "window" and "background" thereafter are
# "objects" (according to the meaning it receives in "object oriented
# programming"). Once an object is created, you may apply functions on
# it very easily (cf functions defined thereafter like splash or
# blank_screen) using window.function, background.function...

# In order to "draw" on this window, we need to create a surface on
# it. We call it "background".

background = pygame.Surface(window.get_size()) # Create a surface the
                                               #size of the window.
background = background.convert() # Convert the surface with the same
                                  #pixel format as the preceding
                                  #one(s). Useful for display speed.

background.fill(bgcolor) # Set a color to fill "background"
window.blit(background, (0,0)) # Draw the modified color on the
    # display

# Be careful, each time we set modifications on a surface (color,
# text...) we need to call pygame.display.flip() to actually display
# these modifications...

pygame.display.flip() # Launch the modifications (update the display)

pygame.time.delay(ITI) # pygame.time.delay takes time values in
                       #milliseconds

#timepersyll = 120
                       
def main():
    ## Phase d'initialisation
    text = "Initialisation de l'affichage"
    #textsurface,textposition = display_text(text)
    nbsyll=9
    #pause(500)
    blank_bg(white)
    #pause(500)
    textsurface,textposition = display_text(text)
    text_progressionbar_grow(textposition,nbsyll,timepersyll,blue) # (width, nb_syll,
    pause(2000)
    liste = pyl.read_data_2D(infile,";",1)

    if debug==1:
        print(len(liste))
    
    # Phase de préparation lecture
    if read == "True":
        random.shuffle(liste)
        splash_text("Vous allez commencer par vous familiariser avec les séquences que vous devrez lire.")
        pause(ITI)
        for i in range(len(liste)):
            j="reading"
            readingphase(liste,i,j)


    # Phase de Training pour le débit
    random.shuffle(liste)
    splash_text("Appuyez sur une touche pour commencer la phase d'entraînement")
    pause(ITI)
    for i in range(10):
        j="training"
        catchpause()
        runtheexperiment(liste,i,j)
    
    # Phase de Test
    splash_text("Appuyez sur une touche pour commencer l'expérience...")
    pause(ITI)
    trial=0
    for j in range(0,nbrep):
        random.shuffle(liste)
        if debug==1:
            print("j = ",j)
        for i in range(0,len(liste)):
            catchpause()
            trial+=1
            if trial == blocksize:
                trial = 0
                blockpause()
            runtheexperiment(liste,i,j)


def catchpause():
	pygame.event.pump()
	for event in pygame.event.get():
		if event.type == KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
			if event.key == K_ESCAPE or event.key == K_SPACE:
				display_text("Appuyez sur une touche pour reprendre l'enregistrement")
				while 1:
					for event in pygame.event.get():
						if event.type == KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
							if event.key == K_q:
								pyl.quitthegame()
							else:
								display_text("")
								return							
				display_text("")
				pygame.time.wait(500)
				pygame.event.clear()
				return
			return
	pygame.event.clear()



def blockpause():
	pygame.event.pump()
	display_text("Appuyez sur une touche pour reprendre l'enregistrement")
	pyl.waitforkeypress()
	display_text("")
	pygame.time.wait(500)
	pygame.event.clear()


def runtheexperiment(liste,i,j):
    if debug==1:
        print("i, nbsylls, column = ",i,nbsylls,column)
    stimulus = liste[i][column]
    #nbsylls = int(liste[i][1])
    nbsyll = int(liste[i][nbsylls])
    if debug==1:
        print("stimulus = ",stimulus,"\n")
    #textsurf = display_text(stimulus)
    blank_bg(white)
    #vblinkbar(35,window_size[1],1,500,blue) # (width, height,
    #nb_blinks, rate (ms), #bar_color)
    resdata.flush()
    #textsurface,textposition = display_text(stimulus)
    #pause(ITI)
    #blank_bg(white)
    #pause(ITI)
    textsurface,textposition = display_text(stimulus)
    #pause(ITI)
    #print(textsurface,textposition,"\n" # bar = vprogressionbar_init(15,10,grey)) #
                            #(width,init_height,bar_color)
    #vprogressionbar_grow(35,length,timepersyll,red) # (width, nb_syll,
                                               #time_per_syll,bar_color)
                                               #pause(100)
    text_progressionbar_grow(textposition,nbsyll,timepersyll,blue) # (width, nb_syll,
                                               #time_per_syll,bar_color)
    savedata = liste[i][column]+";"+liste[i][nbsylls]+";"+liste[i][0]+";"+liste[i][1]+";"+liste[i][2]+";"+liste[i][3]+";"+str(i)+";"+str(j)+";"+str(timepersyll)+"\n"
    print(savedata)
    resdata.write(savedata)
    #pause(100)
    #blank_bg(white)
    #	display_image("material/images/head.jpg")
    #	waitforspacekey()
    #	pause(ITI)
    #	blank_bg(bgcolor)
    #	pause(ITI)
    #	play_sound("material/sounds/dave.wav")
    #	pause(ITI)
    #	splash_image("material/images/head.png")
    #	pause(ITI)
    blank_bg(white)
    pause(ITI)


def readingphase(liste,i,j):
    if debug==1:
        print("i, nbsylls, column = ",i,nbsylls,column)
    stimulus = liste[i][column]
    #nbsylls = int(liste[i][1])
    nbsyll = int(liste[i][nbsylls])
    if debug==1:
        print("stimulus = ",stimulus,"\n")
    #textsurf = display_text(stimulus)
    blank_bg(white)
    #vblinkbar(35,window_size[1],1,500,blue) # (width, height,
    #nb_blinks, rate (ms), #bar_color)
    resdata.flush()
    textsurface,textposition = display_text(stimulus)
    pyl.waitforkeypress()
    blank_bg(white)
    pause(ITI)
    #textsurface,textposition = display_text(stimulus)
    #pause(ITI)
    #print(textsurface,textposition,"\n" # bar = vprogressionbar_init(15,10,grey)) #
                            #(width,init_height,bar_color)
    #vprogressionbar_grow(35,length,timepersyll,red) # (width, nb_syll,
                                               #time_per_syll,bar_color)
                                               #pause(100)
    #text_progressionbar_grow(textposition,nbsyll,timepersyll,blue) # (width, nb_syll,
                                               #time_per_syll,bar_color)
    #savedata = liste[i][column]+";"+liste[i][nbsylls]+";"+liste[i][0]+";"+liste[i][1]+";"+liste[i][2]+";"+liste[i][3]+";"+str(i)+";"+str(j)+";"+str(timepersyll)+"\n"
    #print(savedata)
    #resdata.write(savedata)
    #pause(100)
    #blank_bg(white)
    #	display_image("material/images/head.jpg")
    #	waitforspacekey()
    #	pause(ITI)
    #	blank_bg(bgcolor)
    #	pause(ITI)
    #	play_sound("material/sounds/dave.wav")
    #	pause(ITI)
    #	splash_image("material/images/head.png")
    #	pause(ITI)
    

def splash_text(text):
    blank_bg(white)
    display_text(text)
    pyl.waitforkeypress()
    blank_bg(white)


def blank_bg(color):
    background.fill(color)
    window.blit(background, (0,0))
    pygame.display.flip()

def pause(ms):
	pygame.time.delay(ms)

def display_text(text): # Display text
    font = pygame.font.Font(pygame.font.match_font('arial'), fontsize) # Font name and size
    text = font.render(unicode(text,'utf8'), 1, fgcolor) # Set text to display,
						# antialiasing boolean
						# and color
    textpos = text.get_rect() # Get coordinates of the surface
				# needed for text display
    textsize = text.get_size()
    textpos.centerx = background.get_rect().centerx # set text
							# x-position
							# centered
    textpos.centery = background.get_rect().centery # set text
							# y-position
							# centered
    background.fill(bgcolor) # Blank the background surface
    window.blit(background, (0,0)) # Blit it
    window.blit(text, textpos) # Blits the text to the coordinates
    pygame.display.flip() # Flip the display
    return textsize,textpos


def display_image(filename): # Display an image from disk
    splash = pygame.image.load(filename)
    splashpos = splash.get_rect()
    splashpos.centerx = background.get_rect().centerx
    splashpos.centery = background.get_rect().centery
    blank_bg(bgcolor)
    window.blit(background, (0,0))
    window.blit(splash,splashpos)
    pygame.display.flip()
	

def play_sound(filename): # Play a sound from disk
	buzz = pygame.mixer.Sound(filename) # Load the sound file (wav
						# format)
	duration = int(buzz.get_length()*1000) # Get its duration in
						# ms
	buzz.play() # Play the file
	pygame.time.delay(duration) # Wait until it's finished playing


def blank_screen():
	window.fill(black)
	window.blit(background, (0, 0))

	

def splash_image(filename): # Display an image from disk for a number
				# of milliseconds as precisely as possible
				# (around 10ms accuracy).
	splash = pygame.image.load(filename)
	splashpos = splash.get_rect()
	splashpos.centerx = background.get_rect().centerx
	splashpos.centery = background.get_rect().centery
	blank_bg(bgcolor)
	window.blit(background, (0,0))
	window.blit(splash,splashpos)
	tic = starttimer()
	pygame.display.flip()
	waittimer(tic,1000)
	blank_bg(bgcolor)
	window.blit(background, (0,0))
	pygame.display.flip()



def starttimer(): # Launch a timer
	timer = time.time()*1000 # time in ms
	return timer

def waittimer(timer,duration): # Wait until timer reaches duration
	while ((time.time()*1000)-timer) < duration:
		pygame.time.delay(5)

def readtimer(timer,reference): # Read time spent since reference
				# timer was launched
	timer = (time.time()*1000)-reference
	return timer


def vprogressionbar_init(width,init_height,bar_color):
	bar = pygame.Surface((width,init_height))
	bar = bar.convert()
	bar.fill(bar_color)
	window.blit(bar, (0,window_size[1]-init_height))
	pygame.display.flip()
	return bar,width,init_height

def vblinkbar(width,height,nb_blinks,rate,bar_color):
	width = int(0.02*window_size[0])
	bar = pygame.Surface((width,height))
	bar = bar.convert()
	for i in range(0,nb_blinks):
		bar.fill(bar_color)
		window.blit(bar, (0,0))
		window.blit(bar, (window_size[0]-width,0))
		pygame.display.flip()
		pause(rate)
		bar.fill(white)
		window.blit(bar, (0,0))
		window.blit(bar, (window_size[0]-width,0))
		pygame.display.flip()
        pause(rate)
	return bar,width,height

def vprogressionbar_grow(width,nb_syll,time_per_syll,bar_color): # Need to
	# compute time from beginning to end of window
	width = int(0.02*window_size[0])
	height=0 #initial vertical height
	nbsteps = 20 #100
	stepsize = window_size[1]/nbsteps #
	while height <= window_size[1]:
		bar_l = pygame.Surface((width,height))
		bar_l = bar_l.convert()
		bar_l.fill(bar_color)
		window.blit(bar_l, (0,window_size[1]-height))

		bar_r = pygame.Surface((width,height))
		bar_r = bar_r.convert()
		bar_r.fill(bar_color)
		window.blit(bar_r, (window_size[0]-width,window_size[1]-height))

		height+=stepsize
#		print(nb_syll,time_per_syll,window_size[1],stepsize)
#		print((nb_syll*time_per_syll/nbsteps),"\n")
		pause(nb_syll*time_per_syll/nbsteps)
#		pause(5)
		pygame.display.flip()
	final_blank=0
	if final_blank==1:
		blank_bg(bar_color)
		window.blit(background, (0,0))
		pygame.display.flip()
#	return name,height




def text_progressionbar_grow(space,nb_syll,time_per_syll,bar_color,direction): # Need to
    # compute time from beginning to end of window
    #
    # TODO: set default value for direction in order to keep compatibility with
    # previous versions not implementing direction.
    #
    cwidth=0
    width = space[2] #int(0.02*window_size[0])
    height= space[3] #initial vertical height
    xref = space[0]
    yref = space[1]+height
    if debug==1:
        print(xref, yref, width, height)

    pygame.display.flip()
    #pause(1000)
    nbsteps = 40 #100
    stepsize = width/nbsteps #
    if debug==1:
        print(stepsize)
    while cwidth <= width:
        hbar = pygame.Surface((cwidth,height))
        hbar = hbar.convert()
        hbar.fill(bar_color)
        window.blit(hbar, (xref,yref))
        cwidth+=stepsize
        #		print(nb_syll,time_per_syll,window_size[1],stepsize)
        #		print((nb_syll*time_per_syll/nbsteps),"\n")
        if debug==1:
                print(nb_syll,time_per_syll,nbsteps)
        pause(nb_syll*time_per_syll/nbsteps)
        #		pause(5)
        pygame.display.flip()
        final_blank=0
    if final_blank==1:
        blank_bg(bar_color)
        window.blit(background, (0,0))
        pygame.display.flip()
        #	return name,height















## Exercices : Lire un fichier texte et afficher la liste des mots au
## centre de l'écran.  Lire un fichier contenant des noms de fichiers
## correspondant à des images et afficher chaque image 200ms avec
## 500ms d'intervalle.








# FUNCTIONS


#def read_data(filepath): # Function to load the contents of a text
#			# file into a 2D table
#	table=[] # Create an empty list
#	datafile=open(filepath,'r') # Open file for reading
#	for line in datafile.readlines(): # For each line in the text
#					# file This keeps \n at end
#					# of line
#		cleandata = replace(line,'\n','') # Remove \n at end
#						# of line (from
#						# string.replace)
#		oneline = re.split(";",cleandata) # Split file at
#						# commas
#		table.append(oneline) # Append the line at end of
#					# table
#	datafile.close() # Close the file
#	return table


def cleanup(line):
	data = replace(line,'\n','')
	data = replace(data,'\"','')
	data = replace(data,'\'','')
	return data

def load_data():
	data = read_data(sys.argv[1])
	return data

# MAIN
main()

#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Added chinese font display argument
# Added boolean toggle for progression bar
# TODO: reintroduce RTL / pyfribidi controls for arabic

# Comment lancer le programme
# ./progression.py --col 1 --sylls 2 --sampa --id essai --rep 5 --timepersyll 200 --blocksize 30 --isi 500 list-nasals-EVA.csv 

VERSION = "0.0.7"
DEBUG = False

# These parameters should be controlled from the parsed arguments on
# the command line or from a config file (cf. argparse vs. configargparse).
PROGRESSION_DISPLAY = True

import wx
tmp = wx.App(False)
window_size = wx.GetDisplaySize()
#screen_size = (1280, 1024)


import datetime
expeStart = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')


import argparse

parser = argparse.ArgumentParser(description='Display text strings (words, sentences) for reading from a csv file. A progression bar aimed at manipulating the rate of speech production is displayed during reading.', epilog='Copyleft O. Crouzet (2013)')

parser.add_argument('--col', dest='n', nargs=1, default="1", 
                    help='Select which column number of the file should be displayed (we start at 1, default: N=1 - first column)')

parser.add_argument('--sampa', dest='sampa', nargs=1, default="2",
        help='Select which column number of the file will be used for recording the SAMPA transcription (default: second column).')

parser.add_argument('--sylls', dest='sylls', nargs=1,
        help='Select which column number of the file contains the number of syllables used for controlling display rate (default: third column).')
#parser.add_argument('--sylls', dest='sylls', nargs=1, default="3",
#        help='Select which column number of the file contains the number of syllables used for controlling display rate (default: third column).')

parser.add_argument('--fontsize', dest='fontsize', nargs=1, default="30",
                    help='Select font size for displaying stimuli (default: fontsize="30")')

parser.add_argument('--lang', dest='lang', nargs=1, default='fr',
        help='Select which language (font) we will use for displaying stimuli (default: lang=\'fr\', available = lang=\'ar\')')

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

parser.add_argument('--famread', dest='famread', nargs=1, default='False',
        help='Select whether we start with a reading familiarisation phase (default: read=\'False\', available = read=\'True\')')

parser.add_argument('--preread', dest='preread', nargs=1, default='False',
        help='Select whether we start each trial with displaying the text (default: read=\'False\', available = read=\'True\')')

parser.add_argument('filename', metavar='file', nargs=1,
                   help='The (CSV) file to be read.')

args = parser.parse_args()
if DEBUG:
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
FAMREAD = args.famread[0]
PREREAD = args.preread[0]

#STIMDUR = int(args.STIMDUR)
ITI = int(args.ISI[0])
timepersyll = int(args.timepersyll[0])

if DEBUG:
        print(language, column,nbrep,infile,FAMREAD,PREREAD)

    
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
        import numpy as np
        from pyfribidi import RTL,LTR,ON
        # from socket import *
        from pygame.locals import * # events, key names (MOUSEBUTTONDOWN,K_r...)
        # from pygame.font import *
except ImportError as err:
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
lightblue = (105, 160, 170)
darkblue = (78, 120, 127)
bgcolor = lightblue
fgcolor = white # black

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

if DEBUG:
        window = pygame.display.set_mode(window_size)
else:
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

if language == 'cjk':
        myexpefont = pygame.font.match_font('\
        arplumingcn, \
        arpluminghk, \
        arplumingtw, \
        arplumingtwmbe, \
        arplukaicn, \
        arplukaihk, \
        arplukaitw, \
        arplukaitwmbe, \
        arplsungtilgb, \
        arplkaitimgb, \
        arplkaitimbig5, \
        arplmingti2lbig5, \
        droidsansfallback, \
        wenquanyimicrohei, \
        wenquanyizenhei, \
        notosanscjkkr, \
        notosanscjkjp, \
        notoserifcjkkr, \
        notosanscjktc, \
        notosansmonocjksc, \
        notosansmonocjkjp, \
        notoserifcjksc, \
        notoserifcjktc, \
        notoserifcjkjp, \
        notosansmonocjktc, \
        notosansmonocjkkr, \
        notosanscjksc', bold=False)
        myexpefont = 'fonts/uming.ttc'
        myexpefontsize = 48
        textdirection='LTR'

#unicode = pygame.font.Font(unicode, 48)
print(myexpefont)

myfont = pygame.font.match_font('freesans,arial')
myfontsize = 28


def main():
        ## Phase d'initialisation
        text = "Initialisation de l'affichage"
        #textsurface,textposition = display_text(text)
        nbsyll=9
        #pause(500)
        blank_bg(bgcolor)
        #pause(500)
        textsurface,textposition = display_text(text)
        text_progressionbar_grow(textposition, nbsyll, timepersyll, darkblue) # (width, nb_syll)
        pause(2000)
        liste = pyl.read_data_2D(infile, ";", 1)

        if DEBUG:
                print(len(liste))
        
        # Phase de préparation lecture
        if PREREAD == "True":
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
                runTheTrial(liste, i, j)
        
        # Phase de Test
        splash_text("Appuyez sur une touche pour commencer l'expérience...")
        pause(ITI)
        trial=0
        for j in range(0,nbrep):
                random.shuffle(liste)
                if DEBUG:
                        print("j = ",j)
                for i in range(0,len(liste)):
                        catchpause()
                        trial+=1
                        if trial == blocksize:
                                trial = 0
                                blockpause()
                        runTheTrial(liste, i, j)


def catchpause():
        pygame.event.pump()
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                                display_text("Appuyez sur une touche pour reprendre l'enregistrement")
                                while 1:
                                        for event in pygame.event.get():
                                                if event.type == pygame.KEYDOWN: # or event.type == KEYUP: # QUIT event or keypressed or keydepressed
                                                        if event.key == pygame.K_q:
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


def runTheTrial(liste, i, j):
        """Documentation 

        IMPORTANT: This function launches one single trial of the
        experiment. It must therefore be included in a loop.

        liste = a list of lists (2D table) containing the control data
        for the experiment 

        i = a scalar providing the line number in liste

        j = a string providing information concerning the trial
        (e.g. is it a 'training' trial or an 'experimental' trial (it
        may also be a number identifiying the trial position)

        column = a global variable (cf. arguments) providing the
        column to display in liste

        """
        if DEBUG:
                print("i, nbsylls, column = ", i, nbsylls, column)
                print(liste[i][nbsylls])
                print("lines, columns = ", len(liste), len(liste[0]))
        stimulus = liste[i][column]
        #nbsylls = int(liste[i][1])
        nbsyll = int(liste[i][nbsylls])
        if DEBUG:
                print("stimulus = ",stimulus,"\n")
        #textsurf = display_text(stimulus)
        blank_bg(bgcolor)
        #vblinkbar(35,window_size[1],1,500,blue) # (width, height,
        #nb_blinks, rate (ms), #bar_color)
        resdata.flush()
        #textsurface,textposition = display_text(stimulus)
        #pause(ITI)
        #blank_bg(bgcolor)
        #pause(ITI)
        if PREREAD:
                textsurface,textposition = display_textexpe(stimulus)
                pause(2 * nbsyll * timepersyll)
                blank_bg(red)
                textsurface,textposition = display_textexpe(stimulus, bgcolor=red)
                pause(ITI)
                blank_bg(bgcolor)
        #print(textsurface,textposition,"\n") # bar = vprogressionbar_init(15,10,grey) #
        #(width,init_height,bar_color)
        #vprogressionbar_grow(35,length,timepersyll,red) # (width, nb_syll,
        #time_per_syll,bar_color)
        #pause(100)
        textsurface,textposition = display_textexpe(stimulus)
        if PROGRESSION_DISPLAY:
                text_progressionbar_grow(textposition, nbsyll, timepersyll, darkblue) # (width, nb_syll,
                #time_per_syll,bar_color)
        else:
                pause(nbsyll * timepersyll)

        savedata = liste[i][column]+";"+liste[i][nbsylls]+";"+liste[i][0]+";"+liste[i][1]+";"+liste[i][2]+";"+liste[i][3]+";"+str(i)+";"+str(j)+";"+str(timepersyll)+"\n"
        print(savedata)
        resdata.write(savedata)
        #pause(100)
        #blank_bg(bgcolor)
        #   display_image("material/images/head.jpg")
        #   waitforspacekey()
        #   pause(ITI)
        #   blank_bg(bgcolor)
        #   pause(ITI)
        #   play_sound("material/sounds/dave.wav")
        #   pause(ITI)
        #   splash_image("material/images/head.png")
        #   pause(ITI)
        blank_bg(bgcolor)
        pause(ITI)


def readingphase(liste, i, j):
    if DEBUG:
        print("i, nbsylls, column = ",i,nbsylls,column)
    stimulus = liste[i][column]
    #nbsylls = int(liste[i][1])
    nbsyll = int(liste[i][nbsylls])
    if DEBUG:
        print("stimulus = ",stimulus,"\n")
    #textsurf = display_text(stimulus)
    blank_bg(bgcolor)
    #vblinkbar(35,window_size[1],1,500,blue) # (width, height,
    #nb_blinks, rate (ms), #bar_color)
    resdata.flush()
    textsurface,textposition = display_textexpe(stimulus)
    pyl.waitforkeypress()
    blank_bg(bgcolor)
    pause(ITI)
    #textsurface,textposition = display_text(stimulus)
    #pause(ITI)
    #print(textsurface,textposition,"\n") # bar = vprogressionbar_init(15,10,grey) #
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
    #blank_bg(bgcolor)
    #   display_image("material/images/head.jpg")
    #   waitforspacekey()
    #   pause(ITI)
    #   blank_bg(bgcolor)
    #   pause(ITI)
    #   play_sound("material/sounds/dave.wav")
    #   pause(ITI)
    #   splash_image("material/images/head.png")
    #   pause(ITI)
    

def splash_text(text):
    blank_bg(bgcolor)
    display_text(text)
    pyl.waitforkeypress()
    blank_bg(bgcolor)


def blank_bg(color):
    background.fill(color)
    window.blit(background, (0,0))
    pygame.display.flip()

def pause(ms):
        pygame.time.delay(ms)

def display_textexpe(text, bgcolor = bgcolor, dfont=pygame.font.Font(myexpefont, myexpefontsize)): # Display text
    font = dfont # Font name and size
    text = font.render(text, 1, fgcolor) # Set text to display,
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
    return(textsize,textpos)


def display_text(text, dfont=pygame.font.Font(pygame.font.match_font('arial'), fontsize)): # Display text
    font = dfont # Font name and size
    text = font.render(text, 1, fgcolor) # Set text to display,
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
    return(textsize,textpos)


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
        return(timer)

def waittimer(timer,duration): # Wait until timer reaches duration
        while ((time.time()*1000)-timer) < duration:
                pygame.time.delay(5)

def readtimer(timer,reference): # Read time spent since reference
                                # timer was launched
        timer = (time.time()*1000)-reference
        return(timer)


def vprogressionbar_init(width,init_height,bar_color):
        bar = pygame.Surface((width,init_height))
        bar = bar.convert()
        bar.fill(bar_color)
        window.blit(bar, (0,window_size[1]-init_height))
        pygame.display.flip()
        return(bar,width,init_height)

def vblinkbar(width,height,nb_blinks,rate,bar_color):
        width = int(0.02*window_size[0])
        bar = pygame.Surface((width,height))
        bar = bar.convert()
        for i in range(0,nb_blinks):
                bar.fill(bar_color)
                window.blit(bar, (0,0))
                window.blit(bar, (window_size[0]-width, 0))
                pygame.display.flip()
                pause(rate)
                bar.fill(bgcolor)
                window.blit(bar, (0,0))
                window.blit(bar, (window_size[0]-width,0))
                pygame.display.flip()
        pause(rate)
        return(bar,width,height)

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
#               print(nb_syll,time_per_syll,window_size[1],stepsize)
#               print((nb_syll*time_per_syll/nbsteps),"\n")
                pause(nb_syll*time_per_syll/nbsteps)
#               pause(5)
                pygame.display.flip()
        final_blank=0
        if final_blank==1:
                blank_bg(bar_color)
                window.blit(background, (0,0))
                pygame.display.flip()
#       return(name,height)




def text_progressionbar_grow(space, nb_syll, time_per_syll, bar_color): # Need to
    # compute time from beginning to end of window
    cwidth=0
    width = space[2] #int(0.02*window_size[0])
    height= space[3] #initial vertical height
    xref = space[0]
    yref = space[1]+height
    if DEBUG:
        print(xref, yref, width, height)
    
    pygame.display.flip()
    #pause(1000)
    nbsteps = 40 #100
    stepsize = width/nbsteps #
    if DEBUG:
        print(stepsize)
    while cwidth <= width:
        hbar = pygame.Surface((cwidth,height))
        hbar = hbar.convert()
        hbar.fill(bar_color)
        window.blit(hbar, (xref,yref))
        cwidth+=stepsize
        #               print(nb_syll,time_per_syll,window_size[1],stepsize)
        #               print((nb_syll*time_per_syll/nbsteps),"\n")
        if DEBUG:
                print(nb_syll,time_per_syll,nbsteps)
                print(nb_syll*time_per_syll/nbsteps)
        pause(round(nb_syll*time_per_syll/nbsteps))
        #               pause(5)
        pygame.display.flip()
        final_blank=0
    if final_blank==1:
        blank_bg(bar_color)
        window.blit(background, (0,0))
        pygame.display.flip()
        #       return(name,height)















## Exercices : Lire un fichier texte et afficher la liste des mots au
## centre de l'écran.  Lire un fichier contenant des noms de fichiers
## correspondant à des images et afficher chaque image 200ms avec
## 500ms d'intervalle.








# FUNCTIONS


#def read_data(filepath): # Function to load the contents of a text
#                       # file into a 2D table
#       table=[] # Create an empty list
#       datafile=open(filepath,'r') # Open file for reading
#       for line in datafile.readlines(): # For each line in the text
#                                       # file This keeps \n at end
#                                       # of line
#               cleandata = replace(line,'\n','') # Remove \n at end
#                                               # of line (from
#                                               # string.replace)
#               oneline = re.split(";",cleandata) # Split file at
#                                               # commas
#               table.append(oneline) # Append the line at end of
#                                       # table
#       datafile.close() # Close the file
#       return(table)


def cleanup(line):
        data = replace(line,'\n','')
        data = replace(data,'\"','')
        data = replace(data,'\'','')
        return(data)

def load_data():
        data = read_data(sys.argv[1])
        return(data)

# MAIN
main()

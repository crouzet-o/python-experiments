#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:16:53 2019

@author: OlivierCrouzet
"""

import pygame

black = 0, 0, 0
white = 250,250,250
red = 250,0,0
bgcolor = white
fgcolor = red

# Initialise screen
screen_size= (800,600)
pygame.init()
##screen = pygame.display.set_mode((1280, 1024)) # Set window size
screen = pygame.display.set_mode(screen_size) # Set window size

# Blank Surface
blank = pygame.Surface(screen.get_size())
blank = blank.convert()
blank.fill(bgcolor) # Background color

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bgcolor) # Background color

# Default parameters
myexpefont = pygame.font.match_font('freesans,arial')
myexpefontsize = 38
textdirection='LTR'


print(myexpefont)

pygame.time.wait(1000)

print(fgcolor,bgcolor)

pygame.font.init()
string='test de polices / affichage'
font = pygame.font.Font(myexpefont, myexpefontsize) # Font name and size
text = font.render(string, 1, fgcolor) # Set text to display, antialiasing and color
print(string)

textpos = text.get_rect() # Get surface size information
textpos.centerx = background.get_rect().centerx # set x position
textpos.centery = background.get_rect().centery # set y position

screen.fill(bgcolor)
screen.blit(text, textpos)
pygame.display.flip()
pygame.time.wait(2000)

screen.fill(fgcolor)
text = font.render(string, 1, bgcolor) # Set text to display, antialiasing and color
screen.blit(text, textpos)
pygame.display.flip()
pygame.time.wait(2000)

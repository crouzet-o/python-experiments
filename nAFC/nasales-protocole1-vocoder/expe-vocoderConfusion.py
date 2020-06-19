#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/opt/local/bin/python

debug=0

#sujet = raw_input("ID du sujet :") # Utiliser wxpython pour faire
                                   # apparaître un widget demandant le
                                   # numéro du sujet.

#expenum = "C" ##raw_input("Id de l'expérience (C: Consonnes, V:Voyelles) :") # Utiliser
                                                                         # wxpython
                                                                         # pour
                                                                         # faire
                                                                         # apparaître
                                                                         # un
                                                                         # widget
                                                                         # demandant
                                                                         # le
                                                                         # numéro
                                                                         # du
                                                                         # sujet.


import argparse

parser = argparse.ArgumentParser(description='Phonetic confusion experiment.', epilog='Copyleft O. Crouzet (2012)')

parser.add_argument('--id', dest='subject', nargs=1,
                   help='Subject ID.')

parser.add_argument('--expe', dest='expe', nargs=1, default='C',
			  help='Select experiment id (C vs. V)')

#parser.add_argument('--sampa', dest='sampa', nargs=1, default='1',
#                   help='Select which column number of the file will be used for recording the SAMPA transcription (default: first column).')

#parser.add_argument('--lang', dest='lang', nargs=1, default='fr',
#                   help='Select which language (font) we will use for displaying stimuli (default: lang=\'fr\', available = lang=\'ar\')')

#parser.add_argument('--rep', dest='nbrep', nargs=1, default='1',
#                   help='Select number of repetitions (default: nbrep = 1)')

#parser.add_argument('--stimdur', dest='STIMDUR', nargs=1, default='2000',
#                   help='Stimulus duration (in ms., default: stimdur = 2000)')

#parser.add_argument('--isi', dest='ISI', nargs=1, default='500',
#                   help='Inter-Stimulus Interval (ISI) (in ms., default: isi = 500)')

#parser.add_argument('--sep', dest='csvsep', nargs=1, default=';',
#                   help='Select CSV separator (default: nbrep = \';\')')


#parser.add_argument('filename', metavar='file', nargs=1,
#                   help='The (CSV) file to be read.')

args = parser.parse_args()
if debug==1:
	print args.lang,args.n,args.nbrep,args.filename

sujet = args.subject[0] ##int(args.subject[0])-1 ##args.subject[0]
expenum = args.expe[0] ##int(args.n[0])-1
#sampacol = int(args.sampa[0])-1
#nbrep = int(args.nbrep[0])
#infile = args.filename[0]
#language = args.lang[0]
#csvsep = args.csvsep[0]

#STIMDUR = int(args.STIMDUR[0])
#ITI = int(args.ISI[0])

import wx
tmp = wx.App(False)
screen_size = wx.GetDisplaySize()

trainingsize=12

import Caterpyllar as pyllar

import sys
import locale
import re
import string
import pygame
from pygame.locals import * # events, key names (MOUSEBUTTONDOWN,K_r...)
import time
import scipy
import random

pyllar.sayhi()

import codecs # Permet de convertir un fichier en lecture / écriture en unicode
sys.getdefaultencoding()


#screen = pygame.display.set_mode(screen_size) # Set window size
pygame.display.set_caption(pyllar.__name__+' - Version '+pyllar.version)



##import alsaaudio
##cards = alsaaudio.cards()
##mixers_list = alsaaudio.mixers()
##mixer = alsaaudio.Mixer(control="Master")
###headphone = alsaaudio.Mixer(control="Headphone")
###headphone = alsaaudio.Mixer(control="default")
##headphone = alsaaudio.Mixer()
###pcm = alsaaudio.Mixer(control="PCM")
##pcm = alsaaudio.Mixer()
##vol = 65
###mixer.getvolume()
##mixer.setvolume(vol)
##headphone.setvolume(vol)
##pcm.setvolume(vol)

from pulsectl import Pulse

pulse = Pulse("computer")
output = pulse.sink_list() # All outputs. Dépend du système.
print(output)
#pulse.sink_list()[0] # Digital output
#pulse.sink_list()[1] # Analog output

level=0.55
sink = pulse.sink_list()[0]
#pulse.volume_change_all_chans(sink, -0.1) # increment / decrement volume
pulse.volume_get_all_chans(sink)
pulse.volume_set_all_chans(sink, level) # change to new value (0-1)
pulse.volume_get_all_chans(sink)




import datetime
expeStart = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')

# Initialisation de l'affichage
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)

#global largeur_ecran,hauteur_ecran,scale



textsize=58




## affiche l'interface
## lit la liste des stimuli
## boucle sur la liste en mélangeant aléatoirement (3 listes différentes  : orig, env, spec / block-design ou pas ?
## lit les coordonnées de la souris et détermine la réponse
## enregistre les deux données + les données expérimentales dans un fichier de résultats
## termine
## Phase d'entraînement (une 12zaine de stimuli, 4 par type, assez faciles et plus difficiles
## Donc deux fonctions principales dans main : train et test
## 
## 
## 
## 
## 
## 

if expenum=='C':
    ##matrice = ['.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','.hu.','.m.','.n.','.ny.','.r.','.l.','.y.','.w.']
    matrice = ['.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','','.m.','.n.','.ny.','.r.','.l.','.y.','.w.']
else:
    ##matrice = ['dizaine','départ','dernière','magique','','menteur','','musique','deuxième','meurtrière','','','montagne','','douzaine','morale','mortifère','','','peinture','']
    matrice = ['','hi','hé','ha','han','','','','hue','heu','','hon','','','','houx','ho','','hein','','']


def main():
    pyllar.splash("Bonjour. Appuyez sur une touche pour commencer l'entraînement.")
    training('vocoderConfusion-training-'+expenum+'.conf')
    pyllar.splash("Appuyez sur une touche pour commencer l'expérience.")
    expe('vocoderConfusion-expe-'+expenum+'.conf','resultats-vocoderConfusion-expe-'+expenum+'.res')
    pyllar.splash("Merci de votre participation.")

def expe(conf,res):
    reponse=''
    stimuli = pyllar.read_data_2D(conf,';')
    data = pyllar.read_data(conf)
    results= pyllar.init_resultsfile(res)
    ##pyllar.displaymatrice_3_7('aba','ada','aga','apa','ata','aka','','ava','aza','aja','afa','assa','acha','ahua','ama','ana','anya','ara','ala','aya','awa')
    if expenum=='C':
        ##pyllar.displaymatrice_3_7('.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','.hu.','.m.','.n.','.ny.','.r.','.l.','.y.','.w.')
        pyllar.displaymatrice_3_7('.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','','.m.','.n.','.ny.','.r.','.l.','.y.','.w.')
    else:
        ##pyllar.displaymatrice_3_7('dizaine','départ','dernière','magique','','menteur','','musique','deuxième','meurtrière','','','montagne','','douzaine','morale','mortifère','','','peinture','')
        ##pyllar.displaymatrice_3_7('di...zaine','dé...part','der...nière','ma...gique','','men...teur','','mu...sique','deu...xième','meur...trière','','','mon...tagne','','dou...zaine','mo...rale','mor...tifère','','','pein...ture','')
        ##pyllar.displaymatrice_3_7('hi','hé','ha','','han','','','hue','heu','','','hon','','','houx','ho','','','hein','','')
        pyllar.displaymatrice_3_7('','hi','hé','ha','han','','', '','hue','heu','','hon','','','','houx','ho','','hein','','')
        #pyllar.displaymatrice_3_7(matrice)
    pyllar.pause(500)
    alea = range(0,len(stimuli))
    random.shuffle(alea)
    #for i in range(0,len(stimuli)):
    for i in alea:
        #pyllar.catchquit()
        ##answers = ['aba','ada','aga','apa','ata','aka','','ava','aza','aja','afa','assa','acha','ahua','ama','ana','anya','ara','ala','aya','awa']		#Displaymatrice_2_3('aba','ada','aga','apa','ata','aka')
        answers = matrice
        pyllar.pause(200)
        soundpath="sons/"+expenum+"/"+stimuli[i][0]
        print i,stimuli[i][0]
        pyllar.play_sound(soundpath)
        (x,y,button) = pyllar.catchmouse()
        #pyllar.pause(200)
        reponse=pyllar.getanswerfrommatrix_3_7(x,y,answers)
        for k in range(0,len(data[i])):
            savedata = string.replace(data[i][k],'\n','')+';'
        resultsdata = (sujet+";"+str(expeStart)+";"+str(savedata)+str(i+1)+";"+str(x)+";"+str(y)+";"+str(button)+";"+reponse+"\n")
        results.write(resultsdata)
        results.flush
    pyllar.blank_screen()
    pygame.event.clear()
    results.close()

def training(conf):
    reponse=''
    stimuli = pyllar.read_data_2D(conf,';')
    data = pyllar.read_data(conf)
    #results= pyllar.init_resultsfile('marjolaine-exp1-resultats.txt')
    pyllar.pause(500)
    ##pyllar.displaymatrice_3_7('.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','.hu.','.m.','.n.','.ny.','.r.','.l.','.y.','.w.')
    ##pyllar.displaymatrice_3_7('aba','ada','aga','apa','ata','aka','','ava','aza','aja','afa','assa','acha','ahua','ama','ana','anya','ara','ala','aya','awa')
    if expenum=='C':
        ##pyllar.displaymatrice_3_7('.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','.hu.','.m.','.n.','.ny.','.r.','.l.','.y.','.w.')
        pyllar.displaymatrice_3_7('.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','','.m.','.n.','.ny.','.r.','.l.','.y.','.w.')
    else:
        ##pyllar.displaymatrice_3_7('dizaine','départ','dernière','magique','','menteur','','musique','deuxième','meurtrière','','','montagne','','douzaine','morale','mortifère','','','peinture','')
        ##pyllar.displaymatrice_3_7('di...zaine','dé...part','der...nière','ma...gique','','men...teur','','mu...sique','deu...xième','meur...trière','','','mon...tagne','','dou...zaine','mo...rale','mor...tifère','','','pein...ture','')
        pyllar.displaymatrice_3_7('','hi','hé','ha','han','','', '','hue','heu','','hon','','','','houx','ho','','hein','','')
    ##pyllar.displaymatrice_3_7(matrice)
    alea = range(0,len(stimuli))
    random.shuffle(alea)
    alea = alea[0:trainingsize]
    #for i in range(0,len(stimuli)):
    for i in alea:
        ##pyllar.catchquit()
        ##answers = ['aba','ada','aga','apa','ata','aka','','ava','aza','aja','afa','assa','acha','','ama','ana','anya','ara','ala','aya','awa']		#Displaymatrice_2_3('aba','ada','aga','apa','ata','aka')
        ##answers = ['.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','.hu.','.m.','.n.','.ny.','.r.','.l.','.y.','.w.']
        answers = matrice
        pyllar.pause(200)
        soundpath="sons/"+expenum+"/"+stimuli[i][0]
        print soundpath
        pyllar.play_sound(soundpath)
        (x,y,button) = pyllar.catchmouse()
        #pyllar.pause(200)
        reponse=pyllar.getanswerfrommatrix_3_7(x,y,answers)
        #for k in range(0,len(data[i])):
        #    savedata = string.replace(data[i][k],'\n','')+';'
        #resultsdata = (sujet+";"+str(savedata)+str(i+1)+";"+str(x)+";"+str(y)+";"+str(button)+";"+reponse+"\n")
    pyllar.blank_bg(white)
    pygame.event.clear()
    pyllar.pause(2500)

#def listshuffle(list):
#    vector = range(0,len(list))
#    random.shuffle(vector)
    


main()


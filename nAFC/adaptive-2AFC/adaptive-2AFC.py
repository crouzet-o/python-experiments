#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
adaptive_2AFC.py: A Python Script running a 2 Alternative-Forced-Choice
experiment in noise using an adaptive procedure that tracks peformance
continuously and adapts SNR (in dB).

Created on Mon Feb  3 11:04:05 2020

@author: crouzet-o
"""

import argparse
import wx

import Caterpyllar as pyllar

import sys
import locale
import re
import string

import pygame
#from pygame import event
from pygame.locals import * # events, key names (MOUSEBUTTONDOWN,K_r...)
import time

import numpy as np
import scipy
from scipy.io import wavfile
from scipy.stats import norm # Gaussian distribution functions

import random
import datetime

import codecs # Permet de convertir un fichier en lecture / écriture en unicode

# PortAudio (https://people.csail.mit.edu/hubert/pyaudio/)
import pyaudio
p = pyaudio.PyAudio()

# PulseAudio
#from pulsectl import Pulse
## Soundcard initialization
#pulse = Pulse("computer")
#output = pulse.sink_list() # All outputs. Dépend du système.
#print(output)
##pulse.sink_list()[0] # Digital output
##pulse.sink_list()[1] # Analog output
#
#level = 0.55
#sink = pulse.sink_list()[0]
##pulse.volume_change_all_chans(sink, -0.1) # increment / decrement volume
#pulse.volume_get_all_chans(sink)
#pulse.volume_set_all_chans(sink, level) # change to new value (0-1)
#pulse.volume_get_all_chans(sink)

# TODO: Check a better process using sounddevice (with callbacks) in order
# to suppress issues with playing the beginning of sounds
# Play through PortAudio only
import sounddevice as sd
sd.default.samplerate = 44100

## Writing and reading files on / from disk
#import soundfile as sf
#data = np.random.uniform(-1, 1, 44100)
#sf.write('new_file.wav', data, 44100)

pyllar.sayhi()
pygame.display.toggle_fullscreen()
DEBUG = 1

#sujet = raw_input("ID du sujet :") # Utiliser wxpython pour faire
                                   # apparaître un widget demandant le
                                   # numéro du sujet.

#confFile = "C" ##raw_input("Id de l'expérience (C: Consonnes, V:Voyelles) :") # Utiliser
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


## argparse Module
parser = argparse.ArgumentParser(description = 'Adaptive phonetic confusion experiment.', 
                                 epilog = 'Copyleft O. Crouzet (2020)')

parser.add_argument('--id', dest = 'subject', nargs = 1,
                    help = 'Subject ID.')

parser.add_argument('--conffile', dest='confFile', nargs=1,
                    help='Config File Name')

parser.add_argument('--wavdir', dest='wavDir', nargs=1,
                    help='Soundfiles directory')

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
if DEBUG == 1:
	print(args.subject, args.confFile, args.wavDir)

sujet = args.subject[0] ##int(args.subject[0])-1 ##args.subject[0]
confFile = args.confFile[0] ##int(args.n[0])-1
wavDir = args.wavDir[0] ##int(args.n[0])-1
#sampacol = int(args.sampa[0])-1
#nbrep = int(args.nbrep[0])
#infile = args.filename[0]
#language = args.lang[0]
#csvsep = args.csvsep[0]

#STIMDUR = int(args.STIMDUR[0])
#ITI = int(args.ISI[0])

## wx Module
tmp = wx.App(False)
screen_size = wx.GetDisplaySize()

# Check whether it is done in Caterpyllar/_init.py_ or in the experiment script
# It should be better to keep it inside the experiment script!
target_screensize = (800, 600) # tuple
target_perf = 0.75
empan = 0.1

trainingsize = 25

## codecs Module
sys.getdefaultencoding()


#screen = pygame.display.set_mode(screen_size) # Set window size
pygame.display.set_caption(pyllar.__name__+' - Version '+pyllar.version)

#print(window.get_size())


## datetime Module
expeStart = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')

def trialTimePoint():
    timeNow = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')
    return timeNow


# Initialisation de l'affichage

#global largeur_ecran,hauteur_ecran,scale



textsize = 58




if confFile == 'taka':
    ##matrice = ['.b.', '.d.', '.g.', '.p.', '.t.', '.k.', '', '.v.', '.z.', '.j.', '.f.', '.ss.', '.ch.', '.hu.', '.m.', '.n.', '.ny.', '.r.', '.l.', '.y.', '.w.']
    matrice = ['ta', 'ka']
else:
    ##matrice = ['dizaine', 'départ', 'dernière', 'magique', '', 'menteur', '', 'musique', 'deuxième', 'meurtrière', '', '', 'montagne', '', 'douzaine', 'morale', 'mortifère', '', '', 'peinture', '']
    matrice = ['t.', 'k.']


def main():
    #pyllar.splash("Bonjour. Appuyez sur une touche pour commencer l'entraînement.")
    #training('vocoderConfusion-training-'+confFile+'.conf')
    #pyllar.splash("Appuyez sur une touche pour commencer l'expérience.")
    expe('expe-2AFC-'+confFile+'.conf', 'resultats-expe-2AFC-'+confFile+'.res')
    pyllar.splash("Merci de votre participation.")

def expe(conf, res):
    pygame.event.set_blocked([MOUSEMOTION,MOUSEBUTTONUP,KEYDOWN,KEYUP]) # Block
                                                          # specific
                                                          # events
    results_array = []
    performance = 1
    target_perf = 0.75
    step = 0
    SNRdB = 0
    #reponse = ''
    stimuli = pyllar.read_data_2D(conf, ';')
    print(stimuli, len(stimuli))
    #data = pyllar.read_data(conf)
    results = pyllar.init_resultsfile(res)
    ##answers = ['aba','ada','aga','apa','ata','aka','','ava','aza','aja','afa','assa','acha','ahua','ama','ana','anya','ara','ala','aya','awa']		#Displaymatrice_2_3('aba','ada','aga','apa','ata','aka')
    if confFile == 'taka':
        ##pyllar.displaymatrice_3_7('.b.','.d.','.g.','.p.','.t.','.k.','','.v.','.z.','.j.','.f.','.ss.','.ch.','.hu.','.m.','.n.','.ny.','.r.','.l.','.y.','.w.')
        pyllar.display_2AFC('ta', 'ka')
    else:
        ##pyllar.displaymatrice_3_7('dizaine','départ','dernière','magique','','menteur','','musique','deuxième','meurtrière','','','montagne','','douzaine','morale','mortifère','','','peinture','')
        ##pyllar.displaymatrice_3_7('di...zaine','dé...part','der...nière','ma...gique','','men...teur','','mu...sique','deu...xième','meur...trière','','','mon...tagne','','dou...zaine','mo...rale','mor...tifère','','','pein...ture','')
        ##pyllar.displaymatrice_3_7('hi','hé','ha','','han','','','hue','heu','','','hon','','','houx','ho','','','hein','','')
        pyllar.display_2AFC('t.', 'k.')
        #pyllar.displaymatrice_3_7(matrice)
    answers = matrice
    if DEBUG:
        print(results)
    ##pyllar.displaymatrice_3_7('aba','ada','aga','apa','ata','aka','','ava','aza','aja','afa','assa','acha','ahua','ama','ana','anya','ara','ala','aya','awa')
    alea = range(0, len(stimuli))
    random.shuffle(list(alea))
    #for i in range(0,len(stimuli)):
    # Change to while (infinite loop while not QUIT)
    #for i in alea:
    while True: # tant qu'on ne quitte pas
        timeNow = trialTimePoint()
        pygame.event.set_blocked([MOUSEMOTION,MOUSEBUTTONUP,KEYDOWN,KEYUP]) # Block
                                                          # specific
                                                          # events
        step += 1
        #if step > 10:
        #    sys.exit()
        #pygame.event.clear()           # on evite de saturer la file d'evenements        step += 1

        # Select stimulus to play randomly
        select = random.sample(stimuli, 1)[0] # Extract list from parent list
        if DEBUG:
            print(select[0])
        soundpath = wavDir + "/" + select[0]
        if DEBUG:
            print(step, select[0], select[1])

        # Measure sound length in samples
        fs, solo = scipy.io.wavfile.read(soundpath, mmap=False)
        soloLen = len(solo)
        if DEBUG:
            print(soloLen)
            
        # Normalize signal RMS
        #rms_S = np.sqrt(np.mean(solo) ** 2) # Measure Signal RMS
        rms_S = np.sqrt(np.mean(solo[np.int(1*soloLen/6):np.int(5*soloLen/6)] ** 2)) # Measure Signal RMS
        solo = (0.5 / rms_S) * solo # (ref = RMS)
        #rms_S = np.sqrt(np.mean(solo) ** 2) # Measure Signal RMS
        rms_S = np.sqrt(np.mean(solo[np.int(1*soloLen/6):np.int(5*soloLen/6)] ** 2)) # Measure Signal RMS
       
        # Generate gaussian random noise
        #t = np.linspace(0, soloLen/1000*fs, num=soloLen)
        #print(t)
        np.random.seed(np.int(time.time()/1))
        noise = np.random.normal(loc=np.mean(solo), scale=1, size=soloLen)
        #print(noise)
        
        # Set SNR in dB using SNRdB (compute S_rms, N_rms, update)
        rms_N = np.sqrt(np.mean(noise ** 2)) # Measure Noise RMS
        noise = (0.5 / rms_N) * noise # (ref = RMS)
        rms_N_target = 10 ** (np.log10(rms_S) - (SNRdB/20)) # Compute required Noise RMS
        noise = (rms_N_target / rms_N) * noise # Ne marche pas ?
        
        tracks = np.column_stack((solo, noise))
        mix = np.sum(tracks, axis=1)
        rms_mix = np.sqrt(np.mean(mix[np.int(1*soloLen/6):np.int(5*soloLen/6)] ** 2)) # Measure Noise RMS
        
        # Fade-In / Fade-Out (Gaussian curve)
        fadeDuration = 75 # in ms
        fadeSamples = np.int(np.floor((fadeDuration/1000)*fs))
        fadeIn = norm.cdf(np.linspace(-2.58, 0, fadeSamples))*2
        fadeOut = norm.cdf(np.linspace(0, 2.58, fadeSamples))*2
        
        mix[:(fadeSamples)] = fadeIn * mix[:(fadeSamples)]        
        mix[-(fadeSamples):] = fadeIn * mix[-(fadeSamples):]        

        # Normalize overall intensity level of the mixture
        #mix = (.9 / np.max(np.abs(mix))) * mix # (ref = max PA)
        mix = (0.5 / rms_mix) * mix # (ref = RMS)
        #mix = np.int((2**16 / rms_mix) * mix)
        #print(fs)
        #mix = mix.astype(np.int16)
        
        ## Pygame conversion np.array to pygame.Sound
        #mix = pygame.sndarray.make_sound(mix)        
        #target_S_rms = 20*np.log10(/np.max(test))
        
        # Play sound (we could load these before the loop if there are few sounds)

        # Convert it to wav format (16 bits)
        #mix = np.array(mix, dtype=np.int16)
        # Play sound with sounddevice (sd)
        sd.play(mix, blocking=True)
        

        #tic = pygame.time.get_ticks()
        ## Play from file
        #pyllar.play_sound(soundpath)
        #pyllar.play_sound(mix)
        ## Play from array
        #print(pygame.mixer.get_init())
        #buzz = pygame.mixer.Sound(mix) # Load the sound file (wav format)
        #duration = int(buzz.get_length()*1000) # Get its duration in ms
        #buzz.play() # Play the file
        #pyllar.pause(duration) # Wait until it's finished playing
        #pygame.event.clear()
        ## Check what happens when only 1 or 2 output variables (tupple sent to the latest one?)
        ##pyllar.catchquit()
        (x, y, button) = pyllar.catchmouseOrQuit()
        pygame.event.set_blocked([MOUSEMOTION,MOUSEBUTTONUP,KEYDOWN,KEYUP]) # Block
                                                          # specific
                                                          # events
        #while pygame.time.get_ticks()-tic < 3000:
        #    pyllar.pause(1)
        if DEBUG:
            print(x, y, button)
        #pyllar.pause(200)
        reponse = pyllar.getanswerfrom_2AFC(x, y, answers)
        if DEBUG:
            print(reponse)
        # Evaluate response (compare "reponse" with "stimuli[i][0]")
        if reponse == select[1]:
            success = True
            feedbackstr = "Bonne Réponse :)"
        else:
            success = False
            feedbackstr = "Mauvaise Réponse :("
        if DEBUG:
            print(success)
        # TODO: Save spectrogram as a vector of numbers in a binary format 
        # (with filename = specgram-step-N.bin)
        results.write(expeStart + ';' + timeNow + ';' + str(step) + ';' + sujet + ';' + confFile + ';' + wavDir + ';' + select[1] + ';' + reponse + ';' + str(int(success)) + '\n')
        results_array.append(success)
        if DEBUG:
            print(results_array[:-5])
        # Display feedback on the screen / include diplay_2AFC in the loop
        
        
        # if step / position > 10, compute performance
        if step > 10:
            performance = np.sum(results_array[-10:])/len(results_array[-10:])
            if DEBUG == True:
                print(performance)
            if DEBUG:
                print(str(np.round(performance*100, 2)))
            if DEBUG:
                print(str(np.round(SNRdB, 0)))
            
            # if performance < target_ref - empan, increase SNRdB
            # if performance > target_ref + empan, decrease SNRdB
            # else do not change SNRdB
            dBmod = 0
            if np.abs(performance-target_perf) >= 0.2:
                dBmod = 0.8
            elif np.abs(performance-target_perf) >= 0.15:
                dBmod = 0.6
            elif np.abs(performance-target_perf) >= 0.1:
                dBmod = 0.4
            elif np.abs(performance-target_perf) >= 0.05:
                dBmod = 0.2
            # Increase vs. Decrease SNR
            if performance < target_perf:
                dBmod = dBmod
            elif performance > target_perf:
                dBmod = -dBmod
            # Change SNR
            SNRdB = SNRdB + dBmod
            # Fixed boundaries for SNR
            if SNRdB > 5: # Varnet et al. used 0dB as a limit
                SNRdB = 5
            elif SNRdB < -40: # Varnet et al. used -20dB as a limit
                SNRdB = -40
            if DEBUG:
                print(SNRdB)
        else:
            performance = np.sum(results_array)/len(results_array)

            
        #for k in range(0,len(data[i])):
        #    savedata = string.replace(data[i][k],'\n','')+';'
        #resultsdata = (sujet+";"+str(expeStart)+";"+str(savedata)+str(i+1)+";"+str(x)+";"+str(y)+";"+str(button)+";"+reponse+"\n")
        #results.write(resultsdata)
        #results.flush
        # display recent performance on the screen (top / right, percentage)
        infostring = feedbackstr+" - Réussite : "+str(np.int(performance*100))+"% - "+"Rapport S/B : "+str(np.round(SNRdB, 1))+" dB - Numéro d\'essai : "+str(step)
        pyllar.display_infoline(infostring)
        #pyllar.display_text_pos(str(np.int(performance*100))+"% - "+"Rapport S/B : "+str(np.round(SNRdB, 1))+" dB / Position : "+str(step), 300, 50)
        # display actual SNR on the screen (top / left, dB)
        #pyllar.display_text_pos("Rapport S/B : "+str(np.round(SNRdB, 1))+" dB", 600, 50)
        #pyllar.pause(200)
        pyllar.pause(500)
    pyllar.blank_screen()
    pygame.event.clear()
    results.close()








# Game-Over
#pygame.display.quit()



main()

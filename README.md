# python-experiments
Python programs for speech production / perception experiments

These programs depend on Caterpyllar (http://github.com/crouzet-o/caterpyllar):
a small, _work-in-progress_, Python library for human interface experiments on
speech perception and production.

Included programs:
* displaylist.py
* progression.py


## TODO

* Control split-screen displays with pygame (same image on both screens vs.
  large surface + different displays on both parts of the surface vs. target
  only screen N); 
* Free fonts will be added in order to guarantee the compatibility with any
  computer;
* __IN PROGRESS:__ Homogenize displaylist / progression or even better fuse
  them into a single utility;
* __IN PROGRESS:__ Add command-line argument to activate / deactivate the
  progression bar;
* _Some options have been introduced_ that let one: (1) decide whether they
  want a progress-bar or not (under the text), (2) display the text to be read
  for a few seconds before the reading phase, launching a screen-flash warning
  before the actual reading phase. It should be controlled from either the
  command line or a config file rather than from within the Python script.


## Pre-installation instructions

* In order to use these scripts, you will need a few Python packages (here are
  some usefull installation commands):

sudo apt-get install libgtk2.0-dev python3-pip
(sudo) pip3 install pygame wxPython


## displaylist.py

An interface that will display written sequences on screen either in a
Left-to-Right language (as english or french) or in a Right-to-Left language
(only Arabic has been tested).


## progression.py

An interface that will display written sequences along with a progression bar
at various rates. This is used for experimentation on the impact of speech rate
variations on speech production.

It has also been extended to japanese and mandarin chinese using adequate
fonts. It is distributed with freely licensed fonts in order to guarantee that
it will work on any system. __TODO:__ Font licence information must be
included. As for now only Chinese has been configured to use an internally
distributed font.

The progression bar can be deactivated while keeping the adaptive rate control.


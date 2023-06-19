# Débits utilisés dans l'expérience VV / débit

* 70 (ms / syll)
* 140 (ms / syll)
* 190 (ms / syll)

# Corrections / Améliorations du script

* Amélioration des noms de paramètres

# Exemple de ligne de commande

## En français

`./progression.py --lang fr --fontsize 40 --colstim 2 --colNsyll 7 --id test0 --rep 1 --timepersyll 140 --blocksize 5 --isi 1000 listeVV.csv`

# Installation

* Recent versions of wxPython have been reconceived from scratch. Installing it from conda (conda install -c conda-forge wxpython) or with a simple pip command (pip install wxpython) does not work (ipython won't find the module)
* `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/debian-11 wxPython`
* (see https://www.wxpython.org/pages/downloads/)



# Quelques exemples de lignes de commande pour lancer le programme :

En arabe :
./progression.py --lang ar --fontsize 40 --col 3 --sampa 4 --sylls 9 --id loc1 --rep 1 --timepersyll 100 --blocksize 5 --isi 1000 --progbar --trialpreread listes/liste-mohamad-rateinfo.csv 

En chinois :
./progression.py --lang cjk --fontsize 40 --col 2 --sylls 1 --id loc1 --rep 1 --timepersyll 300 --blocksize 25 --isi 1000 2020-jue-master2-aff.csv

# Signification des options :

Lancer "./progression.py -h" pour avoir la liste des options disponibles

--lang
--fontsize
--col
--sampa
--syls
--id
--trialpreread
--




# Notes sur l'expérience en chinois :

Fichiers de contrôle (utiliser cet ordre de passation fixe) :
 
2020-jue-master2-intpart.csv 
2020-jue-master2-aff.csv 
2020-jue-master2-int.csv 
2020-jue-master2-mots.csv 

# DONE:
Modifier le script pour avoir (1) une phase de lecture silencieuse, (2) un
top-départ pour la lecture à voix haute rapide


# TODO:
* Add information from other READMEs (in displaylist/ and 00fusedOld)
* Add information concerning arabic / pyfribidi to be installed
* Need to add case where no syllable count is provided in the file (add
  constant number of syllables or trial display rate / duration)
* Plan more thoughtfully how configuration of the experiment is controlled:
	- Distinguish cases where a column with number of syllables in the
	  utterance is provided vs. cases where no such information is provide,
	implying that the number of syllables should either be unused (we only use ISI
	/ ITI to control presentation rate) or number of syllables is fixed (therefore
	it should be a number that is provided on the command line but this number is
	not a column number but rather a scalar to be used in the script).

 
Pour lancer le programme il faut copier la ligne de commande suivante :

./progression.py --lang cjk --fontsize 40 --col 2 --sylls 1 --id loc1 --rep 1 --timepersyll 300 --blocksize 25 --isi 1000 2020-jue-master2-aff.csv

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

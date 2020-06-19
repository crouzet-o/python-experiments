

# Réplication multi-locuteurs + contexte phonétique


# Variantes de réplication à prévoir (stagiaires)



# Manip JEP2018
Participant n°15 interruption de l'expérience en cours de route (pour C uniquement) ?



Packages à installer :

python-argparse
python-pygame
python-scipy
python-wxgtk*
python-datetime

Changement pour l'audio

python-alsaaudio (obsolète)
changé pour
python-pulsectl (Pulse Audio drivers)
(permet d'utiliser les cartes son externes)


Exécution du protocole :

./expe-vocoderConfusion.py --h

./expe-vocoderConfusion.py --id sujet1 --expe C

./expe-vocoderConfusion.py --id sujet1 --expe V

# --id : identifiant du sujet, --liste : numéro de la liste, --colstim : numéro de colonne contenant les noms des fichiers audio

./expe-vocoderConfusion.py --id sujet1 --liste 1 --colstim 2



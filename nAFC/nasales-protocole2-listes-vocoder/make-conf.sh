#!/bin/sh

# Génération des fichiers de configuration pour l'expérience C
#gawk 'BEGIN { FS=";"; OFS=";"; split("1;2;4;6;8;12;16;22;32",nbbands); split("4;16;32;64;128",freqc); split("Adrien;Julien;Paul;Juliette;Samantha;Sarah", speaker) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { for (k in speaker) { print speaker[k]"_"$8"-"nbbands[i]"bands-fc-"freqc[j]"NoiseCarrier.wav",$0 }}}}' < liste-C-finale.csv > vocoderConfusion-expe-C.conf

# ENTRAÎNEMENT
#gawk 'BEGIN { FS=";"; OFS=";"; split("8;16;32",nbbands); split("128",freqc); split("Adrien;Julien;Paul;Juliette;Samantha;Sarah", speaker) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { for (k in speaker) { print speaker[k]"_"$8"-"nbbands[i]"bands-fc-"freqc[j]"NoiseCarrier.wav",$0 }}}}' < liste-C-finale.csv > vocoderConfusion-training-C.conf

#"Adrien;Julien;Paul;Juliette;Samantha;Sarah"
#"Paul;Julien;Juliette;Samantha"
#split("1;4;8;12;16;22",nbbands);
#split("4;16;128",freqc)
# Génération des fichiers de configuration pour l'expérience V (contexte CV)
# 1580*2/60 = 52 minutes à 2s / stimulus
gawk 'BEGIN { FS=";"; OFS=";"; split("4;8;12;16;22",nbbands); split("128",freqc); split("Adrien;Julien;Juliette;Samantha", speaker) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $1"-"nbbands[i]"bands-fc-"freqc[j]"-NoiseCarrier.wav",$0 }}}' < liste-CV.csv > vocoderConfusion-expe-V.conf

# ENTRAÎNEMENT
gawk 'BEGIN { FS=";"; OFS=";"; split("16;22",nbbands); split("128",freqc); split("Adrien;Julien;Juliette;Samantha", speaker) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $1"-"nbbands[i]"bands-fc-"freqc[j]"-NoiseCarrier.wav",$0 }}}' < liste-CV.csv > vocoderConfusion-training-V.conf

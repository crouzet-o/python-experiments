#!/bin/sh

# Génération des fichiers de configuration pour l'expérience C
gawk 'BEGIN { FS=";"; OFS=";"; split("1;2;4;6;8;12;16;22;32",nbbands); split("4;16;32;64;128",freqc) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $8"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}' < liste-C-finale.csv > vocoderConfusion-expe-C.conf

# ENTRAÎNEMENT
gawk 'BEGIN { FS=";"; OFS=";"; split("4;8;16",nbbands); split("128",freqc) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $8"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}' < liste-C-finale.csv > vocoderConfusion-training-C.conf

# Génération des fichiers de configuration pour l'expérience V
gawk 'BEGIN { FS=";"; OFS=";"; split("1;2;4;6;8;12;16;22;32",nbbands); split("4;16;32;64;128",freqc) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $3"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}' < liste-V-finale.csv > vocoderConfusion-expe-V.conf

# ENTRAÎNEMENT
gawk 'BEGIN { FS=";"; OFS=";"; split("4;8;16",nbbands); split("128",freqc) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $3"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}' < liste-V-finale.csv > vocoderConfusion-training-V.conf


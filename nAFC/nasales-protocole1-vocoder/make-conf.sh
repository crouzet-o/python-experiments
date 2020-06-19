#!/bin/sh

# Génération des fichiers de configuration pour l'expérience C
gawk 'BEGIN { FS=";"; OFS=";"; split("2;4;6;8",nbbands); split("4;16;128",freqc) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $9"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}' < liste-C-finale.csv > vocoderConfusion-expe-C.conf

# ENTRAÎNEMENT
gawk 'BEGIN { FS=";"; OFS=";"; split("8",nbbands); split("128",freqc) } NR<=1 {next} { for (i in nbbands) { for (j in freqc) { print $9"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}' < liste-C-finale.csv > vocoderConfusion-training-C.conf

# Génération des fichiers de configuration pour l'expérience V
gawk 'BEGIN { FS=";"; OFS=";"; split("1;2;3;4;5", reps); split("2;4;6;8",nbbands); split("4;16;128",freqc) } NR<=1 {next} { for (k in reps) { for (i in nbbands) { for (j in freqc) { print $4"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}}' < liste-V-finale.csv > vocoderConfusion-expe-V.conf

# ENTRAÎNEMENT
gawk 'BEGIN { FS=";"; OFS=";"; split("1;2;3;4", reps); split("8",nbbands); split("128",freqc) } NR<=1 {next} { for (k in reps) { for (i in nbbands) { for (j in freqc) { print $4"-"nbbands[i]"bands-fc-"freqc[j]".wav",$0 }}}}' < liste-V-finale.csv > vocoderConfusion-training-V.conf


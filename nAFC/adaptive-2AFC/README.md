# TODO:

* Check whether there's a more recent version on the Dell laptop that was
used during the NBC...


# Description

This script has been designed for a demonstration of an adaptive procedure used
in experiments using the method of classification images in speech perception.

This is a simple adaptive experiment in which Signal-to-Noise Ratio varies
depending on 2AFC classification performance. The target performance is 75%.

The display provides continuous information on: (1) correct / incorrect answer 
feedback, (2) Current SNR, (3) Performance over the 10 previous trials.


# Launching the experiment

./adaptive-2AFC.py --id test --conffile taka --wavdir sons



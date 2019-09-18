#!/usr/bin/sh

./parse.py
wordcloud_cli --text causality.txt --imagefile causality.png --width 1000 --height 1000 --background white
wordcloud_cli --text hmm.txt --imagefile hmm.png --width 1000 --height 1000 --background white
wordcloud_cli --text hmm_intent_objects_types.txt --imagefile hmm_intent_objects_types.png --width 1000 --height 1000 --background white

Rscript descriptive.R
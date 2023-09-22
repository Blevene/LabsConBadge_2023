#!/bin/bash

for I in {0..1024}; do
	echo "#$I: waiting for /dev/$1. Plug in!"
	while [ ! -b /dev/$1 ]; do sleep .1; done
	echo "$1 attached. mounting.. "
	pmount /dev/$1
	echo "$1 wiping.. "
	rm /media/$1/*
	echo "$1 copying code.. "
	cp -r software/* /media/$1/ 
	echo "$1 copying dataset.. "
	cp configs/$I/* /media/$1/data/
	echo "$1 unmounting.. "
	pumount /media/$1
	echo "$1 Done - Unplug!"
	while [ -b /dev/$1 ]; do sleep .1; done
done

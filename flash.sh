#!/bin/bash

for INDEX in $(seq 1 50);
do
	echo "Plug in"
	read
	cp -r software/* /media/silas/CIRCUITPY/


	cp configs/g0/$INDEX_game0.csv /media/silas/CIRCUITPY/data/game0.csv
	cp configs/g1/$INDEX_game1.csv /media/silas/CIRCUITPY/data/game1.csv
	cp configs/g2/$INDEX_game2.csv /media/silas/CIRCUITPY/data/game2.csv
	cp configs/g3/$INDEX_game3.csv /media/silas/CIRCUITPY/data/game3.csv
	cp configs/g4/$INDEX_game4.csv /media/silas/CIRCUITPY/data/game4.csv
	
	umount /media/silas/CIRCUITPY/
	
	echo "DONE $INDEX"
done
	
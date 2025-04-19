#!/bin/bash
FILES="FSMs/*"
for f in $FILES
do
mkdir "${f%.*}" && mv "$f" "${f%.*}"
done

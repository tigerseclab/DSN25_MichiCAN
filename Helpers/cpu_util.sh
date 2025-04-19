#!/bin/bash
FILES="../FSM_Generation/results/FSMs/*"
for f in $FILES
do
echo "Processing $f ..."
echo "Compiling..."
./arduino-cli --fqbn arduino:sam:arduino_due_x compile "$f"
echo "Uplading..."
./arduino-cli --fqbn arduino:sam:arduino_due_x -p /dev/ttyACM1 upload "$f"
echo "Write external time measurement to file..."
esptool --chip auto --port /dev/ttyUSB0 run
timeout 15s tail -f < /dev/ttyUSB0 > "./Evaluation/CPU_Util/"$(basename "$f")".txt"
echo "Done Processing $f"
done

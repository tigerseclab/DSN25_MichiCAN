#!/bin/bash
FILES="../FSM_Generation/results/FSMs/Arduino/125K/Buses_light/*"
TESTS="../FSM_Generation/results/FSMs/Arduino/125K/Tests/*"
for f in $FILES
do
echo $(basename "$f")
for i in "$f"/*
do
echo "Running through different CAN IDs"

for j in $TESTS
do
#Upload Programming Sketch
echo "Processing $j ..."
echo "Compiling Programming..."
./arduino-cli --fqbn arduino:sam:arduino_due_x_dbg compile "$j"
echo "Uploading to Programming..."
./arduino-cli --fqbn arduino:sam:arduino_due_x_dbg -p /dev/ttyACM1 upload "$j"
#Upload Native Sketch
echo "Processing $i ..."
echo "Compiling Native..."
./arduino-cli --fqbn arduino:sam:arduino_due_x compile "$i"
echo "Uploading to Native..."
./arduino-cli --fqbn arduino:sam:arduino_due_x -p /dev/ttyACM0 upload "$i"
#Sampling CPU and BUS
echo "Sampling $i from PulseView..."
sigrok-cli -d fx2lafw --config samplerate=250000 --time 10000 --channels D2 > "./Evaluation/125K_light/"$(basename "$f")"/Bus_Load/"$(basename "$j")".txt"
echo "Done sampling $i"
echo "Write external time measurement to file..."
esptool --chip auto --port /dev/ttyUSB0 run
timeout 15s tail -f < /dev/ttyUSB0 > "./Evaluation/125K_light/"$(basename "$f")"/CPU_Util/"$(basename "$j")".txt"
echo "Done Processing $i"
done

done
done





#mkdir "./Evaluation/125K/"$(basename "$f") to make sub directories 

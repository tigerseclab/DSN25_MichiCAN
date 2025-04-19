import os
from pathlib import Path
import random

for i in range(20):
    ecu = random.choice(range(0x001, 0x7fe))
    ecu = hex(ecu)
    current_directory = os.getcwd()
    write_ecu = current_directory + "/results/FSMs/Arduino/125K/Tests/" + ecu + "/" + ecu
    Path(write_ecu).parent.mkdir(exist_ok=False, parents=True)
    with open("{}.{}".format(write_ecu, "ino"), "w+") as f:
        with open("test_template.ino", "r") as template:
            f.write(template.read().replace(
                "{{CAN_ID}}", ecu).replace("{{BUS_SPEED}}", "125"))
    write_ecu = current_directory + "/results/FSMs/Arduino/50K/Tests/" + ecu + "/" + ecu
    Path(write_ecu).parent.mkdir(exist_ok=False, parents=True)
    with open("{}.{}".format(write_ecu, "ino"), "w+") as f:
        with open("test_template.ino", "r") as template:
            f.write(template.read().replace(
                "{{CAN_ID}}", ecu).replace("{{BUS_SPEED}}", "50"))

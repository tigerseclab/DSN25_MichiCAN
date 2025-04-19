# MichiCAN: Spoofing and Denial-of-Service Protection using Integrated CAN Controllers

## What’s Inside
- **FSM_Generation**: Python scripts and Arduino templates that auto-generate FSM sketches targeting specific CAN IDs.
- **Helpers**: Bash scripts to build, deploy, and test the generated sketches. Also includes the sketch used to measure time via ESPs.
- **MichiCAN_due_examples**: Example sketches that bring MichiCAN to life.

## Getting Started
1. **Requirements**: Arduino Due, Arduino IDE, Python 3, and Bash (or Git Bash on Windows).
2. **Generate**: Customize `custom_ids.txt` and run the Python scripts in the FSM_Generation folder.
3. **Deploy**: Use helper scripts (e.g., `load_125.sh`) to compile and upload sketches.
4. **Test**: Review the results and graphs in `FSM_Generation/results`.

# This python program is used to generate C++ code for the arduino to run
# The idea behind this is that this will run on a higher priority CAN bus
# This state machine implementation will only identify if the CAN bus's own CAN ID is being used elsewhere
# This can be recognized as a spoofed CAN ID and can then be shut down appropriately
# Only a CAN ID can recognize that itself is being spoofed, so this higher priority CAN bus is the only one that can recognize and shut down such an attack, but spoofed IDs that are not already owned will be identified and shut down by lower priority CAN buses


GENERATED_FOR = 0x110

# Don't change anything below this for your configuration


def main(algData, ecus, ecu_to_catch):
    # generate the code for the state machine from another file
    return generate_cpp(algData.padded_binary(ecu_to_catch))


def generate_cpp(id):
    code = '// Generated by canid_specific_match.py:\n'
    code += '// built for ECU bus ID: ' + \
        hex(int(id, 2)) + '\n'
    code += 'void state_machine_run(uint8_t value) {\n'
    code += '  bitWrite(state, 10 - len, value);\n'
    code += '  len++;\n'
    code += '  \n'
    code += '  if (len == 11 && state == {}) {{\n'.format(
        int(id, 2))
    code += '    start_counterattack = true;\n'
    code += '    return;\n'
    code += '  }\n'
    code += '  \n'
    code += ''
    code += '  return;\n'
    code += '}\n'
    code += '// End generated code\n'
    return code

# now we are done collecting everything we need and can build out our (sort of) state machine for the CAN ID


# run this if this function is called directly from command line to build specific FSM
if __name__ == "__main__":
    import canid_shared_algs
    print(generate_cpp(canid_shared_algs.algs.padded_binary(None, GENERATED_FOR)))

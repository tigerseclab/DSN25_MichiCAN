bool tester(uint16_t to_test) {
    char id[12];
    len = 0;
    state = 0;
    start_counterattack = false;

    // write the binary values to a char array to read in as simulated input
    for (int i = 0; i < 11; i++) {
        string tmp = to_string(bitRead(to_test, 10 - i));
        char const* num_char = tmp.c_str();
        id[i] = num_char[0];
    }

    // iterate through each binary value and test the state machine
    for (int i = 0; i < 11; i++) {
        state_machine_run((uint8_t)(id[i] - '0'));
        if (start_counterattack) {
            break;
        }
    }
    if (start_counterattack) {
        return true;
    }
    else {
        return false;
    }
}

int main() {
    if (tester(generated_for)) {
        return 0;
    }
    else {
        return 1;
    }
}

// Generated by canid_catch_less_than.py:
// using ECU CAN IDs: ['0x100', '0x101', '0x110', '0x150']
// built for ECU bus ID: 0x101
void state_machine_run(uint8_t value) {
  
  bitWrite(state, 10 - len, value);
  len++;
  
  if (state > 257) {
    return;
  }
  if (len == 11 && state == 257) {
    start_counterattack = true;
    return;
  }
  if (len == 1 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 2 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 3 && value == 0) {
    start_counterattack = true;
    return;
  }
  if (len == 4 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 6 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 8 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 9 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 10 && value == 1) {
    start_counterattack = true;
    return;
  }
  if (len == 7 && state == 320) {
    start_counterattack = true;
    return;
  }
  if (len == 11 && state == 273) {
    start_counterattack = true;
    return;
  }
  if (len == 11 && state == 337) {
    start_counterattack = true;
    return;
  }
  return;
}
// End generated code


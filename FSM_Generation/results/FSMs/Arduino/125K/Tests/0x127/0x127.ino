// Required libraries
#include "variant.h"
#include <due_can.h>
#define TEST1_CAN_TRANSFER_ID    0x127
#define MAX_CAN_FRAME_DATA_LEN   8
#define SPEED                    CAN_BPS_125K

#define sda PIO_PC3
#define scl PIO_PC1

//Leave defined if you use native port, comment if using programming port
// #define Serial SerialUSB
CAN_FRAME frame1;
void setup()
{
    Serial.begin(115200);

    Can0.begin(SPEED);
    frame1.id = TEST1_CAN_TRANSFER_ID;
    frame1.length = MAX_CAN_FRAME_DATA_LEN;
    frame1.data.bytes[0] = 0x12;
    frame1.data.bytes[1] = 0x22;
    frame1.data.bytes[2] = 0x33;
    frame1.data.bytes[3] = 0x44;
    frame1.data.bytes[4] = 0x55;
    frame1.data.bytes[5] = 0x66;
    frame1.data.bytes[6] = 0x77;
    frame1.data.bytes[7] = 0x88;
    frame1.extended = 0;

    //Use Pins 33 and 35 for external time measurement on ESP32
    PIOC->PIO_PER = PIO_PC1;
    PIOC->PIO_PER = PIO_PC3;

    //Set Pins 33 and 35 as output (Ouput Enable Register)
    PIOC->PIO_OER = PIO_PC1;
    PIOC->PIO_OER = PIO_PC3;

    //Disable pull-up on both pins (Pull Up Disable Register)
    PIOC->PIO_PUDR = PIO_PC1;
    PIOC->PIO_PUDR = PIO_PC3;

}


void loop() {
    Can0.sendFrame(frame1);
    delayMicroseconds(1000);

    /*
    PIOC->PIO_CODR = sda;
    PIOC->PIO_SODR = sda;
    delayMicroseconds(25);
    PIOC->PIO_CODR = scl;
    PIOC->PIO_SODR = scl;
    */

}

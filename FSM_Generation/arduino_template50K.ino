#include "variant.h"
#include <due_can.h>

#define SPEED                    CAN_BPS_50K
#define SAMPLING_POINT           1.4       // Add 1 to the sampling point

#define sda PIO_PC7
#define scl PIO_PC1

#define Serial SerialUSB

int counter = 0;
int counter2 = 0;
int stuffcnt = 0;
bool can_frame[27];
volatile bool sof = false;
bool start_counterattack = false;
uint16_t state = 0;
uint8_t len = 0;
volatile bool first_cycle = false;
volatile uint8_t retransmission_count = 0;

// FSM

void reset_state_machine() {
    state = 0;
    len = 0;
}

void TC3_Handler() {
    TC_GetStatus(TC1, 0);

    PIOC->PIO_CODR = sda;   // External Timer
    PIOC->PIO_SODR = sda;

    bool value = PIOA->PIO_PDSR & PIO_PA1A_CANRX0;

    if (sof == true) {    // Start arbitration
        counter2++;
        if (counter2 < 25 && !start_counterattack) {
            if (can_frame[counter2 - 2] != value && stuffcnt == 5) {
                stuffcnt = 0;
                counter2--;
            }
            else if (can_frame[counter2 - 2] == value && stuffcnt < 5) {
                can_frame[counter2 - 1] = value;
                state_machine_run(value);
                stuffcnt++;
            }
            else if (can_frame[counter2 - 2] != value && stuffcnt < 5) {
                can_frame[counter2 - 1] = value;
                state_machine_run(value);
                stuffcnt = 1;
            }
        }

        if (first_cycle == true) {
            first_cycle = false;
            NVIC_DisableIRQ(TC3_IRQn);
            startTimer(TC1, 0, TC3_IRQn, SPEED);
        }

        if (counter2 == 21) {
            PIOA->PIO_PDR = PIO_PA0A_CANTX0;
            PIOA->PIO_ODR = PIO_PA0A_CANTX0;
            sof = false;
            counter2 = 0;
            retransmission_count++;
        }

        else if (counter2 == 14) {
            if (start_counterattack == true) {    // Counterattack
                start_counterattack = false;
                PIOA->PIO_PER = PIO_PA0A_CANTX0;    // Multiplex CAN_TX to GPIO
                PIOA->PIO_OER = PIO_PA0A_CANTX0;    // Define CAN_TX as output
                PIOC->PIO_CODR = PIO_PA0A_CANTX0;   // set pin to LOW
            }
        }
    }
    else {    // Keep for retransmissions
        if (value == 1) {
            counter++;
        }
        else if (value == 0 && counter < 11) {
            counter = 0;
        }

        if (counter >= 11 && value == 0) {    //SOF
            sof = true;
            counter = 0;
            stuffcnt = 1;
            can_frame[0] = 0;
            counter2 = 1;
            reset_state_machine();
        }
    }

    PIOC->PIO_CODR = scl;   // External Timer
    PIOC->PIO_SODR = scl;
}

void startTimer(Tc* tc, uint32_t channel, IRQn_Type irq, uint32_t frequency) {

    //Enable or disable write protect of PMC registers.
    pmc_set_writeprotect(false);
    //Enable the specified peripheral clock.
    pmc_enable_periph_clk((uint32_t)irq);

    TC_Configure(tc, channel, TC_CMR_WAVE | TC_CMR_WAVSEL_UP_RC | TC_CMR_TCCLKS_TIMER_CLOCK4);
    uint32_t rc = VARIANT_MCK / 128 / frequency;

    TC_SetRA(tc, channel, rc / 2);
    TC_SetRC(tc, channel, rc);
    TC_Start(tc, channel);

    tc->TC_CHANNEL[channel].TC_IER = TC_IER_CPCS;
    tc->TC_CHANNEL[channel].TC_IDR = ~TC_IER_CPCS;
    NVIC_EnableIRQ(irq);
}

void MichiCAN_Sync() {
    first_cycle = true;
    sof = true;
    counter = 0;
    can_frame[0] = 0;
    counter2 = 1;
    stuffcnt = 1;
    reset_state_machine();
    NVIC_DisableIRQ(TC3_IRQn);
    startTimer(TC1, 0, TC3_IRQn, (1 / SAMPLING_POINT) * SPEED);
    detachInterrupt(PIO_PA1A_CANRX0);
}

void setup() {

    // start serial port at 115200 bps:
    Serial.begin(115200);

    // Verify CAN0 and CAN1 initialization, baudrate is 1Mb/s:
    if (Can0.begin(SPEED) &&
        Can1.begin(SPEED)) {
    }
    else {
        Serial.println("CAN initialization (sync) ERROR");
    }

    PMC->PMC_PCER0 |= PMC_PCER0_PID11; // PIOA power ON

    //Multiplex CAN_RX to GPIO (Peripheral Enable Register)
    PIOA->PIO_PER = PIO_PA1A_CANRX0;

    //Set CAN_RX as input (Ouput Disable Register)
    PIOA->PIO_ODR = PIO_PA1A_CANRX0;

    //Disable pull-up on both pins (Pull Up Disable Register)
    PIOA->PIO_PUDR = PIO_PA1A_CANRX0;
    PIOA->PIO_PUDR = PIO_PA0A_CANTX0;

    //Use Pins 33 and 35 for external time measurement on ESP32
    PIOC->PIO_PER = scl;
    PIOC->PIO_PER = sda;

    //Set Pins 33 and 35 as output (Ouput Enable Register)
    PIOC->PIO_OER = scl;
    PIOC->PIO_OER = sda;

    Can0.watchFor();
}

void loop()
{
    if (sof == false) {
        attachInterrupt(PIO_PA1A_CANRX0, MichiCAN_Sync, FALLING); //Indicates SOF
    }
}

#include <user_interface.h>
#include <Wire.h>

#define sda 4 
#define scl 5 
#define SIZE 5000
volatile unsigned long startCountVar = 0;
volatile unsigned long stopCountVar = 0;
volatile unsigned int count = 0;
volatile unsigned long startlist[SIZE];
volatile unsigned long stoplist[SIZE];
volatile boolean sendFlag = true;
volatile boolean switching = false;
int value = 0;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  pinMode(sda,INPUT);
  pinMode(scl,INPUT);
  //delayMicroseconds(1000000); Doesn't do anything
  attachInterrupt(digitalPinToInterrupt(sda), startCount, RISING); //Attach interrupts don't interrupt each other
  attachInterrupt(digitalPinToInterrupt(scl), stopCount, RISING);
}


ICACHE_RAM_ATTR void startCount(){
  if(sendFlag){
    
      startlist[count] = ESP.getCycleCount();
      sendFlag = false;
    
  }
}

/*ICACHE_RAM_ATTR void startCount(){
  if(sendFlag){
    if(!switching){
      startlist[count] = ESP.getCycleCount();
      sendFlag = false;
    } else {
      stoplist[count] = ESP.getCycleCount();
      sendFlag = false;
      count++;
    }
    
  } else {
    count++;
    startlist[count] = ESP.getCycleCount();
    sendFlag = false;
    switching = false;
  }
}*/

/*ICACHE_RAM_ATTR void stopCount(){
  if(!sendFlag){
    if(!switching){
      stoplist[count] = ESP.getCycleCount();
      count++;
      sendFlag = true;
    } else {
      startlist[count] = ESP.getCycleCount();
      sendFlag = true;
    }
    
  } else {
    startlist[count] = ESP.getCycleCount();
    sendFlag = true;
    switching = true;
  }
}*/

ICACHE_RAM_ATTR void stopCount(){
  if(!sendFlag){
      stoplist[count] = ESP.getCycleCount();
      count++;
      sendFlag = true;
    
  }
}



// the loop function runs over and over again forever
void loop() {
  //Serial.println("Has this happened");
  
  //Serial.println("LOOPING");
    if(count == SIZE){
      detachInterrupt(digitalPinToInterrupt(sda)); //Attach interrupts don't interrupt each other
      detachInterrupt(digitalPinToInterrupt(scl));
      
      for(int i = 0; i < SIZE; i++)
      {
        value = (stoplist[i] -startlist[i])*6.25;
        Serial.println(value);
      }
      count++;
    }

}

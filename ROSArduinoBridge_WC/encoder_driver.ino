/* *************************************************************
   Encoder definitions
   
   Add a "#if defined" block to this file to include support for
   a particular encoder board or library. Then add the appropriate
   #define near the top of the main ROSArduinoBridge.ino file.
   
   ************************************************************ */
#include <Encoder.h>

#ifdef USE_BASE

#if defined ARDUINO_ENC_COUNTER

  Encoder leftEnc(LEFT_ENC_PIN_A, LEFT_ENC_PIN_B);
  Encoder rightEnc(RIGHT_ENC_PIN_A, RIGHT_ENC_PIN_B);
 
  /* Wrap the encoder reading function */
  long readEncoder(int i) {
    if (i == LEFT) return leftEnc.read();
    else return rightEnc.read();
  }

  /* Wrap the encoder reset function */
  void resetEncoder(int i) {
    if (i == LEFT){
      leftEnc.write(0);
      return;
    } else { 
      rightEnc.write(0);
      return;
    }
  }
#else
  #error A encoder driver must be selected!
#endif

/* Wrap the encoder reset function */
void resetEncoders() {
  resetEncoder(LEFT);
  resetEncoder(RIGHT);
}

#endif


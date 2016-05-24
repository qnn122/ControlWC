/* *************************************************************
   Encoder driver function definitions - by James Nugen
   ************************************************************ */
   
   
#ifdef ARDUINO_ENC_COUNTER

  //otherwise additional changes in the code are required
  #define LEFT_ENC_PIN_A 2  //pin 2
  #define LEFT_ENC_PIN_B 3  //pin 3
  
  #define RIGHT_ENC_PIN_A 18  //pin 18
  #define RIGHT_ENC_PIN_B 19   //pin 19
#endif
   
long readEncoder(int i);	
void resetEncoder(int i);
void resetEncoders();


#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg1;
struct can_frame canMsg;

MCP2515 mcp2515(10);
unsigned long prevTime = 0;
const long interval = 10; //send data each 0.01 seconds

void setup() {

  canMsg1.can_id  = 0x0F6;
  canMsg1.can_dlc = 8;
  canMsg1.data[0] = 0x00;
  canMsg1.data[1] = 0x00;
  canMsg1.data[2] = 0x00;
  canMsg1.data[3] = 0xFA;
  canMsg1.data[4] = 0x00;
  canMsg1.data[5] = 0x8E;
  canMsg1.data[6] = 0x00;
  canMsg1.data[7] = 0x86;
  
  while (!Serial);
  Serial.begin(115200);
  SPI.begin();
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_250KBPS);
  mcp2515.setNormalMode();
  Serial.println("Write and read to CAN");
}

void loop() {
    if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK) {
      if(canMsg.can_id !=0x0F6){ //own id
        if(canMsg.can_id ==0x01){
          Serial.println("recieved message to set speed: ");
            canMsg1.data[0] = 0x00;
            canMsg1.data[1] = 0x00;
            canMsg1.data[2] = 0x00;
            canMsg1.data[3] = canMsg.data[0];
        }
        else if(canMsg.can_id ==0x02){
          Serial.println("recieved message to set current: ");
          canMsg1.data[4] = 0x00;
          canMsg1.data[5] = canMsg.data[0];
        }
        else if(canMsg.can_id ==0x03){
          Serial.println("recieved message to set duty cycle: ");
          canMsg1.data[6] = 0x00;
          canMsg1.data[7] = canMsg.data[0];
        }
        Serial.print(canMsg.can_id, HEX); // print ID
        Serial.print(" "); 
        Serial.print(canMsg.can_dlc, HEX); // print DLC
        Serial.print(" ");
                
        for (int i = 0; i<canMsg.can_dlc; i++)  {  // print the data
            
          Serial.print(canMsg.data[i],HEX);
          Serial.print(" ");    
        }
        Serial.println(); 
    }     
 }
 if( millis()-prevTime >= interval){
    prevTime = millis();    
    mcp2515.sendMessage(&canMsg1);
    //Serial.println("Messages sent: ");
 }
  

}

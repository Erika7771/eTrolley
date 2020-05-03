#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg1;
struct can_frame canMsg;

MCP2515 mcp2515(10);
unsigned long prevTime = 0;
const long interval = 500; //send data each 0.5 seconds

void setup() {

  canMsg1.can_id  = 0x0F6;
  canMsg1.can_dlc = 8;
  canMsg1.data[0] = 0x8E;
  canMsg1.data[1] = 0x87;
  canMsg1.data[2] = 0x32;
  canMsg1.data[3] = 0xFA;
  canMsg1.data[4] = 0x26;
  canMsg1.data[5] = 0x8E;
  canMsg1.data[6] = 0xBE;
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
    if(canMsg.can_id !=0x0F6){
      Serial.println("recieved message: ");
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
    Serial.println("Messages sent: ");
 }
  

}

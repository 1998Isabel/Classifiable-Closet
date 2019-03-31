#include "mbed.h"
#include "AsyncStepper/AsyncStepper.hpp"

AsyncStepper a(D6, D5, D4, 200);

DigitalIn  mypin(USER_BUTTON); // change this to the button on your board
DigitalOut myled(LED1);

int main()
{
    // check mypin object is initialized and connected to a pin
    if(mypin.is_connected()) {
        a.Rotate(POSITIVE, 720);
        printf("mypin is connected and initialized! \n\r");
    }
    // press the button and see the console / led change
    while(1) {
        printf("mypin has value : %d \n\r", mypin.read());
        myled = mypin; // toggle led based on value of button
        wait(0.25);
    }
    
}
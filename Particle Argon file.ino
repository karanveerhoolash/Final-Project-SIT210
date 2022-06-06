// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

#include "application.h"
#include "MQTT.h"

MQTT client("test.mosquitto.org", 1883, callback);

void callback(char* topic, byte* payload, unsigned int length) 
{
    char p[length + 1];
    memcpy(p, payload, length);
    p[length] = NULL;

    if (strcmp(p, "on")){
        alarm_on();
    }
}



int alert_pin = D5;

SYSTEM_THREAD(ENABLED);

void setup() {


  pinMode(alert_pin, OUTPUT);
  
  client.connect("sparkclient_" + String(Time.now()));

    // publish/subscribe
    if (client.isConnected()) {
    client.subscribe("alarm/status");
    }

}

2
void loop() {
    client.loop();

}



void alarm_on(){
    
    int count = 0 ;    
    
    while(count < 90) // perform alarm_on procedure for (180 seconds / 2) because we want to sound alarm for at least 3 minutes. Note, the 2 seconds delay.
    {
        Particle.publish("alarm_status", "on"); 
        tone(alert_pin,4000,3000);  
        delay(2000);
        
        count = count +1;
    }
    
}
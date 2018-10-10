#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>

#define wifi_ssid ""
#define wifi_password ""

#define mqtt_server ""
#define mqtt_port 
#define mqtt_user ""  //s'il a été configuré sur Mosquitto
#define mqtt_password "" //idem

#define water_command_topic "cmnd/arrosage"  //Topic commade arrosage
#define water_humidity_stat_topic "tele/arrosage/humidite"  //Topic info arrosage


long lastMsg = 0;   //Horodatage du dernier message publié sur MQTT
long lastRecu = 0;
bool debug = true;  //Affiche sur la console si True


int ON_PIN = 5;
int OFF_PIN = 4;

WiFiClient espClient;
PubSubClient client(espClient);

//Connexion au réseau WiFi
void setup_wifi() {
  delay(10);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

//Reconnexion
void reconnect() {
  //Boucle jusqu'à obtenur une reconnexion
  while (!client.connected()) {
    if (!client.connect("ESP8266Client", mqtt_user, mqtt_password)) {
      delay(5000);
    }
  }
}

/**
 * reset to low state
**/
void reset() {
    digitalWrite(ON_PIN, LOW);
    digitalWrite(OFF_PIN, LOW);
}

/**
 * Turn on water
**/
void turnOn() {
    digitalWrite(OFF_PIN, LOW);
    digitalWrite(ON_PIN, HIGH);
    delay(200);
    reset();
}

/**
 * Turn off water
**/
void turnOff() {
    digitalWrite(ON_PIN, LOW);
    digitalWrite(OFF_PIN, HIGH);
    delay(200);
    reset();
}

void readHumidity() {

    long now = millis();
    //Envoi d'un message par minute
    if (now - lastMsg > 1000 * 10) {
        lastMsg = now;
        //Lecture de l'humidité ambiante
        float h = analogRead(A0);
        client.publish(water_humidity_stat_topic, String(h).c_str(), true);
    } 
    
}

void callback(char* topic, byte* payload, unsigned int length) {
    int i = 0;
    //Buffer qui permet de décoder les messages MQTT reçus
    char message_buff[100];

    if ( debug ) {
        Serial.println("Message recu =>  topic: " + String(topic));
        Serial.print(" | longueur: " + String(length,DEC));
    }
    for (int i = 0; i < length; i++) {
        Serial.print((char)payload[i]);
    }
    // create character buffer with ending null terminator (string)
    for(i=0; i<length; i++) {
        message_buff[i] = (char)payload[i];
    }
    message_buff[i] = '\0';

    String msgString = String(message_buff);
    if ( debug ) {
        Serial.println(" | Payload: " + msgString);
    }

    if ( msgString == "ON" ) {
        turnOn();
    } else if( msgString == "OFF") {
        turnOff(); 
    }
}


void setup() {
    Serial.begin(9600);     //Facultatif pour le debug

    setup_wifi();           //On se connecte au réseau wifi

    client.setServer(mqtt_server, mqtt_port);    //Configuration de la connexion au serveur MQTT
    client.setCallback(callback);  //La fonction de callback qui est executée à chaque réception de message   

    pinMode(ON_PIN, OUTPUT);   
    pinMode(OFF_PIN, OUTPUT);  

    if(!client.connected()) {
        reconnect();
    }

    turnOff();

    client.subscribe(water_command_topic);
}


void loop() {
    client.loop();
    readHumidity();
}
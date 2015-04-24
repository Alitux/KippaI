/*
Este es el modulo central de control de KIPPA I

 */


#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>         // Libreria UDP


// Ingresar datos de conexion (MAC del ethernet Shield e IP)
// La MAC se puede dejar como esta
byte mac[] = {
  0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED
};
// IPAddress ip(10, 30, 121, 113);

unsigned int localPort = 3400;      // Puerto a utilizar

int luces=22; // Luces principales

int mtba=26; // Motor Trasero Babor A
int mtbb=27; // Motor Trasero Babor B

int mtea=28; // Motor Trasero Estribor A
int mteb=29; // Motor Trasero Estribor B

int mcba=32; // Motor Central Babor A
int mcbb=33; // Motor Central Babor B

int mcea=34; // Motor Central Estribor A
int mceb=35; // Motor Central Estribor B

// Buffers para guardar paquetes recibidos
char packetBuffer[UDP_TX_PACKET_MAX_SIZE]; //Se guarda el paquete recibido
// char  ReplyBuffer[] = "acknowledged";       // Un string de respuesta

// Se permite utilizar udp para recibir y enviar paquetes
EthernetUDP Udp;

void setup() {
  // Se inicia la conexion ethernet y el protocolo UDP
  Ethernet.begin(mac);
  Udp.begin(localPort);
  Serial.begin(9600);
  //Luces
  pinMode(luces, OUTPUT);
  //Motor Trasero Estribor
  pinMode(mtba, OUTPUT);
  pinMode(mtbb, OUTPUT);
  //Motor Trasero Estribor 
  pinMode(mtea, OUTPUT);
  pinMode(mteb, OUTPUT);
  //Motor Central Babor
  pinMode(mcba, OUTPUT);
  pinMode(mcbb, OUTPUT);
  //Motor Central Estribor
  pinMode(mcea, OUTPUT);
  pinMode(mceb, OUTPUT);  
}

void loop() {
  // Si existen datos, se lee el paquete.
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // Leer el paquete guardado en el buffer.
    Udp.read(packetBuffer, UDP_TX_PACKET_MAX_SIZE);
    Serial.println(String(packetBuffer));
    // Se detecta y ejecuta una orden posible
    if (String(packetBuffer) == String("2"))
    {
      Serial.println("RETROCESO");
      // Motor Trasero Babor
      digitalWrite(mtba, HIGH);
      digitalWrite(mtbb, LOW);
      // Motor Trasero Estribor      
      digitalWrite(mtea, HIGH);
      digitalWrite(mteb, LOW);
    }
    
    if (String(packetBuffer) == String("-2"))
    {
      Serial.println("STOP RETROCESO");
      // Motor Trasero Babor
      digitalWrite(mtba, LOW);
      digitalWrite(mtbb, LOW);
      // Motor Trasero Estribor      
      digitalWrite(mtea, LOW);
      digitalWrite(mteb, LOW);
    }
    
    if (String(packetBuffer) == String("3"))
    {
      Serial.println("Avante");
      
      // Motor Trasero Babor
      digitalWrite(mtba, LOW);
      digitalWrite(mtbb, HIGH);
      // Motor Trasero Estribor      
      digitalWrite(mtea, LOW);
      digitalWrite(mteb, HIGH);
    }
    
   if (String(packetBuffer) == String("-3"))
    {
      Serial.println("STOP Avante");
      
      // Motor Trasero Babor
      digitalWrite(mtba, LOW);
      digitalWrite(mtbb, LOW);
      // Motor Trasero Estribor      
      digitalWrite(mtea, LOW);
      digitalWrite(mteb, LOW);
    }
    
    
    
    if (String(packetBuffer) == String("4"))
    {
      Serial.println("Caer a estribor");
      // Motor Trasero Babor
      digitalWrite(mtba, LOW);
      digitalWrite(mtbb, HIGH);
    }
    if (String(packetBuffer) == String("-4"))
    {
      Serial.println("STOP estribor");
      // Motor Trasero Babor
      digitalWrite(mtba, LOW);
      digitalWrite(mtbb, LOW);
    }
    
    if (String(packetBuffer) == String("5"))
    {
      Serial.println("Caer a babor");
      // Motor Trasero Babor
      digitalWrite(mtea, LOW);
      digitalWrite(mteb, HIGH);
      
    }
    if (String(packetBuffer) == String("-5"))
    {
      Serial.println("STOP babor");
      // Motor Trasero Babor
      digitalWrite(mtea, LOW);
      digitalWrite(mteb, LOW);
    }
    if (String(packetBuffer) == String("6"))
    {
      Serial.println("Ascender");
      // Motor Central Babor
      digitalWrite(mcba, HIGH);
      digitalWrite(mcbb, LOW);
      // Motor Central Estribor      
      digitalWrite(mcea, LOW);
      digitalWrite(mceb, HIGH);
    }
    
    if (String(packetBuffer) == String("-6"))
    {
      Serial.println("STOP Ascender");
      // Motor Central Babor
      digitalWrite(mcba, LOW);
      digitalWrite(mcbb, LOW);
      // Motor Central Estribor      
      digitalWrite(mcea, LOW);
      digitalWrite(mceb, LOW);
    }
    
    if (String(packetBuffer) == String("7"))
    {
      Serial.println("Descender");
      // Motor Central Babor
      digitalWrite(mcba, LOW);
      digitalWrite(mcbb, HIGH);
      // Motor Central Estribor      
      digitalWrite(mcea, HIGH);
      digitalWrite(mceb, LOW);
    }
    
    if (String(packetBuffer) == String("-7"))
    {
      Serial.println("STOP Descender");
      // Motor Central Babor
      digitalWrite(mcba, LOW);
      digitalWrite(mcbb, LOW);
      // Motor Central Estribor      
      digitalWrite(mcea, LOW);
      digitalWrite(mceb, LOW);
    }
    
    if (String(packetBuffer) == String("-8"))
    {
      Serial.println("STOP TODO");
      // Motor Central Babor
      digitalWrite(mcba, LOW);
      digitalWrite(mcbb, LOW);
      // Motor Central Estribor      
      digitalWrite(mcea, LOW);
      digitalWrite(mceb, LOW);
      // Motor Trasero Babor
      digitalWrite(mtba, LOW);
      digitalWrite(mtbb, LOW);
      // Motor Trasero Estribor      
      digitalWrite(mtea, LOW);
      digitalWrite(mteb, LOW);
    }
    
    if (String(packetBuffer) == String("1"))
    {
      Serial.println("Encendiendo luces");
      // Escribir aqui instrucciones para encender luces
      digitalWrite(luces, HIGH);
     }
    

    if (String(packetBuffer) == String("0"))
    {
      Serial.println("Apagando Luces");
      // Escribir aqui instrucciones para encender luces
      digitalWrite(luces, LOW);
    }
    for(int i=0;i<UDP_TX_PACKET_MAX_SIZE;i++) packetBuffer[i] = 0;
    // send a reply, to the IP address and port that sent us the packet we received
    // Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    // Udp.write(ReplyBuffer);
    // Udp.endPacket();
  }
  
  delay(10);
}


#include <SPI.h>
#include <WiFi101.h>



#define FIREBASE_HOST "www.ratesbu-wrapper-api.appspot.com"
#define FIREBASE_AUTH "qaRKX6XSZTOOAHjjFGyNxlJfD7oa6Mt7ulxEfE4o"
#define WIFI_SSID "iPhone"
#define WIFI_PASSWORD "12345nnn"

int ledPin = 13; // choose the pin for the LED
int inPin = 7;   // choose the input pin (for a pushbutton)
int val = 0;     // variable for reading the pin status
int status = WL_IDLE_STATUS;
WiFiClient client;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;
  }

  pinMode(ledPin, OUTPUT);  // declare LED as output
  pinMode(inPin, INPUT);    // declare pushbutton as input


  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print("..");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());

  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true);
  }

  Serial.println("Connected to wifi");
}

void loop() {
    val = digitalRead(inPin);
  Serial.println(val);
  if (val == HIGH) {
    digitalWrite(ledPin, LOW);
  } else {
    digitalWrite(ledPin, HIGH);
  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  if (client.connect(FIREBASE_HOST, 80)) {
    Serial.println("connected to server");
    // Make a HTTP request:
    client.println("GET /professor HTTP/1.1");
    client.println("Host: www.ratesbu-wrapper-api.appspot.com");
    client.println("Connection: close");
    client.println();
  }
  
  // if there are incoming bytes available
  // from the server, read them and print them:
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  // if the server's disconnected, stop the client:
  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting from server.");
    client.stop();

    // do nothing forevermore:
    while (true);
  }
  }
  delay(100);
}






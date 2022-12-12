package main

import (
	"fmt"
	mqtt "github.com/eclipse/paho.mqtt.golang"
	//    "log"
	"time"
)

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	fmt.Printf("Received message: %s topic %s\n", msg.Payload(),  msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Println("Connection lost: ", err)
}

func main() {
	var broker = "localhost" //"broker.emqx.io" "test.mosquitto.org"
	var port = 1883
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
	opts.SetClientID("go_mqtt_client")
	//opts.SetUsername("emqx")
	//opts.SetPassword("public")
	opts.SetDefaultPublishHandler(messagePubHandler)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler
	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	topic := "datetime" // "topic/test"
	sub(client, topic)

	message := "hello from go client"
	publish(client, topic, message)

	client.Disconnect(250)
}

func publish(client mqtt.Client, topic string, message string) {
	num := 10
	for i := 0; i < num; i++ {
		text := fmt.Sprintf("%d %s", i, message)
		token := client.Publish(topic, 0, false, text)
		token.Wait()
		time.Sleep(time.Second)
	}
}

func sub(client mqtt.Client, topic string) {
	token := client.Subscribe(topic, 1, nil)
	token.Wait()
	fmt.Println("Subscribed to topic: ", topic)
}

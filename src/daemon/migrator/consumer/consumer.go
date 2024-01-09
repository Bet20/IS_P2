package consumer

import (
	"encoding/json"
	"log"
	"migrator/utils"
	"os"
	"os/signal"
	"syscall"
  "fmt"
	"migrator/db"

	"github.com/streadway/amqp"
)

type BrokerMessage struct {
	DocumentId string `json:"document_id"`
}

func Consume() {
	conn, err := amqp.Dial("amqp://is:is@rabbitmq:5672/is")
	if err != nil {
		return
	}

	utils.E(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	utils.E(err, "Failed to open a channel")
	defer ch.Close()

	// Declare a direct exchange named "preference_exchange"
	err = ch.ExchangeDeclare(
		"preference_exchange", // Exchange name
		"direct",              // Exchange type
		true,                  // Durable
		false,                 // Auto-delete
		false,                 // Internal
		false,                 // No-wait
		nil,                   // Arguments
	)
	utils.E(err, "Failed to declare an exchange")

	q, err := ch.QueueDeclare(
		"service_migrator", // Queue name
		false,              // Durable
		false,              // Delete when unused
		false,              // Exclusive
		false,              // No-wait
		nil,                // Arguments
	)
	utils.E(err, "Failed to declare a queue")

	// Bind the queue to the exchange with routing key "low_priority"
	err = ch.QueueBind(
		q.Name,                // Queue name
		"low_priority",        // Routing key
		"preference_exchange", // Exchange name
		false,                 // No-wait
		nil,                   // Arguments
	)
	utils.E(err, "Failed to bind the queue")

	msgs, err := ch.Consume(
		q.Name, // Queue
		"",     // Consumer
		true,   // Auto Acknowledge
		false,  // Exclusive
		false,  // No-local
		false,  // No-wait
		nil,    // Arguments
	)
	utils.E(err, "Failed to register a consumer")

	go func() {
		for msg := range msgs {
			var broker BrokerMessage
			err := json.Unmarshal(msg.Body, &broker)
			if err != nil {
				log.Println("Failed to unmarshal message")
				return
			}
			docReference := db.GetDocument(broker.DocumentId)
			fmt.Printf("Document: %v\n", docReference)
			db.AddDocumentToRelationalDatabase(docReference)
		}
	}()

	log.Printf("Service B [*] Waiting for messages. To exit, press CTRL+C")

	signalCh := make(chan os.Signal, 1)
	signal.Notify(signalCh, syscall.SIGINT, syscall.SIGTERM)
	<-signalCh
	log.Println("Service B Exiting...")
}

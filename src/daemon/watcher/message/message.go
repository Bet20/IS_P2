package message

import (
	"fmt"
	"watcher/utils"

	"github.com/streadway/amqp"
)

func sendCountryShouldCreateMessage(countries []string, queue amqp.Queue, channel *amqp.Channel) {
	msg := "{\"countries\":[" + "\"" + countries[0] + "\""

	for _, c := range countries {
		msg += fmt.Sprintf(`, "%s"`, c)
	}
	msg += "]}"

	fmt.Println(msg)

	err := channel.Publish(
		"preference_exchange",
		"high_priority",
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(msg),
			Priority:    5,
		},
	)

	utils.E(err)
	fmt.Println("Published 'SHOULD CREATE COUNTRY' Successfully")
}

func sendDocumentShouldMigrateMessage(documentId string, queue amqp.Queue, channel *amqp.Channel) {
	msg := fmt.Sprintf(`{"document_id": "%s"}`, documentId)

	err := channel.Publish(
		"preference_exchange",
		"low_priority",
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(msg),
			Priority:    0,
		},
	)

	utils.E(err)
	fmt.Println("Published 'SHOULD MIGRATE' Successfully")
}

func Send(documentId string, countries []string) {
	fmt.Println("Rabbitmq")
	connection, err := amqp.Dial("amqp://is:is@rabbitmq:5672/is")
	if err != nil {
		connection.Close()
		return
	}

	channel, err := connection.Channel()
	utils.E(err, "CHANNEL")
	defer channel.Close()

	queue_arguments := make(amqp.Table)
	queue_arguments["x"] = 10

	var queue amqp.Queue
	err = channel.ExchangeDeclare(
		"preference_exchange", // Exchange name
		"direct",              // Exchange type
		true,                  // Durable
		false,                 // Auto-delete
		false,                 // Internal
		false,                 // No-wait
		nil,
	)
	// queue, err = channel.QueueDeclare(
	// 	"is",
	// 	false,
	// 	false,
	// 	false,
	// 	false,
	// 	queue_arguments,
	// )
	utils.E(err)

	sendCountryShouldCreateMessage(countries, queue, channel)
	sendDocumentShouldMigrateMessage(documentId, queue, channel)
}

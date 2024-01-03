package message

import (
	"fmt"
	"watcher/utils"

	"github.com/streadway/amqp"
)

func sendCountryShouldCreateMessage(country []string, queue amqp.Queue, channel *amqp.Channel) {
	msg := "["
	for _, c := range country {
		msg += fmt.Sprintf(`{"name": "%s"}`, c)
	}
	msg += "]"

	err := channel.Publish(
		"",
		queue.Name,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(msg),
			Priority:    5,
		},
	)

	utils.E(err)
	fmt.Println("Queue: ", queue)
	fmt.Println("Published Successfully")
}

func sendDocumentShouldMigrateMessage(documentId string, queue amqp.Queue, channel *amqp.Channel) {
	err := channel.Publish(
		"",
		queue.Name,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(documentId),
			Priority:    0,
		},
	)

	utils.E(err)
	fmt.Println("Queue: ", queue)
	fmt.Println("Published Successfully")

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

	queue, err = channel.QueueDeclare(
		"is",
		false,
		false,
		false,
		false,
		queue_arguments,
	)
	utils.E(err)

	sendCountryShouldCreateMessage(countries, queue, channel)
	sendDocumentShouldMigrateMessage(documentId, queue, channel)
}

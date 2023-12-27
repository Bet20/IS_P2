package message

import (
	"fmt"
	"watcher/utils"

	"github.com/streadway/amqp"
)

func Send(id string) {
	fmt.Println("Rabbitmq")
	connection, err := amqp.Dial("amqp://is:is@rabbitmq:5672/is")
	utils.E(err)
	defer connection.Close()

	channel, err := connection.Channel()
	utils.E(err)
	defer channel.Close()

	queue, err := channel.QueueDeclare(
		"is",
		false,
		false,
		false,
		false,
		nil,
	)

	utils.E(err)
	err = channel.Publish(
		id,
		queue.Name,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte("There have been changes to the xml document db"),
		},
	)

	utils.E(err)
	fmt.Println("Queue: ", queue)
	fmt.Println("Published Successfully")
}

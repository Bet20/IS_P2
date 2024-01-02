package consumer 

import (
	"fmt"
	"migrator/utils"

	"github.com/streadway/amqp"
)

func Consume() {
	connection, err := amqp.Dial("amqp://is:is@rabbitmq:5672/is")
	utils.E(err)
	defer connection.Close()

  fmt.Println("amqp Consumer")

	channel, err := connection.Channel()
	utils.E(err)
	defer channel.Close()

  msgs, err := channel.Consume(
    "is",
    "",
    true,
    false,
    false,
    false,
    nil,
  )

  utils.E(err)
  forever := make(chan bool)
  go func ()  {
    for msg := range msgs {
      fmt.Println(msg)
    }
  }()

  <-forever
}

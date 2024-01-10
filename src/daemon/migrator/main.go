package main

import (
	"fmt"
	"migrator/consumer"
	"migrator/db"

	// "migrator/db"
	// "os"
	"time"
)

const (
	VERSION       = "0.0.1"
	MIGRATOR_TICK = time.Second * 10
)

func main() {
	fmt.Printf("running Migrator (version %s)", VERSION)
	for range time.Tick(MIGRATOR_TICK) {
		fmt.Printf("MIGRATOR TICK")
		fmt.Printf("%v", db.GetAllDocuments())
		consumer.Consume()
	}
}

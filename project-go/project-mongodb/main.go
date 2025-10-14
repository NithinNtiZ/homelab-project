// Connects to MongoDB and sets a Stable API version
package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func add_data(data userdata) {
	uri := "mongodb://localhost:27017"

	// Set client options
	clientOptions := options.Client().ApplyURI(uri)

	// Connect to MongoDB
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}

	// Create a new context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Ping the database to ensure connection
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatalf("Could not ping MongoDB: %v", err)
	}

	fmt.Println("Connected to MongoDB successfully!")

	// Create a new database and collection
	db := client.Database("Ticket")
	collection := db.Collection("user_info")

	// Insert the document
	_, err = collection.InsertOne(ctx, data)
	if err != nil {
		log.Fatalf("Failed to insert document: %v", err)
	}

	fmt.Println("Inserted a document to create the database!")

	// Close the connection
	if err := client.Disconnect(ctx); err != nil {
		log.Fatalf("Error disconnecting from MongoDB: %v", err)
	}

	fmt.Println("Disconnected from MongoDB")

}

type userdata struct {
	Firstname string `bson:"firstname"`
	Lastname  string `bson:"lastname"`
	Email     string `bson:"email"`
	Age       int    `bson:"age"`
	Ticket    int    `bson:"ticket"`
}

func main() {
	total_ticket := 50
	
	for { 
		var firstname, lastname, email string
		var age, ticket int
		
		if total_ticket <= 0 {

			fmt.Println("out of tickets !!!!")
			break
			} else {
				fmt.Printf("Enter first name: ")
				fmt.Scan(&firstname)
				fmt.Printf("Enter last name: ")
				fmt.Scan(&lastname)
				fmt.Printf("Enter email: ")
				fmt.Scan(&email)
				fmt.Printf("Enter age: ")
				fmt.Scan(&age)
				fmt.Printf("Enter number of tickets: ")
				fmt.Scan(&ticket)
				total_ticket -=ticket
				userData := userdata{
					Firstname: firstname,
					Lastname:  lastname,
					Email:     email,
					Age:       age,
					Ticket:    ticket,
				}
			
				add_data(userData)
			
				fmt.Printf("User %s %s (Age: %d) bought %d ticket(s).\n", userData.Firstname, userData.Lastname, userData.Age, userData.Ticket)
			}
		}
}

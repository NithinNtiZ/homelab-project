package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func main() {
	// Define MongoDB URI
	uri := "mongodb://localhost:27017"

	// Set client options
	clientOptions := options.Client().ApplyURI(uri)

	// Connect to MongoDB
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}

	// Ping the database to ensure connection
	err = client.Ping(ctx, nil)
	if err != nil {
		log.Fatalf("Could not ping MongoDB: %v", err)
	}

	fmt.Println("Connected to MongoDB successfully!")

	// Create a new database and collection
	db := client.Database("Loto")
	collection := db.Collection("env")

	// Insert a dummy document
	for i := 0; i < 10; i++ {

		dummyDoc := bson.D{{Key: "name", Value: fmt.Sprintf("Nithin-%v", i)}, {Key: "created_at", Value: time.Now()}}
		_, err = collection.InsertOne(ctx, dummyDoc)
		if err != nil {
			log.Fatalf("Failed to insert document: %v", err)
		}
	}	
	fmt.Println("Inserted a document to create the database!")

	// Close the connection
	if err := client.Disconnect(ctx); err != nil {
		log.Fatalf("Error disconnecting from MongoDB: %v", err)
	}

	fmt.Println("Disconnected from MongoDB")
}

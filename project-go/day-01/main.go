package main

import (
	"fmt"
)

func userinput() (string, string) {
	fmt.Println("Enter your first name : ")
	var firstname string
	fmt.Scanln(&firstname)
	fmt.Println("Enter you last name : ")
	var lastname string
	fmt.Scanln(&lastname)
	return firstname, lastname
}

type userdata struct {
	Firstname string
	Lastname  string
	Ticket    int
}

var booking []userdata

func main() {

	total := 50

	for {
		firstname, lastname := userinput()
		fmt.Printf("Hello %s %s\n", firstname, lastname)
		fmt.Printf("Enter No of ticket : ")
		var ticket int
		fmt.Scan(&ticket)
		fmt.Printf("thank you for booking %v tickets\n", ticket)
		if ticket > total {
			fmt.Printf("Only %d tickets left.\n", total)
			continue
		}
		total -= ticket
		fmt.Printf("Remaining tickets %v\n", total)
		user := userdata{Firstname: firstname, Lastname: lastname, Ticket: ticket}
		booking = append(booking, user)
		if total < 0 {
			fmt.Println("No more tickets available")
			total += ticket // revert the ticket count
		} else if total == 0 {
			fmt.Println("All tickets are sold out")
			break
		}

	}
	fmt.Println("Booking Summary:")
	// Print the booking summary
	fmt.Printf("Total tickets booked: %v\n", booking)
	for _, b := range booking {
		fmt.Printf("- %s %s booked %d tickets\n", b.Firstname, b.Lastname, b.Ticket)
	}
}

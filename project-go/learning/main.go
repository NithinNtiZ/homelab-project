package main

import (
	"fmt"
)
func greetUser (firstname string) {
	fmt.Printf("Hello %v welcome to the ticket booking system \n", firstname)
}

func userinput () (string, string) {
	var firstname string 
	var lastname string 
	fmt.Println("Enter  your first name: ")
	fmt.Scan(&firstname)
	fmt.Println("Enter  your last name: ")
	fmt.Scan(&lastname)
	return firstname, lastname
}

func isValidUserInput(firstname string, lastname string, num1 int, total int) (bool, bool) {
	isValidFirstname := len(firstname) > 2 && len(lastname) >= 2
	isVlaidTicket := num1 > 0 && num1 <= total
	return isValidFirstname, isVlaidTicket
}


func main () {
	var firstname string 
	var lastname string 
	var total int = 50
	var num1 int
	var list []string
	firstnames := []string{}
	// booking := make([]map[string]string, 0)
	
	type userdata struct {	
		firstname string
		lastname string
		tickets int
	}
	booking := make([]userdata, 0)
	
	for {
		firstname, lastname = userinput()
		greetUser(firstname)
		fmt.Printf("enter no of tickets you want to buy: ")
		fmt.Scan(&num1)
		isValidFirstname, isVlaidTicket := isValidUserInput(firstname, lastname, num1, total)
		if isValidFirstname && isVlaidTicket {
			total -=num1
			
			// userdata := make(map[string]string)
			// userdata["firstname"] = firstname
			// userdata["lastname"] = lastname
			// userdata["tickets"] = strconv.FormatUint(uint64(num1), 10)
			userdata := userdata{
				firstname: firstname,
				lastname: lastname,
				tickets: num1,
			}
			booking = append(booking, userdata)
			firstnames = append(firstnames, userdata.firstname)
			
			
			list = append(list, firstname + " " + lastname)
			fmt.Printf("Your have booked %d tickets, Balance no of ticket is %d\n", num1 , total)
			if total <= 0 {
				fmt.Println("Tickets are sold out")
				break
			}
			} else {
				if !isValidFirstname {
					fmt.Println("Invalid firstname or lastname")
				}
				if !isVlaidTicket {
					fmt.Println("Invalid no of tickets, remaining tickets are ", total)
				}
				
			}
		}
		fmt.Printf("map of people who have booked tickets: %v\n", booking)
		fmt.Printf("List of firstnames of people who have booked tickets: %v\n", firstnames)
		
		for _, a := range booking {
		fmt.Printf("Firstname: %v, Lastname: %v, Tickets: %v\n", a.firstname, a.lastname, a.tickets)
		}
	}
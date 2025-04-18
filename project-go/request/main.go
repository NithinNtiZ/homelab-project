package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
)

func create_file(content string) {

	newFile, _ := os.Create("testfile.txt")
	newFile.WriteString(content)
	defer newFile.Close()
}

func read_file() string {
	filecontent, _ := os.ReadFile("testfile.txt")
	return (string(filecontent))
}

func find_ip() string {
	resp, err := http.Get("https://ifconfig.me")
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	fmt.Printf("response is : %v \n", body)
	return string(body)
}

func main() {
	data := map[string]interface{}{
		"Name":   "Nithin",
		"Age":    25,
		"Skills": []string{"Go", "Python", "Linux"},
	}
	fmt.Printf("the json value is : %v \n", data)
	for {
		var request int
		fmt.Printf("Enter no of request : \n")
		fmt.Scan(&request)
		var wg sync.WaitGroup
		wg.Add(request)

		for i := 0; i < request; i++ {
			go func() {
				defer wg.Done()
				ip := find_ip()
				create_file(ip)
				fmt.Println("IP Address:", ip)
			}()
		}

		wg.Wait()
		break
	}
	fmt.Printf("file content is : %s", read_file())
}

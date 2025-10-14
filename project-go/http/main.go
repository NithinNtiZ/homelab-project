package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type IPInfo struct {
	IPAddr    string `json:"ip_addr"`
	UserAgent string `json:"user_agent"`
	Port      string `json:"port"`
	Method    string `json:"method"`
	Encoding  string `json:"encoding"`
	Via       string `json:"via"`
	Forwarded string `json:"forwarded"`
}

func main() {
	res, err := http.Get("http://ifconfig.me/all.json")
	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	body, err := io.ReadAll(res.Body)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%s\n", body)

	var info IPInfo
	if err := json.Unmarshal(body, &info); err != nil {
		log.Fatal(err)
	}
	fmt.Printf("IP Address: %s\n", info.IPAddr)
}

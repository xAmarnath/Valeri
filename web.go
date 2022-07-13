package main

import (
	"net/http"
	"os"
)

func main() {
	Port := os.Getenv("PORT")
	http.Handle("/", http.FileServer(http.Dir(".")))
	http.ListenAndServe(":"+Port, nil)
}

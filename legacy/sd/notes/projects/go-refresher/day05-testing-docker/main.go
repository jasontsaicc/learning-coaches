package main

import (
	"fmt"
	"net/http"
)

func main() {
	store := NewMemoryStore()
	http.HandleFunc("/keys/", store.handleKeys)
	fmt.Println("Server starting on :8090")
	http.ListenAndServe(":8090", nil)
}

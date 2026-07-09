package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

type MemoryStore struct {
	data map[string]string
}

func NewMemoryStore() *MemoryStore {
	return &MemoryStore{
		data: make(map[string]string),
	}
}

func (s *MemoryStore) Get(key string) (string, bool) {
	val, ok := s.data[key]
	return val, ok
}

func (s *MemoryStore) Set(key string, value string) {
	s.data[key] = value
}

func (s *MemoryStore) Delete(key string) bool {
	_, ok := s.data[key]
	delete(s.data, key)
	return ok
}

type SetValue struct {
	Value string `json:"value"`
}

func (s *MemoryStore) handleKeys(w http.ResponseWriter, r *http.Request) {
	key := strings.TrimPrefix(r.URL.Path, "/keys/")

	switch r.Method {
	case "GET":
		val, ok := s.Get(key)
		if !ok {
			w.WriteHeader(http.StatusNotFound)
			return 
		}
		json.NewEncoder(w).Encode(map[string]string{"key":key, "value": val})

	case "PUT":
		var input SetValue
		json.NewDecoder(r.Body).Decode(&input)
		s.Set(key, input.Value)
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})

	case "DELETE":
		deleted := s.Delete(key)
		if !deleted {
			w.WriteHeader(http.StatusNotFound)
			return
		}
	
		json.NewEncoder(w).Encode(map[string]string{"status":"deleted"})
	default:
		w.WriteHeader(http.StatusMethodNotAllowed)
	}
}

func main() {
	store := NewMemoryStore()
	http.HandleFunc("/keys/", store.handleKeys)
	fmt.Println("Server started on: 8080")
	http.ListenAndServe(":8090", nil)
}

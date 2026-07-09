package main

import "fmt"

type Store interface {
	Get(key string) (string, bool)
	Set(key string, value string)
	Delete(key string) bool
}

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

func main() {
	store := NewMemoryStore()

	store.Set("name", "Jason")
	val, ok := store.Get("name")
	fmt.Println("name:", val, "found:", ok)

	val2, ok2 := store.Get("不存在的key")
	fmt.Println("不存在的key:", val2, "found:", ok2)

	deleted := store.Delete("name")
	fmt.Println("deleted name:", deleted)

	val3, ok3 := store.Get("name")
	fmt.Println("name after delete:", val3, "found:", ok3)

}

package main

import "testing"

func TestMemoryStore(t *testing.T) {
	tests := []struct {
		name        string
		action      string // "set", "get", "delete"
		key         string
		value       string // used for "set"
		expectedVal string // used for "get"
		expectedOk  bool   // used for "get" and "delete"
	}{
		{"set name=Jason", "set", "name", "Jason", "", false},
		{"get name", "get", "name", "", "Jason", true},
		{"get non-existent key", "get", "age", "", "", false},
		{"overwrite name=Bob", "set", "name", "Bob", "", false},
		{"get overwritten name", "get", "name", "", "Bob", true},
		{"delete existing key", "delete", "name", "", "", true},
		{"get after delete", "get", "name", "", "", false},
		{"delete non-existent key", "delete", "name", "", "", false},
	}

	store := NewMemoryStore()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			switch tt.action {
			case "set":
				store.Set(tt.key, tt.value)
			case "get":
				val, ok := store.Get(tt.key)
				if val != tt.expectedVal || ok != tt.expectedOk {
					t.Errorf("Get(%q) = (%q, %v), want (%q, %v)",
						tt.key, val, ok, tt.expectedVal, tt.expectedOk)
				}
			case "delete":
				ok := store.Delete(tt.key)
				if ok != tt.expectedOk {
					t.Errorf("Delete(%q) = %v, want %v",
						tt.key, ok, tt.expectedOk)
				}
			}
		})
	}
}

func BenchmarkSet(b *testing.B) {
	store := NewMemoryStore()
	for i := 1; i < b.N; i++ {
		store.Set("key", "value")
	}
}

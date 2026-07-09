package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"sync/atomic"
)

// global atomic counter — safe for concurrent access
var requestCount atomic.Int64

func main() {
	// --- 1. read config ---
	hostname, _ := os.Hostname()
	port := getEnv("PORT", "8080")
	failRate := getFailRate()

	// --- 2. register handlers ---

	// Handler: GET /
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		count := requestCount.Add(1)

		if failRate > 0 && rand.Float64() < failRate {
			w.WriteHeader(http.StatusInternalServerError)
			fmt.Fprintf(w, "500 ERROR from %s (request #%d)\n", hostname, count)
			return
		}
		fmt.Fprintf(w, "Hello from %s | path=%s | request #%d\n", hostname, r.URL.Path, count)
	})

	// Handler: GET /health
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK from %s\n", hostname)
	})

	// Handler: GET /metrics
	http.HandleFunc("/metrics", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		data := map[string]any{
			"hostname":  hostname,
			"requests":  requestCount.Load(),
			"fail_rate": failRate,
		}
		json.NewEncoder(w).Encode(data)
	})

	// --- 3. start server ---
	log.Printf("Starting server on :%s (host=%s, fail_rate=%.0f%%)\n", port, hostname, failRate*100)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}

// getEnv reads an environment variable with a fallback default
func getEnv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

// getFailRate reads FAIL_RATE env var and returns float64 (0.0 ~ 1.0)
func getFailRate() float64 {
	v := os.Getenv("FAIL_RATE")
	if v == "" {
		return 0
	}
	f, err := strconv.ParseFloat(v, 64)
	if err != nil {
		return 0
	}
	return f
}

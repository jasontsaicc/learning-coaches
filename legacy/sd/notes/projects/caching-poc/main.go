package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"sync/atomic"
	"time"

	"github.com/redis/go-redis/v9"
)

var (
	rdb           *redis.Client
	cacheHits     atomic.Int64
	cacheMisses   atomic.Int64
	cacheDisabled bool
	dbLatency     = 50 * time.Millisecond
)

func main() {
	redisAddr := os.Getenv("REDIS_ADDR")
	if redisAddr == "" {
		redisAddr = "localhost:6379"
	}
	cacheDisabled = os.Getenv("CACHE_DISABLED") == "true"

	rdb = redis.NewClient(&redis.Options{
		Addr: redisAddr,
	})

	ctx := context.Background()
	if err := rdb.Ping(ctx).Err(); err != nil {
		log.Printf("WARNING: Redis not available: %v", err)
	} else {
		log.Println("Connected to Redis")
	}

	http.HandleFunc("/items/", handleGetItem)
	http.HandleFunc("/metrics", handleMetrics)

	log.Println("Server starting on :8085")
	log.Fatal(http.ListenAndServe(":8085", nil))
}

// TODO(human): Implement handleGetItem — cache-aside pattern
// 1. Extract ID from URL path: strings.TrimPrefix(r.URL.Path, "/items/")
// 2. If !cacheDisabled → try rdb.Get(ctx, "item:"+id)
// 3. Hit → cacheHits.Add(1), return cached value
// 4. Miss (errors.Is(err, redis.Nil)) → call simulateDB(id), rdb.Set with 30s TTL, cacheMisses.Add(1)
// 5. Return JSON: fmt.Fprintf(w, `{"id":"%s","data":"%s","cache":"hit/miss"}`, id, data)
func handleGetItem(w http.ResponseWriter, r *http.Request) {
	id := strings.TrimPrefix(r.URL.Path, "/items/")
	ctx := context.Background()
	var data string
	cacheStatus := "miss"

	if !cacheDisabled {
		val, err := rdb.Get(ctx, "item:"+id).Result()
		if err == nil {
			// cache hit
			data = val
			cacheStatus = "hit"
			cacheHits.Add(1)
		} else {
			// cache miss — read DB, write cache
			data = simulateDB(id)
			rdb.Set(ctx, "item:"+id, data, 30*time.Second)
			cacheMisses.Add(1)
		}
	} else {
		// cache disabled
		data = simulateDB(id)
		cacheMisses.Add(1)
	}
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"id":"%s","data":"%s","cache":"%s"}`, id, data, cacheStatus)
}

func handleMetrics(w http.ResponseWriter, r *http.Request) {
	hits := cacheHits.Load()
	misses := cacheMisses.Load()
	total := hits + misses

	var hitRatio float64
	if total > 0 {
		hitRatio = float64(hits) / float64(total) * 100
	}

	w.Header().Set("Content-Type", "application/json")
	fmt.Fprintf(w, `{"hits":%d,"misses":%d,"total":%d,"hit_ratio":"%.1f%%"}`, hits, misses, total, hitRatio)
}

// simulateDB fakesf a slow database query
func simulateDB(id string) string {
	time.Sleep(dbLatency)
	return fmt.Sprintf("db-record-for-%s", id)
}

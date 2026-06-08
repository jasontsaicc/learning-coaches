package main

import (
	"fmt"
	"time"
)

type TokenBucket struct {
	capacity   float64
	tokens     float64
	refillRate float64
	lastRefill time.Time
}

func NewTokenBucket(capacity, refillRate float64) *TokenBucket {
	return &TokenBucket{
		capacity:   capacity,
		tokens:     capacity,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
}

func (b *TokenBucket) Allow() bool {
	// TODO(human): implement lazy-refill + take-one-token.
	//   1. elapsed seconds since b.lastRefill  → time.Since(b.lastRefill).Seconds()
	//   2. b.tokens += elapsed * b.refillRate, but cap at b.capacity (use min)
	//   3. update b.lastRefill = time.Now()
	//   4. if b.tokens >= 1 { consume one, return true } else { return false }
	return false
}

func min(a, b float64) float64 {
	if a < b {
		return a
	}
	return b
}

func main() {
	bucket := NewTokenBucket(100, 10)
	allowed, rejected := 0, 0
	for i := 0; i < 120; i++ {
		if bucket.Allow() {
			allowed++
		} else {
			rejected++
		}
	}
	time.Sleep(1 * time.Second)
	refillAllowed := 0
	for i := 0; i < 20; i++ {
		if bucket.Allow() {
			refillAllowed++
		}
	}
	fmt.Printf("\nAfter 1s refill, retrying 20 requests:\n")
	fmt.Printf("  allowed  = %d  (expected ~10)\n", refillAllowed)
}

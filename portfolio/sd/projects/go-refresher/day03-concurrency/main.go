package main

import (
	"fmt"
	"sync"
)

func main() {
	ch := make(chan string)
	go func() {
		for i := 0; i < 5; i++ {
			ch <- fmt.Sprintf("訂單 %d", i)
		}
		close(ch)
	}()

	// TODO(human): Add 2 consumer goroutines with WaitGroup
	// 1. var wg sync.WaitGroup
	// 2. wg.Add(2)
	// 3. Two go func() with defer wg.Done() + for msg := range ch
	// 4. wg.Wait()
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		for msg := range ch {
			fmt.Println("Consumer 1:", msg)
		}
	}()

	go func() {
		defer wg.Done()
		for msg := range ch {
			fmt.Println("consumer2:", msg)
		}
	}()
	wg.Wait()
}

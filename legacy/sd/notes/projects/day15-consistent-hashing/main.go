package main

import "fmt"

func main() {
	r := New(1) // 1 vnode = baseline (same as before, no vnoding)
	r.Add("server-A")
	r.Add("server-B")
	r.Add("server-C")

	fmt.Println("Ring state after adding 3 nodes:")
	fmt.Println("─────────────────────────────────")
	for i, h := range r.keys {
		fmt.Printf("  [%d] hash=%-12d → node=%s\n", i, h, r.hashMap[h])
	}
	fmt.Println("─────────────────────────────────")
	fmt.Printf("Total positions on ring: %d\n\n", len(r.keys))

	// ── Sample keys: show which node owns each ──
	fmt.Println("Sample key → node assignment:")
	fmt.Println("─────────────────────────────────")
	for _, k := range []string{"user-1", "user-42", "user-100", "session-abc", "order-xyz"} {
		fmt.Printf("  Get(%-13q) → %s\n", k, r.Get(k))
	}
	fmt.Println()

	// ── Distribution test: 10,000 keys across 3 nodes ──
	fmt.Println("Distribution over 10,000 keys (no vnodes yet):")
	fmt.Println("─────────────────────────────────")
	counts := map[string]int{}
	for i := 0; i < 10000; i++ {
		key := fmt.Sprintf("key-%d", i)
		node := r.Get(key)
		counts[node]++
	}
	for _, node := range []string{"server-A", "server-B", "server-C"} {
		c := counts[node]
		pct := float64(c) / 100.0
		fmt.Printf("  %-10s: %5d keys (%.2f%%)\n", node, c, pct)
	}
}

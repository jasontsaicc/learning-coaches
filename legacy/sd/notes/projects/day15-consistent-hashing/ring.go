package main

import (
	"fmt"
	"hash/crc32"
	"sort"
)

// Ring is the consistent hash ring.
type Ring struct {
	vnodes  int               // virtual nodes per physical node (1 = no vnodes)
	keys    []uint32          // sorted hash positions on the ring
	hashMap map[uint32]string // hash position -> PHYSICAL node name
}

// New creates an empty Ring with `vnodes` virtual nodes per physical node.
// Pass 1 to disable vnodes; pass 150 for production-quality distribution.
func New(vnodes int) *Ring {
	return &Ring{
		vnodes:  vnodes,
		hashMap: make(map[uint32]string),
	}
}

// hash computes the CRC32 hash of a string.
func hash(key string) uint32 {
	return crc32.ChecksumIEEE([]byte(key))
}

// Add inserts a node into the ring.
// Each node occupies ONE position on the ring (no vnodes yet — Stage 3 adds them).
// Add inserts a physical node into the ring.
// Each physical node creates r.vnodes virtual positions on the ring,
// all mapped back to the same physical node name.
func (r *Ring) Add(node string) {
	for i := 0; i < r.vnodes; i++ {
		vnodeName := fmt.Sprintf("%s#%d", node, i)
		h := hash(vnodeName)
		r.keys = append(r.keys, h)
	}
}

// Get returns the node that owns the given key.
// Rule: find the first node CLOCKWISE on the ring whose hash >= key's hash.
// If key's hash exceeds all node hashes, wrap around to the first node.
func (r *Ring) Get(key string) string {
	if len(r.keys) == 0 {
		return ""
	}
	h := hash(key)
	idx := sort.Search(len(r.keys), func(i int) bool {
		return r.keys[i] >= h
	})
	if idx == len(r.keys) {
		idx = 0
	}
	return r.hashMap[r.keys[idx]]
}

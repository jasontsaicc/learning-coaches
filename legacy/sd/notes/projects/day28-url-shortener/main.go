package main

import (
	"flag"
	"fmt"
	"sort"
	"sync"
	"time"
)

// base62 的 62 個符號:索引 0~61 各對應一個字元。
// 用 const = 這是一張固定查表,誰想改它就編譯失敗。
const alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

// base62Encode 把一個「全域唯一的數字」換成 base62 字串。
// 注意:輸入是 counter 那個數字,跟長網址內容完全無關。
// 機制就是反覆除以 62,把餘數查表 → 自然長度,不補 0。
func base62Encode(n int64) string {
	if n == 0 {
		return string(alphabet[0]) // 特例:0 → "0"
	}
	var buf []byte
	for n > 0 {
		r := n % 62                    // ① 這一位是第幾個符號
		buf = append(buf, alphabet[r]) // ② 查表拿 byte 收集起來
		n = n / 62                     // ③ 砍掉這一位,迴圈才會停
	}
	reverse(buf) // 除法從低位先吐,要反過來才是正確順序
	return string(buf)
}

func reverse(b []byte) {
	for i, j := 0, len(b)-1; i < j; i, j = i+1, j-1 {
		b[i], b[j] = b[j], b[i]
	}
}

// ---------------------------------------------------------------------------
// KGS (Key Generation Service):中央發號器,是「號碼」的唯一真相來源。
// 重點:不是每生一個碼就跟 KGS 要一次(那 KGS 會變瓶頸 + 網路 hop 爆量),
// 而是每台機器一次跟 KGS 領「一整塊 (block)」號碼,自己慢慢用。
// 機器掛掉 → 那塊剩下的號碼丟掉 = 號碼出現空洞 = 完全 OK(短碼不需連續)。
// ---------------------------------------------------------------------------
type KGS struct {
	mu      sync.Mutex // 多台機器同時來領,要互斥保證不發重號
	counter int64      // 下一個還沒發出去的號
}

// AllocBlock 發一整塊號碼 [start, end) 給呼叫者,並把游標往前推。
func (k *KGS) AllocBlock(size int64) (start, end int64) {
	k.mu.Lock()
	defer k.mu.Unlock()
	start = k.counter
	k.counter += size
	end = k.counter
	return
}

// Worker 模擬一台短網址機器,手上握著一塊從 KGS 領來的號碼。
type Worker struct {
	id        int
	kgs       *KGS
	blockSize int64
	next      int64 // 這塊裡下一個要用的號
	end       int64 // 這塊的上界(用到這就要再領)
}

// Next 吐出一個全域唯一的號;塊用完了就自動再跟 KGS 領一塊。
func (w *Worker) Next() int64 {
	if w.next >= w.end {
		w.next, w.end = w.kgs.AllocBlock(w.blockSize)
	}
	n := w.next
	w.next++
	return n
}

func main() {
	workers := flag.Int("workers", 50, "模擬幾台機器同時生碼")
	perWorker := flag.Int("per", 10000, "每台機器生幾個短碼")
	blockSize := flag.Int64("block", 1000, "每次跟 KGS 領多大一塊")
	dropBlocks := flag.Bool("drop", false, "失敗注入:每台機器用到一半就丟掉整塊(模擬當機)")
	flag.Parse()

	// --- 0. 先驗證 encoder 本身對不對(對齊手算) ---
	fmt.Println("== base62Encode sanity ==")
	for _, tc := range []struct {
		n    int64
		want string
	}{{0, "0"}, {1, "1"}, {61, "Z"}, {62, "10"}, {125, "21"}} {
		got := base62Encode(tc.n)
		mark := "OK"
		if got != tc.want {
			mark = "FAIL"
		}
		fmt.Printf("  encode(%d) = %q (want %q) %s\n", tc.n, got, tc.want, mark)
	}

	// --- 1. 多台機器並行生碼,全部丟進各自的 slice(無共享狀態) ---
	kgs := &KGS{}
	results := make([][]string, *workers)
	var wg sync.WaitGroup
	start := time.Now()

	for i := 0; i < *workers; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			w := &Worker{id: id, kgs: kgs, blockSize: *blockSize}
			codes := make([]string, 0, *perWorker)
			for j := 0; j < *perWorker; j++ {
				// 失敗注入:用到半塊就強制丟棄,下一個 Next() 會再領新塊
				if *dropBlocks && j > 0 && j%(*perWorker/2) == 0 {
					w.next = w.end // 假裝當機,手上這塊作廢
				}
				codes = append(codes, base62Encode(w.Next()))
			}
			results[id] = codes
		}(i)
	}
	wg.Wait()
	elapsed := time.Since(start)

	// --- 2. 合併 + 碰撞檢查(核心主張:零碰撞) ---
	total := 0
	seen := make(map[string]bool)
	collisions := 0
	lenDist := map[int]int{}
	for _, codes := range results {
		for _, c := range codes {
			total++
			lenDist[len(c)]++
			if seen[c] {
				collisions++
			} else {
				seen[c] = true
			}
		}
	}

	// --- 3. Production hooks:metrics ---
	fmt.Println("\n== run report ==")
	fmt.Printf("  workers           : %d\n", *workers)
	fmt.Printf("  codes generated   : %d\n", total)
	fmt.Printf("  unique codes      : %d\n", len(seen))
	fmt.Printf("  COLLISIONS        : %d  <-- 核心主張:必須是 0\n", collisions)
	fmt.Printf("  KGS final counter : %d  (含被丟棄的空洞號)\n", kgs.counter)
	fmt.Printf("  elapsed           : %s\n", elapsed)
	fmt.Printf("  throughput        : %.0f codes/sec\n", float64(total)/elapsed.Seconds())

	fmt.Println("  code length dist  :")
	lens := make([]int, 0, len(lenDist))
	for l := range lenDist {
		lens = append(lens, l)
	}
	sort.Ints(lens)
	for _, l := range lens {
		fmt.Printf("    %d 碼: %d 個\n", l, lenDist[l])
	}

	if *dropBlocks {
		gaps := kgs.counter - int64(total)
		fmt.Printf("  dropped (空洞) numbers: %d  <-- 機器當機丟掉的號,沒造成碰撞\n", gaps)
	}
}

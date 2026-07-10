# Pre-Migration Archive (leetcode)

Converted 2026-07-10 from the standalone `leetcode-notes` repo (remote
`github.com:jasontsaicc/leetcode-notes.git`, HEAD `e93fd23`, tag `pre-migration`).
Files here are verbatim originals, never updated again. Full git history:
`legacy/leetcode/notes/` (learner repo) and `legacy/leetcode/coach/` (standalone
skill repo, remote `leetcode_coach.git`, HEAD `c76c79e`, tag `pre-migration`).

## Reconciliation (entry counts, original vs converted)

| Table (original) | Rows | Converted to |
|------------------|:---:|--------------|
| Problem Log | 16 | `session-log.md` verbatim; evidence distilled into progress.md Mastery |
| Interview Drill Scorecard | 1 | progress.md Scorecard history, `certifier: coach`, pre-Examiner 標記 |
| Mistake Registry | 69 (15 open / 54 resolved) | 15 open → progress.md Mistake Registry(原狀態原文引註);54 resolved 留本檔,不逐列重排 |
| Pattern One-Liner Library | 16 | `one-liner-library.md` verbatim(domain registry)|
| Phase Gate Results | 0 | 無可轉;P0 gate 列為舊債,不回填 retroactive pass |

Meta: session_count 16;last_session_date 2026-07-08;weekly review 從未跑過(→ S17 逾期補跑)。

## Conversion rules applied

- Session 編號為鍵、無日期的列:保留 `(sN)` + `(未記日期)`,不發明日期。
- 間隔複習排程:migration 初始化近似值。已知日期(S15=2026-07-02、S16=2026-07-08)照
  原相對排程推算(+3d/+7d);S13/S14 以其 commit 日 2026-07-02 起算標 `(approx)`;
  無日期舊列以轉換日 2026-07-10 起算。原始相對排程於各列原文引註。
- 🟡(Parked / Recurring / Re-test)一律轉 `unresolved`,原狀態原文引註。
- unresolved-session-count 以「建立 session 至 S16 的 session 數」近似;≥5 者標
  Priority Override。
- 舊 chapter 檔案 → 新 `<phase>/<slug>/` layout(對映見下);舊解答無 harness 測試,
  不補造,複習到該題時再補。

## Known discrepancies (recorded, not merged)

- 舊 `CLAUDE.md`(legacy/leetcode/notes/)的 Learning Record 記有 2026-01~02 的
  15 題(Two Sum、3Sum、Two Sum II、Group Anagrams 等),早於本 archive 的起算日
  (2026-03-17),且其「DevOps 精選進度 18/48(A&H 9/9、TP 4/4)」與本檔 Topic
  Mastery(A&H 5/11、TP 2.5/5)計數基礎不同(精選子集 vs NeetCode 全量)。
  依 archive 自我宣告的 single source of truth 原則,轉換以本檔為準;
  1-2 月的題目證據體現在對應 solution 檔案存在,mastery 不因此上調。
- 課綱轉換:standalone 的 DevOps 精選 ~50 題課綱不再使用;新課綱 = NeetCode 150
  E+M 全量照序 + DevOps 優先標注(使用者 2026-07-10 決策,見 curriculum hook)。

## File mapping (old chapter layout → new phase/slug layout)

    000_complexity_demo.py -> p0-mental-model/complexity-demo/solution.py
    arrays_and_hashing/001_two_sum_notes.md -> p1-arrays-hashing/two-sum/notes.md
    arrays_and_hashing/001_two_sum.py -> p1-arrays-hashing/two-sum/solution.py
    arrays_and_hashing/002_contains_duplicate_notes.md -> p1-arrays-hashing/contains-duplicate/notes.md
    arrays_and_hashing/002_contains_duplicate.py -> p1-arrays-hashing/contains-duplicate/solution.py
    arrays_and_hashing/003_valid_anagram_notes.md -> p1-arrays-hashing/valid-anagram/notes.md
    arrays_and_hashing/003_valid_anagram.py -> p1-arrays-hashing/valid-anagram/solution.py
    arrays_and_hashing/004_group_anagrams_notes.md -> p1-arrays-hashing/group-anagrams/notes.md
    arrays_and_hashing/004_group_anagrams.py -> p1-arrays-hashing/group-anagrams/solution.py
    arrays_and_hashing/005_top_k_frequent_notes.md -> p1-arrays-hashing/top-k-frequent/notes.md
    arrays_and_hashing/005_top_k_frequent.py -> p1-arrays-hashing/top-k-frequent/solution.py
    arrays_and_hashing/006_product_of_array_except_self_notes.md -> p1-arrays-hashing/product-of-array-except-self/notes.md
    arrays_and_hashing/006_product_of_array_except_self.py -> p1-arrays-hashing/product-of-array-except-self/solution.py
    arrays_and_hashing/007_single_number_notes.md -> p1-arrays-hashing/single-number/notes.md
    arrays_and_hashing/007_single_number.py -> p1-arrays-hashing/single-number/solution.py
    arrays_and_hashing/008_intersection_of_two_arrays_notes.md -> p1-arrays-hashing/intersection-of-two-arrays/notes.md
    arrays_and_hashing/008_intersection_of_two_arrays.py -> p1-arrays-hashing/intersection-of-two-arrays/solution.py
    arrays_and_hashing/009_missing_number_notes.md -> p1-arrays-hashing/missing-number/notes.md
    arrays_and_hashing/009_missing_number.py -> p1-arrays-hashing/missing-number/solution.py
    arrays_and_hashing/010_majority_element_notes.md -> p1-arrays-hashing/majority-element/notes.md
    arrays_and_hashing/010_majority_element.py -> p1-arrays-hashing/majority-element/solution.py
    arrays_and_hashing/011_valid_sudoku_notes.md -> p1-arrays-hashing/valid-sudoku/notes.md
    arrays_and_hashing/011_valid_sudoku.py -> p1-arrays-hashing/valid-sudoku/solution.py
    arrays_and_hashing/012_encode_and_decode_strings_notes.md -> p1-arrays-hashing/encode-and-decode-strings/notes.md
    arrays_and_hashing/012_encode_and_decode_strings.py -> p1-arrays-hashing/encode-and-decode-strings/solution.py
    arrays_and_hashing/012_encode_and_decode_strings_test.py -> p1-arrays-hashing/encode-and-decode-strings/test_encode_and_decode_strings.py
    arrays_and_hashing/013_longest_consecutive_sequence_notes.md -> p1-arrays-hashing/longest-consecutive-sequence/notes.md
    arrays_and_hashing/013_longest_consecutive_sequence.py -> p1-arrays-hashing/longest-consecutive-sequence/solution.py
    two_pointers/001_valid_palindrome_notes.md -> p1-arrays-hashing/valid-palindrome/notes.md
    two_pointers/001_valid_palindrome.py -> p1-arrays-hashing/valid-palindrome/solution.py
    two_pointers/001_valid_palindrome_share.md -> p1-arrays-hashing/valid-palindrome/share.md
    two_pointers/002_two_sum_ii_notes.md -> p1-arrays-hashing/two-sum-ii/notes.md
    two_pointers/002_two_sum_ii.py -> p1-arrays-hashing/two-sum-ii/solution.py
    two_pointers/003_3sum_notes.md -> p1-arrays-hashing/3sum/notes.md
    two_pointers/003_3sum.py -> p1-arrays-hashing/3sum/solution.py
    two_pointers/004_container_with_most_water_notes.md -> p1-arrays-hashing/container-with-most-water/notes.md
    two_pointers/004_container_with_most_water.py -> p1-arrays-hashing/container-with-most-water/solution.py
    two_pointers/005_trapping_rain_water_notes.md -> p1-arrays-hashing/trapping-rain-water/notes.md
    two_pointers/005_trapping_rain_water.py -> p1-arrays-hashing/trapping-rain-water/solution.py
    two_pointers/two_pointers_template.py -> p1-arrays-hashing/two_pointers_template.py
    sliding_window/001_longest_substring_without_repeating.py -> p2-window-stack/longest-substring-without-repeating/solution.py
    sliding_window/002_permutation_in_string.py -> p2-window-stack/permutation-in-string/solution.py
    sliding_window/003_sliding_window_maximum_notes.md -> p2-window-stack/sliding-window-maximum/notes.md
    sliding_window/003_sliding_window_maximum.py -> p2-window-stack/sliding-window-maximum/solution.py
    stack/001_valid_parentheses.py -> p2-window-stack/valid-parentheses/solution.py
    stack/002_evaluate_rpn.py -> p2-window-stack/evaluate-rpn/solution.py
    stack/003_min_stack_notes.md -> p2-window-stack/min-stack/notes.md
    stack/003_min_stack.py -> p2-window-stack/min-stack/solution.py
    stack/004_daily_temperatures_cold.py -> p2-window-stack/daily-temperatures/solution_cold.py
    stack/004_daily_temperatures.py -> p2-window-stack/daily-temperatures/solution.py
    stack/005_car_fleet.py -> p2-window-stack/car-fleet/solution.py
    stack/006_largest_rectangle_in_histogram.html -> p2-window-stack/largest-rectangle-in-histogram/visual.html
    stack/006_largest_rectangle_in_histogram_notes.md -> p2-window-stack/largest-rectangle-in-histogram/notes.md
    stack/006_largest_rectangle_in_histogram.py -> p2-window-stack/largest-rectangle-in-histogram/solution.py
    binary_search/001_binary_search.py -> p3-binsearch-linkedlist/binary-search/solution.py

# HexDoku HDC-Lite v1

Status: **Reference encoder strategy / experimental**

HDC-Lite v1 defines a deliberately small encoder for Sudoku Profile v1.

The encoder starts from a completed ParityGrid and searches for a 25-hole mask that is cheap for HDE to reconstruct.

## 1. Core idea

HDC knows the completed Sudoku ParityGrid before it removes cells.

Therefore HDC does not need to solve an unknown puzzle first. It can use the known final state to search for a reconstruction-friendly hole pattern.

~~~text
completed ParityGrid
        |
        v
generate a small family of 25-hole masks
        |
        v
run the exact HDE/Sudoku-v1 reconstruction on each mask
        |
        v
keep only masks that reconstruct the original ParityGrid exactly
        |
        v
choose the cheapest canonical mask
~~~

The ParityGrid may be used by HDC to verify a candidate mask, but HDE must not require the hidden ParityGrid in order to choose digits.

## 2. Fixed 9+9+7 baseline

The first HDC-Lite profile fixes the removed digit multiplicities to:

~~~text
digit 1: remove all 9 occurrences
digit 2: remove all 9 occurrences
digit 3: remove 7 of its 9 occurrences
total:   9 + 9 + 7 = 25 holes
~~~

Digits 4 through 9 remain visible.

Because a completed Sudoku contains every digit exactly nine times, the only free mask choice is which two occurrences of digit 3 remain visible.

Number of possible masks:

~~~text
C(9, 2) = C(9, 7) = 36
~~~

Therefore an exhaustive HDC-Lite v1 mask search requires only 36 candidate masks.

## 3. Canonical six-bit mask rank

List the nine coordinates containing digit 3 in row-major order:

~~~text
C0, C1, ... C8
~~~

Choose the two positions that remain visible.

The unordered pair is ranked canonically among the 36 combinations.

~~~text
mask_rank in 0..35
~~~

A fixed six-bit field is sufficient:

~~~text
2^5 = 32 < 36 <= 64 = 2^6
~~~

Ranks 36..63 are invalid and must be rejected.

Because removal of every 1 and every 2 is implicit in the profile, those 18 hole coordinates do not need to be listed separately.

## 4. Candidate domain consequence

Under the fixed 9+9+7 construction, every hole originally contains 1, 2, or 3.

Digits 4..9 remain placed in the board.

For a valid Sudoku state, this strongly restricts the hole candidate domain and often reduces active local candidates to a subset of:

~~~text
{1, 2, 3}
~~~

This is a property to measure, not an assumption that every active cell always has all three candidates.

## 5. Exact acceptance test

For every one of the 36 masks, HDC performs the following:

1. create the 25-hole board;
2. derive E0..E24 in the normal row-major rule;
3. run the exact Sudoku Profile v1 q/HR procedure;
4. run the exact HDE commit resolver without consulting the hidden ParityGrid;
5. materialize the reconstructed 81-cell result;
6. accept the mask only if the reconstructed result is bit-for-bit equal to the source ParityGrid.

Formally:

~~~text
HDE(masked_board, sudoku-v1) == source_ParityGrid
~~~

must hold.

If no mask among the 36 candidates satisfies this equality, HDC-Lite v1 reports `NO_MASK` and a later/fallback profile is required.

## 6. Canonical mask scoring

If multiple masks reconstruct the source ParityGrid exactly, choose one by the following lexicographic score:

1. maximize `forced_prefix`: the number of earliest scheduled commits whose target has HR0 before any feasibility search;
2. maximize `forced_total`: the total number of scheduled commits observed at HR0;
3. minimize `candidate_cost = sum_t |Candidates(E_t)|` over the 24 normal target commits;
4. minimize `trajectory_nonzero_q`: the number of non-zero q entries across the full 325-state DNA trajectory;
5. minimize `trajectory_change_count`: canonical q-symbol changes from one serialized q symbol to the next;
6. minimize `mask_rank` as the final deterministic tie-break.

This score is an encoder search heuristic. It does not change HDE semantics.

Compression claims must still use actual encoded byte counts rather than the score itself.

## 7. Search size

The baseline mask search has only:

~~~text
36 masks
~~~

If each candidate is evaluated over all 325 active coordinate states and only the three potentially absent digits are fast-path evaluated, the upper-level accounting is:

~~~text
36 × 325 × 3 = 35,100 candidate-score slots
~~~

This number is only a structural operation count. Exact runtime also includes Sudoku feasibility checks and must be benchmarked rather than inferred from this count.

## 8. Bit-mask implementation

A lightweight implementation can represent Sudoku legality with nine-bit masks:

~~~text
row_mask[9]
col_mask[9]
box_mask[9]
~~~

For a cell c:

~~~text
used = row_mask[row(c)] | col_mask[col(c)] | box_mask[box(c)]
legal = FULL_1_TO_9_MASK & ~used
~~~

This makes local candidate generation constant-size integer work.

The entire DNA trajectory does not need to be retained in memory. HDC may stream q symbols into histogram, entropy, and change-count accumulators.

## 9. Generalized 9+9+7 search

A later HDC-Lite mode may choose which digits play the 9+9+7 roles.

Choose:

- two digits to remove completely;
- one different digit from the remaining seven;
- seven of that digit's nine occurrences to remove.

Number of configurations:

~~~text
C(9,2) × 7 × C(9,7)
= 36 × 7 × 36
= 9,072
~~~

A fixed 14-bit rank is sufficient:

~~~text
2^13 = 8,192 < 9,072 <= 16,384 = 2^14
~~~

This generalized mode is not the first baseline. The fixed digits 1,2,3 mode is used first so measurements remain easy to reproduce.

## 10. HDC-Lite descriptor

In the **received-board baseline**, `mask_rank` is an HDC-internal/analysis value and does not need to be transmitted: the 25 hole coordinates are already visible in the received 81-cell board.

An alternate compressed descriptor may still contain:

~~~text
profile_id       = sudoku-v1/hdc-lite-9-9-7-v1
mask_rank        = 6 bits
rule_version
optional integrity/reference fields
~~~

but that is a different transport profile. The six-bit mask rank never encodes an unknown ParityGrid by itself.

## 11. HDE path

HDE receives/reconstructs the masked Sudoku board and the profile identifier.

It then:

1. recreates E0..E24;
2. computes q and HR deterministically;
3. performs the fixed 24 commits;
4. resolves the final Sudoku cell;
5. validates Sudoku constraints;
6. verifies any provided final digest/reference.

HDE does not repeat the 36-mask encoder search.

## 12. Benchmark requirements

Measure at least:

- number of ParityGrids tested;
- masks accepted / rejected;
- distribution of selected mask_rank;
- forced_prefix and forced_total;
- candidate_cost;
- q histogram and entropy;
- trajectory_nonzero_q;
- trajectory_change_count;
- HDC search time;
- HDE reconstruction time;
- raw DNA bytes;
- compressed DNA bytes;
- descriptor bytes;
- exact Parity equality.

Only measured results should be reported as HDC-Lite performance.

## 13. Received-board HDE target

The current baseline sends the 25-hole board itself to HDE.

Under fixed `9+9+7`, the simple board encoding is 243 bits because the only cell symbols on wire are `HOLE,3,4,5,6,7,8,9`.

From that board, HDE derives the 25 coordinates, solved values, deterministic order, HR values, and HR branch-slot positions. These derived fields therefore add zero transmission bits when the rule profile is pinned.

A 41-bit canonical-transform Seed remains an alternate restricted transport experiment and is not the current baseline.

See [HDE_MIN_PACKET.md](HDE_MIN_PACKET.md) and [ONE_BOARD_DERIVED_INFORMATION.md](ONE_BOARD_DERIVED_INFORMATION.md).

## 14. Coverage result of fixed 36-mask family

The 500-board order-bearing corpus benchmark evaluated all 36 fixed `9+9+7` masks for every completed board:

~~~text
500 boards
18,000 masks
3,780 exact-round-trip masks
367 boards with >=1 valid mask
133 boards with NO_MASK
~~~

Therefore the fixed 36-mask family is **not a complete coverage profile** for the tested corpus.

For information-bearing derived order, the same corpus measured `K=0..30`. Some successful boards had only `K=1`, so the current fixed family guarantees zero independent order bits.

The next HDC experiment should expand the candidate family and optimize lexicographically for:

1. exact round-trip coverage;
2. minimum number of distinct derived orders K;
3. low HDE cost;
4. HR/reference structure;
5. descriptor overhead.

The generalized 9+9+7 family of 9,072 configurations is the next documented candidate for this test.

See [ORDER_HR_CORPUS_500.md](ORDER_HR_CORPUS_500.md).

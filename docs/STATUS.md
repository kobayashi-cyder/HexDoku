# Project Status

Last updated: 2026-09-24

## Current phase

HexDoku is in the **formalization and reference-test phase**.

The architecture has a defined direction, but performance and scaling claims remain unverified.

## Defined concepts

- HDC-Lite v1 9+9+7 Parity-first mask search (36 masks / 6-bit rank)
- HR branch-reference channel: one implicit anchor plus HR alternative reference slots
- One-board derived-information model: received 25-hole board; coordinates/values/order/HR/slot positions are decoder-derived when reproducible

- Seed Cell as a minimal bootstrap descriptor
- HexDoku ID / serial
- versioned deterministic reconstruction
- content-addressed chunk references
- hash-based integrity verification
- Sudoku Profile v1 as the first reference rule profile
- rollback-first recovery
- regeneration when rollback and source recovery are impossible
- bit-perfect reconstruction as the first acceptance criterion

## Not yet established

The following should be treated as open research questions:

- practical compression advantage
- storage advantage after counting shared dependencies
- bandwidth reduction on real workloads
- reconstruction latency at scale
- useful error-correction properties
- optimal HexDoku board construction
- formal information-theoretic bounds
- distributed AI/model-state benefit
- security against malicious manifests or peers

## Required evidence before stronger claims

A result should include:

1. source corpus
2. exact code version
3. Seed Cell size
4. all external/shared storage bytes
5. bytes transferred
6. reconstruction time
7. hardware/software environment
8. original digest
9. reconstructed digest
10. direct byte comparison

## Near-term milestones

### M0 — Formal schema
Define a canonical Seed Cell and rule-version format.

### M1 — Sudoku Profile v1 reference implementation
Implement one fixed 9×9 Sudoku baseline with 25 unresolved coordinates, deterministic q tables, HR, 24 validity-preserving commits, and ParityGrid verification.

### M1A — Probability trajectory benchmark
Generate a corpus of Sudoku Profile v1 boards and measure q-value histograms, entropy, repeated values, turn-to-turn reuse, HCT size, and compression of the raw 2,925-byte trajectory.

### M1B — Payload profile design gate
Do not freeze a payload-specific terminal/permutation rule until the Sudoku v1 baseline is measured. T76 is not counted as 76 free payload bits in sudoku-v1.

### M1C — HDC-Lite 36-mask benchmark
From completed Sudoku ParityGrids, enumerate the 36 fixed `9+9+7` masks, replay HDE exactly, reject non-round-tripping masks, select the canonical best mask, and measure HDC search/HDE decode time plus q-trajectory compression.

### M1D — Minimum HDE packet benchmark
Compare the one-board packet modes: 324-bit full Parity, 243-bit masked board, ~73-bit arbitrary-Sudoku rank reference, 41-bit canonical-transform Seed, and optional 46-bit coordinate-bearing Seed. Measure HDE code size, working memory, and latency in addition to packet bits.

### M1E — HR branch-reference benchmark
Measure `sum_hr_targets`, `sum_hr_commits`, and `sum_hr_dna` on the 25-hole corpus; record HR histograms, deduplicated reference-slot counts, dictionary overhead, HDE regeneration operations, and the reachable complete-assignment count K where feasible. Report `log2(K)` separately from raw slot width.

### M1F — Reachable-order and instruction benchmark
Use the received 25-hole board as the only board input. Measure the number K of distinct valid deterministic solve orders HDC can deliberately realize, report `log2(K)`, and instrument HDE candidate-cell evaluations plus actual CPU instructions/cycles. Compare against a conventional 84-bit factoradic order field.

### M2 — Bit-perfect cross-process reconstruction
Prove exact reconstruction in a fresh process.

### M3 — Partial-cache transfer test
Measure bytes transferred at different cache hit rates.

### M4 — Corruption and rollback test
Inject corruption and verify rollback behavior.

### M5 — Cross-implementation test
Reproduce identical bytes using two independent implementations.

### M6 — Comparative benchmark
Compare against simple baselines such as full transfer, ordinary content-addressed deduplication, and conventional compression.

## Publication principle

Experimental hypotheses should be easy to distinguish from measured results.

The project should prefer a small falsifiable claim over a broad unverifiable one.

# HexDoku

**HexDoku** is an experimental architecture for **deterministic reconstruction, compact state description, integrity verification, and parity-style layout** using a solved-Sudoku-inspired structure.

> 発想の起点は「**エピゲノムの逆って、数独ではないか？**」という直感だった。

This is a conceptual analogy, **not** a claim that Sudoku is a biological or mathematical inverse of the epigenome.

The intuition is the contrast between:

- a system in which state/annotations influence what is expressed from an underlying information space, and
- a constraint system in which a relatively small set of conditions can determine a much larger global configuration.

HexDoku explores whether that second direction can be useful as an engineering primitive for reconstruction and synchronization.

---

## Status

**Experimental / research prototype.**

The repository is being opened early so the model, protocol, assumptions, and evaluation criteria can be inspected independently.

Claims such as compression ratio, reconstruction speed, fault tolerance, and scaling behavior are **not considered established until measured**.

### Documentation

- [Origin of the idea](docs/ORIGIN.md)
- [What HexDoku can do](docs/CAPABILITIES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [DNA / Parity Model v0.2](docs/DNA_PARITY_SPEC.md)
- [Sudoku Profile v1](docs/SUDOKU_PROFILE_V1.md)
- [HDC-Lite v1](docs/HDC_LITE_V1.md)
- [HDE Minimum Packet](docs/HDE_MIN_PACKET.md)
- [One-Board Derived Information Model](docs/ONE_BOARD_DERIVED_INFORMATION.md)
- [Order-Bearing Sudoku Profile v0](docs/ORDER_BEARING_PROFILE_V0.md)
- [500-board Order / HR Corpus Benchmark](docs/ORDER_HR_CORPUS_500.md)
- [Permutation / Address Compression](docs/PERMUTATION_ADDRESSING.md)
- [Canonical order and HexDoku Hamming Rank](docs/CANONICAL_ORDER.md)
- [HR Branch Reference Channel](docs/HR_BRANCH_REFERENCES.md)
- [Turn trajectory and optional Hamming addressing](docs/TRAJECTORY.md)
- [Protocol draft](docs/PROTOCOL.md)
- [Project status and milestones](docs/STATUS.md)
- [Contributing](CONTRIBUTING.md)

---

## What can HexDoku do?

In practical terms, HexDoku aims to let compatible systems **reproduce a large shared state while exchanging only the new information needed to identify or complete that state**.

Potential uses include:

- sparse state synchronization
- content-addressed caches
- deterministic checkpoints
- distributed agent/model state
- partial transfers between nodes
- rollback and regeneration
- hierarchical Seed Cells

The strongest gains are expected when the sender and receiver already share most of the underlying data or deterministic rules.

A proposed communication mode lets the bus exchange only **Seed Cells, HexDoku identifiers, hashes, references, and residual bits**. Intermediate relays therefore do not need to understand the reconstructed application payload. If a unique HexDoku solution maps to one canonical bit ordering, the receiver can reconstruct and identify the exact bit string.

HexDoku also investigates an asymmetric codec model: an expensive **compressor** discovers a compact Seed Cell / arithmetic / shared-state description, while a separate deterministic **expander** recreates the original bytes. On workloads with large shared or mathematically derivable state, this compact description may be far smaller than a conventional self-contained ZIP stream. This is a research hypothesis and must be benchmarked with all decoder-side shared data counted.

See [What HexDoku can do](docs/CAPABILITIES.md) for the full explanation.

---

## HDC / HDE

HexDoku defines two primary codec components:

- **HDC — HexDoku Compressor**  
  Converts source data into a compact HexDoku representation such as a Seed Cell, rule references, hashes, shared-state references, arithmetic reconstruction rules, and residual bits.

- **HDE — HexDoku Expander**  
  Takes the compact HexDoku representation and deterministically reconstructs the canonical original bit string.

```text
source bytes
   |
   v
  HDC
   |
   v
Seed Cell + references + residual bits
   |
   v
  HDE
   |
   v
canonical reconstructed bytes
```

HDC may be computationally expensive in general. The first Sudoku baseline instead uses **HDC-Lite v1**, which restricts encoder search to 36 canonical `9+9+7` hole masks. HDE is deterministic and does not repeat that mask search.

## First reference rule: Sudoku Profile v1

The first runnable HexDoku baseline is intentionally ordinary Sudoku.

~~~text
HexDoku Core
├─ Sudoku Profile v1   <- baseline now
└─ Payload Profile vN  <- later
~~~

Sudoku Profile v1 fixes 9×9 geometry, digits 1..9, row/column/3×3 constraints, the 25 unresolved coordinates, deterministic integer q-distributions, and a validity-preserving commit resolver.

This gives a clean baseline for measuring the 2,925-byte raw DNA trajectory, HCT compression, repeated q values, and HDC/HDE equality before payload-specific rules are introduced.

See [Sudoku Profile v1](docs/SUDOKU_PROFILE_V1.md).

---
## HDC-Lite v1: Parity-first hole search

The first encoder strategy starts from the completed Sudoku ParityGrid and searches only a tiny family of reconstruction-friendly 25-hole masks.

Baseline removal rule:

~~~text
remove all nine 1s
remove all nine 2s
remove seven of the nine 3s
= 25 holes
~~~

Only the two visible 3-cells vary, so there are exactly:

~~~text
C(9,2) = 36 candidate masks
~~~

HDC runs the exact Sudoku-v1 HDE procedure on each candidate and keeps only masks that reconstruct the source ParityGrid exactly. A canonical six-bit rank identifies the chosen mask (`0..35`; `36..63` invalid).

This makes the first HDC a small mask-search encoder rather than a broad combinatorial compressor. HDE never repeats the 36-mask search.

See [HDC-Lite v1](docs/HDC_LITE_V1.md).

---
## One-board received-board model

The current reference input is **one 9×9 Sudoku board containing exactly 25 holes**.

HDE does not receive separate coordinate, solution-value, order, HR, or branch-slot-position metadata when those values are reproducible from the board.

~~~text
received 25-hole board
   |
   +-> 25 hole coordinates        : +0 transmitted bits
   +-> solved values              : +0 transmitted bits
   +-> deterministic solve order  : +0 transmitted bits
   +-> HR trajectory              : +0 transmitted bits
   +-> branch-reference positions : +0 transmitted bits
~~~

A standalone cell address among 81 positions needs 7 fixed bits; `3 bit × 3 bit` is not sufficient for a 9×9 coordinate because three bits encode only eight values per axis. In the received-board model this does not matter: positions are implicit in the 81-cell array.

Simple board widths:

| Board profile | Simple fixed-width representation |
|---|---:|
| Generic `HOLE + 1..9` | 324 bit (`81 × 4`) |
| Fixed `9+9+7`: `HOLE,3..9` | 243 bit (`81 × 3`) |

The 243-bit figure applies **only** to the fixed `9+9+7` profile.

For 25 distinct holes, the absolute arbitrary-order space is `25!`, or `log2(25!) ≈ 83.6815` bits. HexDoku omits a separate 84-bit order field only to the extent that HDC/HDE can actually realize and reproduce those orders. If only K orders are reachable, the real order-channel capacity is `log2(K)`.

Against a hypothetical `board + standalone order` baseline, the maximum order-field omission is about **25.62%** for the 243-bit board and **20.53%** for the 324-bit board. If K=1, the order-derived saving is 0%.

See [One-Board Derived Information Model](docs/ONE_BOARD_DERIVED_INFORMATION.md).

### Fixed order vs information-bearing order

The baseline `sudoku-v1` still keeps `E0..E24` fixed in row-major order. Therefore its independent order-channel capacity is **0 bits** even though the fixed order itself needs no transmission.

To test order as a derived information channel, the separate experimental `sudoku-order-bearing-mrv-v0` profile dynamically chooses the next coordinate by minimum candidate count (minimum HR), then row-major tie-break.

For one fixed ParityGrid and the current 36-mask `9+9+7` family, the hard upper bound is only `K <= 36`, or at most **5.17 bits** of order capacity. The current single-Parity reference sample accepted 27 masks with 27 distinct orders: `K=27`, `log2(K)≈4.755 bits`.

The often-mentioned `log2(25!)≈83.68 bits` remains only the absolute ceiling for an unrestricted 25-element permutation family; it is not a measured capacity of the current 36-mask profile.
A 500-completed-board corpus benchmark now gives a stronger result for the fixed 36-mask family:

~~~text
500 completed boards
18,000 mask evaluations
3,780 exact-round-trip masks (21.0%)
367 boards with >=1 valid mask (73.4%)
133 boards with NO_MASK (26.6%)
K mean over all boards = 7.56
K max = 30
mean log2(K), successful boards = 2.928 bits
guaranteed order capacity over this corpus = 0 bits
~~~

The zero guarantee is important: the fixed family still has `NO_MASK` boards and some successful boards have `K=1`. The next HDC step must improve **minimum coverage and minimum K**, not merely average K.

Across accepted masks, target-only `sum(HR)` averaged 2.222 alternative-reference slots; full-DNA `sum(HR)` averaged 357.613 structural slots. These are slot counts, not independent payload bits.

See [500-board Order / HR Corpus Benchmark](docs/ORDER_HR_CORPUS_500.md).


---
## DNA / Parity trajectory

For the current 25-unresolved-coordinate profile, HexDoku defines **25 canonical evaluation tables but only 24 normal commits**.

~~~text
P0  -> 25 unresolved coordinates
P1  -> 24
...
P23 -> 2
P24 -> 1 Terminal Reference coordinate
~~~

The initial 25 unresolved coordinates are fixed once in row-major order (top-to-bottom, left-to-right). HR and probability values never choose the next coordinate.

The tables contain:

~~~text
25 + 24 + ... + 1 = 325 evaluated coordinate states
~~~

With nine 8-bit candidate values per coordinate, the raw q-only DNA trajectory is:

~~~text
325 × 9 × 8 = 23,400 bits = 2,925 bytes
~~~

The HexDoku Core can support non-Sudoku profiles, but the **first reference implementation is Sudoku Profile v1**: standard row, column, and 3×3 box constraints are used for candidate generation and baseline reconstruction.

The final coordinate remains part of the 25th evaluation table. In Sudoku Profile v1, its 72-bit q vector is **derived from Sudoku state**, not free payload. The structural 4-bit terminal extension is reserved as `0000`. A future Payload Profile may redefine terminal payload/selector behavior without changing the Sudoku baseline.

The 25-table evaluation trajectory is **DNA**. The completed 81-cell reference table is **Parity**.

See [DNA / Parity Model v0.2](docs/DNA_PARITY_SPEC.md).

---

## HR branch-reference channel

HexDoku HR can also be interpreted as the number of **alternative candidate branches beyond one canonical anchor**.

~~~text
HR = candidate_count - 1
alternative reference slots = HR
~~~

Thus HR0 has no extra branch reference, HR1 has one, HR2 has two, and HR8 has eight.

A branch slot may carry or derive a content hash, chunk/object reference, manifest index, or another stable shared-state reference. The hash/reference identifies shared or retrievable state; it does not recreate unknown content.

For the full 25-stage DNA trajectory:

~~~text
B_DNA = sum HR(t,c) over all 325 evaluated coordinate states
~~~

The generic structural maximum is `325 × 8 = 2,600` alternative-reference slots. In the fixed `9+9+7` case, when active candidates are restricted to `{1,2,3}`, `HR <= 2`, giving a structural bound of at most `650` slots.

These are slot counts, **not proven independent payload capacity**. Real capacity is bounded by `log2(K)`, where K is the number of complete branch/reference assignments that HDC can actually choose while preserving deterministic reconstruction and exact Parity.

See [HR Branch Reference Channel](docs/HR_BRANCH_REFERENCES.md).

---
## T76 research container

For the 25th evaluation table, the current 8-bit-q profile defines:

~~~text
q1..q9 in fixed candidate order = 9 × 8 = 72 bits
Terminal Extension              = 4 bits
------------------------------------------------
T76                             = 76 bits
~~~

T76 is a **76-bit structural container** in the general research model. Under Sudoku Profile v1 it is not a 76-bit free selector: Q72 is derived and the four-bit extension is reserved.

Its nominal selector space is:

~~~text
2^76 = 75,557,863,725,914,323,419,136 states
~~~

A future Payload Profile may define a T76-based selector family of up to 2^76 states. That capacity is **not claimed by Sudoku Profile v1**, because its q bits are constrained by Sudoku evaluation. Any payload-selector profile must be separately versioned and benchmarked.

A canonical 13-symbol text form may use the Base64url alphabet as a **radix-64 integer alphabet**, with the first symbol restricted to 16 values. This is not standard byte-oriented Base64url encoding. Standard Base64url of a 10-byte container would require 14 unpadded characters.

See [Permutation / Address Compression](docs/PERMUTATION_ADDRESSING.md).

---

## T76 compression accounting (future Payload Profile)

A future Payload Profile with a genuinely free T76 field could identify one order from a versioned family containing at most 2^76 orders. **Sudoku Profile v1 does not provide this free 76-bit selector.**

For **25 distinct elements**, the complete arbitrary permutation space is larger:

~~~text
log2(25!) ≈ 83.68 bits
fixed-width rank for every 25! order = 84 bits
~~~

Therefore T76 does **not** encode every possible 25-element permutation. It encodes a restricted/shared family of at most 2^76 permutations.

When comparing against a naive explicit list of 25 IDs, the reduction can be substantial:

| Baseline representation | Baseline bits | T76 bits | Incremental reduction |
|---|---:|---:|---:|
| 25 × 5-bit local IDs | 125 | 76 | 39.20% |
| 25 × 32-bit IDs | 800 | 76 | 90.50% |
| 25 × 64-bit IDs | 1,600 | 76 | 95.25% |
| 25 × 256-bit hashes | 6,400 | 76 | 98.81% |

These percentages are conditional design examples for that future payload profile. They are valid only when the element set, rule version, and other required context are already shared or accounted separately; they are not Sudoku-v1 benchmark results.

For the selected family itself, 76 bits is already the information-theoretic minimum needed to distinguish all 2^76 selector states. HexDoku's gain is therefore mainly the replacement of a verbose explicit ordering/address list with a shared deterministic selector.

The complete transmitted size is:

~~~text
T76
+ any Seed bytes not already shared
+ rule/profile identifiers
+ universe/manifest reference
+ residual ordering data
+ verification/authentication fields
~~~

Benchmarks must report both the 76-bit incremental-selector case and the complete descriptor size.

---
## Permutation / address compression

A central HexDoku use case is to compress the **ordering/address description** of blocks that are already shared, content-addressable, or retrievable by hash/ID.

~~~text
shared block set
      |
      v
hash / object IDs
      |
      v
HexDoku DNA + Parity
      |
      v
canonical ID permutation
      |
      v
ordered bit stream
~~~

Instead of transmitting a long explicit ID sequence, HDC may describe the ordering with a HexDoku ID, Seed/rules, and only the residual ordering information that HDE cannot regenerate.

This does **not** make unknown block contents disappear. HexDoku first targets the permutation/address information; conventional compression may separately compress the block contents.

For 81 distinct blocks, a completely arbitrary permutation has `81!` possibilities and therefore requires about `log2(81!) = 401.17` bits of distinguishing information. HexDoku only reduces this explicit cost when shared state, deterministic rules, restricted permutation families, nonuniform distributions, previous state, or residual coding provide structure.

See [Permutation / Address Compression](docs/PERMUTATION_ADDRESSING.md).

---

## Core idea

HexDoku separates the system into a very small **Seed Cell** and a deterministic reconstruction path.

```text
Seed Cell
   |
   v
HexDoku ID / serial
   |
   v
Rule set + version
   |
   v
Deterministic expansion
   |
   +----> exact chunk references / hashes
   |
   v
Reconstructed state
```

Instead of assuming that a hash can reconstruct arbitrary missing information, HexDoku uses hashes as **identifiers and integrity checks** for data that is already reproducible, locally available, or retrievable from a shared store.

A hash is therefore a key/check, not a magic decompressor.

---

## Seed Cell

A Seed Cell is intended to be a minimal bootstrap description.

A practical Seed Cell may contain:

- HexDoku ID or serial number
- schema / rule-set version
- deterministic-generation parameters
- chunk identifiers
- chunk hashes
- root hash or manifest hash
- optional rollback reference

The design goal is that two compatible nodes given the same Seed Cell and the same referenced rule/data universe arrive at the **same bit-level result**.

---

## DNA / Parity topology

HexDoku Core uses a 9×9 board as a deterministic coordinate topology. **Sudoku Profile v1**, the first reference profile, additionally requires standard Sudoku constraints. Future profiles may replace those constraints without changing the Core. The fully materialized 81-cell final table is called **Parity**, while the 25-stage evaluation-table trajectory is called **DNA**.

Possible roles include:

- parity placement
- deterministic routing
- connection topology
- reconstruction coefficients
- chunk-to-cell assignment
- redundancy layout
- ordering / addressing

The final Parity is therefore treated as a **layout, reconstruction, and ordering/address map**.

It is not assumed, by itself, to be an error-correcting code. Any error-correction capability must be defined and measured explicitly.

---

## Deterministic reconstruction

A HexDoku implementation should make reconstruction reproducible.

Given the same:

1. Seed Cell
2. HexDoku rule version
3. referenced chunks or deterministic generators
4. canonical ordering
5. hash algorithm

the output should be identical.

Target invariant:

```text
reconstruct(seed, rules, data_universe) -> identical bytes
```

This makes bit-for-bit verification possible.

---

## Communication model

Nodes do not need to exchange the entire reconstructed object when both sides already share most of the underlying universe.

A compact exchange can be:

```text
HexDoku serial
+ rule version
+ root/manifest hash
+ required chunk hashes
```

The receiver then:

1. resolves the HexDoku serial,
2. loads the exact rule version,
3. checks which chunks already exist locally,
4. requests only missing chunks,
5. verifies each chunk by hash,
6. deterministically reconstructs the state,
7. verifies the final root hash.

This makes HexDoku closer to a **content-addressed deterministic reconstruction protocol** than to conventional lossless compression.

---

## Recovery policy

HexDoku intentionally distinguishes verification from recovery.

Current recovery principle:

- If a known-good state exists, **rollback**.
- Reconstruct from the last verified state.
- If rollback is impossible and the required source information is unavailable, treat the state as effectively lost.
- In that case, **regenerate** rather than pretending that hashes alone can restore unknown bytes.

This is a deliberate constraint.

---

## Why “HexDoku”?

The project combines several ideas:

- Sudoku-like global constraint structure
- compact identifiers / serials
- hash- and hex-oriented content addressing
- deterministic reconstruction
- parity-like placement

The exact encoding format is still subject to change.

---

## What HexDoku is not

HexDoku is **not** currently claimed to be:

- a proven replacement for standard compression
- a cryptographic primitive
- an error-correcting code by definition
- a method for recovering arbitrary data from only a hash
- a biological model of epigenetics
- a proven distributed-AI architecture

Those are separate questions that require experiments.

---

## Evaluation plan

The first useful implementation should be small enough to verify completely.

Primary measurements:

| Metric | Question |
|---|---|
| Bit-perfect reconstruction | Does the receiver reproduce exactly the same bytes? |
| Seed size | How small is the bootstrap description? |
| Total stored bytes | Is total storage actually reduced after all dependencies are counted? |
| Transfer bytes | How much data must cross the network? |
| Reconstruction latency | How long does expansion take? |
| Missing-chunk rate | How often must external data be fetched? |
| Verification cost | What is the cost of hashing / validation? |
| Rollback success | Can a corrupted state return to a known-good state? |
| Regeneration cost | What happens when rollback is unavailable? |

A result is only useful if **all dependencies and shared stores are counted**.

---

## Minimal experiment

A first reference test can use:

1. a fixed binary corpus,
2. deterministic chunking,
3. a fixed 9×9 HexDoku coordinate board,
4. a canonical cell/chunk mapping,
5. SHA-256 chunk hashes,
6. a Seed Cell manifest,
7. reconstruction on a second process or machine,
8. final byte-for-byte comparison.

Success criterion:

```text
SHA256(original) == SHA256(reconstructed)
AND
original bytes == reconstructed bytes
```

After correctness is established, measure storage, transfer, and latency.

---

## Repository direction

Planned areas:

```text
/
├─ README.md
├─ CONTRIBUTING.md
├─ docs/
│  ├─ ORIGIN.md
│  ├─ ARCHITECTURE.md
│  ├─ PROTOCOL.md
│  └─ STATUS.md
├─ reference/
│  ├─ seed/
│  ├─ sudoku/
│  └─ reconstruction/
└─ tests/
```

The reference implementation should remain deliberately small until deterministic equivalence is demonstrated.

---

## Design principles

1. **Determinism before scale**
2. **Bit equality before benchmark claims**
3. **Hashes identify and verify; they do not recreate unknown information**
4. **Count all external/shared storage**
5. **Version every reconstruction rule**
6. **Rollback only to verified state**
7. **Regenerate when recovery information no longer exists**
8. **Keep experimental claims falsifiable**

---

## Relationship to AI / distributed systems

HexDoku may eventually be tested as a building block for:

- distributed model state
- shared caches
- content-addressed artifacts
- reproducible agent state
- sparse synchronization
- checkpoint reconstruction

However, there is currently no claim that major AI labs use this exact **Seed Cell + HexDoku** architecture.

The useful question is empirical: whether HexDoku can reduce transfer or duplicated storage **without losing exact reproducibility**.

---

## Contributing

The most valuable contributions are currently:

- formalization of the encoding
- deterministic reference implementations
- adversarial tests
- storage-accounting tests
- corruption / rollback tests
- comparisons with existing content-addressed and erasure-coding systems
- reproducible benchmarks

See `CONTRIBUTING.md`.

---

## License

No open-source license has been selected yet.

Until a license is added, publication of the source repository does **not** automatically grant broad reuse rights.

---

## Short definition

> **HexDoku is an experimental deterministic reconstruction architecture in which a small Seed Cell selects a versioned Sudoku-inspired layout and content-addressed data, allowing compatible nodes to reproduce and verify the same larger state while transferring only what is missing.**

---

## DNADoku extension: genome reconstruction / reference-compression profile

**DNADoku** is an experimental HexDoku extension that treats DNA-like symbols as a compact representation layer for **selectors, permutation ranks, reconstruction rules, and references**.

It must not be interpreted as a claim that arbitrary biological DNA can be losslessly compressed to a tiny seed without shared information. DNADoku is most useful when a receiver already has a versioned reference genome, pangenome, block dictionary, or other shared reconstruction universe.

### Radix-4 / codon mapping

Using the four DNA symbols `A/C/G/T` as a radix-4 alphabet gives:

~~~text
1 base   = 2 bits
3 bases  = 1 codon = 6 bits
13 codons = 39 bases = 78 bits
14 codons = 42 bases = 84 bits
~~~

This aligns naturally with the existing HexDoku selector work:

- a 76-bit T76-style selector fits inside a 13-codon / 78-bit container,
- an unrestricted permutation of 25 distinct elements needs `log2(25!) ≈ 83.6815` bits,
- therefore every one of the `25!` permutations needs an 84-bit fixed-width rank, which fits in 14 codons.

The unused rank values in the 84-bit space must be treated as invalid or reserved; 84 bits are a container width, not a claim that all `2^84` states correspond to valid 25-element permutations.

### Genome-compression role

DNADoku is not intended to replace sequence compressors by itself. Its intended role is the **reconstruction-description layer** around conventional sequence compression and shared-reference coding.

~~~text
individual genome
      |
      v
reference / pangenome matching
      |
      +--> shared blocks / haplotypes / known variants
      |
      +--> novel or residual sequence
      |
      v
DNADoku selector / ordering / dependency description
      |
      v
residual integer coding + entropy coding
      |
      v
compact reconstruction descriptor
~~~

For an idealized A/C/G/T-only sequence, direct two-bit packing already costs 2 bits per base. A roughly 3.1-billion-base haploid reference therefore has a simple lower representation scale of about 6.2 billion bits, or about 775 MB, before metadata, ambiguity symbols, indexing, ploidy, and other biological details are accounted for.

DNADoku does not make those unknown sequence bits disappear.

Its potential advantage appears when much of the genome is already present in a **shared, versioned universe**. In that case the transmitted or per-sample object may contain primarily:

- reference / pangenome version,
- selected shared blocks or haplotypes,
- permutation / placement information,
- known-variant selectors,
- structural-variant description,
- genuinely novel residual sequence,
- verification hashes and integrity metadata.

In that model, the per-individual descriptor can be far smaller than a self-contained whole-genome file, but the shared reference, dictionary, and decoder are dependencies and must be counted separately in storage accounting.

### Proposed profiles

| Profile | Shared context | DNADoku role | Claim status |
|---|---|---|---|
| DNADoku-13 | versioned selector family | 78-bit container for up to 76 selector bits | structural definition |
| DNADoku-14 | fixed 25-element universe | 84-bit full permutation-rank container | mathematically sufficient for `25!` |
| Genome-Reference Profile | reference genome shared | ordering / block / residual reconstruction description | experimental |
| Genome-Pangenome Profile | pangenome + block/variant dictionary shared | compact haplotype/block selection and rearrangement description | experimental |
| Population-Dictionary Profile | large shared cohort dictionary | per-sample residual / selector description | research target |

No size target for the genome profiles is considered established until an implementation performs exact round-trip reconstruction and reports:

~~~text
original genome bytes
shared reference bytes
shared dictionary bytes
per-sample descriptor bytes
residual sequence bytes
index / metadata bytes
decoder / rule version
reconstruction latency
final byte-for-byte equality
~~~

### Accounting rule

A DNADoku genome result must distinguish at least two measurements:

1. **Incremental per-sample size** — bytes unique to one genome when all shared state already exists.
2. **Amortized / self-contained size** — per-sample size after the required share of references, dictionaries, indexes, and rule data is included.

Reporting only the first number as "genome compression size" is not sufficient.

### Design objective

The long-term objective is therefore not:

> reconstruct an arbitrary human genome from a hash or tiny seed alone.

The objective is:

> **given the same versioned reference universe, encode the identity, arrangement, known differences, and irreducible novel sequence of an individual genome with the smallest deterministic reconstruction descriptor that still reproduces the exact canonical sequence.**

In this role, DNADoku is best understood as a **genome reconstruction seed language layered on top of shared-reference and entropy-compression systems**, rather than as a standalone biological compression algorithm.

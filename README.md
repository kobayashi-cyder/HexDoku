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

---

---

## DNADoku epigenome extension: methylation-state decomposition

The genome and the epigenome should be represented as different layers.

~~~text
Genome      = reference sequence / structural identity
Epigenome   = state overlay on that sequence
DNADoku     = compact description of overlay state and exceptions
HexDoku     = deterministic reconstruction / verification framework
~~~

For DNA methylation, the principal engineering target is not to re-encode the underlying genome repeatedly. The target is to encode **which genomic sites or regions carry which methylation state under a specified biological and measurement context**.

In human methylome work, CpG sites are the main methylation context, although WGBS pipelines can also report CHG and CHH methylation. A representative human genome contains on the order of tens of millions of CpG positions (commonly described as roughly 28 million, depending on assembly and counting convention). Therefore a purely idealized one-bit state vector over 28 million predefined CpG loci would require about:

~~~text
28,000,000 × 1 bit
= 28,000,000 bits
≈ 3.5 MB
~~~

This is only a structural lower-level baseline. Real methylation datasets also need locus identity or an agreed coordinate universe, missing/unknown states, measurement confidence, coverage, strand/genotype context where relevant, and often a **fractional methylation value** rather than a single binary state.

For bulk sequencing, a value such as `0.82` usually represents the observed fraction of molecules/read evidence methylated at that locus, not an intrinsic eight-tenths methylation of one DNA molecule. Therefore DNADoku profiles must distinguish at least:

- single-molecule / single-cell discrete state,
- aggregated fractional methylation,
- unknown or insufficient-coverage state,
- optional non-CpG methylation contexts.

### Reference-overlay decomposition

The proposed decomposition is:

~~~text
Genome reference
      |
      v
CpG / methylation-coordinate universe
      |
      v
tissue / cell-type / developmental reference methylome
      |
      v
regional methylation-pattern dictionary
      |
      v
DNADoku region selectors / state transitions
      |
      v
DMR and exceptional-site residuals
      |
      v
exact reconstructed methylation state
~~~

Rather than transmitting an independent value for every locus when large regions follow already shared patterns, a DNADoku methylome descriptor can encode the **reference pattern plus deviations**.

A conceptual reconstruction equation is:

~~~text
Methylome
  = Reference(cell/tissue/context)
  + DNADoku(regional-state selectors)
  + DMR residuals
  + site-level residuals
  + measurement metadata
~~~

and a larger cellular state descriptor becomes:

~~~text
Cell State
  = Genome Seed
  + Genome Residual
  + Epigenome Seed
  + Epigenome Residual
~~~

### 25-locus / 25-region blocks

DNADoku may group loci or, preferably, already-coherent genomic regions into 25-element blocks.

A naive 25-CpG binary block has `2^25` possible methylation patterns and therefore requires 25 bits when no structure is known.

A shared pattern dictionary can instead map frequently recurring patterns to compact IDs:

~~~text
25-site block
      |
      +--> shared canonical pattern ID
      +--> optional DNADoku arrangement / region selector
      +--> exceptional loci
      +--> residual quantitative values
~~~

DNADoku-14 must **not** automatically be attached to every 25-locus block. An 84-bit permutation field would be larger than the naive 25-bit binary state and would make compression worse when genomic order is already known.

Therefore the canonical rule is:

- genomic coordinate order is implicit and costs zero extra ordering bits when shared,
- DNADoku permutation/routing fields are emitted only when they describe information not already implied by the coordinate universe,
- common methylation patterns use compact dictionary selectors,
- unusual or quantitative state is left to residual coding.

### DMR-first representation

Differentially methylated regions (DMRs) are a natural higher-level unit because methylation differences often occur regionally rather than as completely independent random bits.

A practical hierarchy is therefore:

~~~text
chromosome
  -> methylation domain
     -> DMR / regulatory region
        -> DNADoku state selector
           -> exceptional CpG residual
~~~

Possible region states may include, for a versioned profile:

~~~text
reference
hypomethylated
hypermethylated
mixed / partially methylated
unknown
quantitative residual follows
~~~

The exact state alphabet must be profile-specific and must not discard quantitative information required for exact reconstruction.

### State inheritance and transition layer

DNA methylation is also interesting as a state-transition problem.

DNMT1 is primarily associated with maintenance of pre-existing DNA methylation patterns, while DNMT3A and DNMT3B are major de-novo methyltransferases. This motivates an optional DNADoku transition model:

~~~text
previous methylation state
        |
        +--> maintenance rule
        +--> de-novo / erasure / context-dependent transition
        |
        v
next methylation state
        |
        +--> measured residual
        v
verified state
~~~

This is an engineering analogy, not a claim that a real methylome is deterministically derivable from DNA sequence or a small Seed Cell. Actual methylation depends on biological context including cell type, developmental state, chromatin environment, environmental/history effects, stochasticity, and measurement conditions.

Therefore an epigenome Seed can only reconstruct a methylome exactly when the required **reference state, rule version, context, and irreducible residual information** are supplied or shared.

### Compression objective

The useful compression target is not:

> encode every methylated cytosine independently.

It is:

> **factor the methylome into shared biological/reference structure, reusable regional patterns, DNADoku selectors, and the smallest residual needed for exact reconstruction.**

This changes the storage problem from:

~~~text
millions of independent locus records
~~~

toward:

~~~text
reference methylome ID
+ regional pattern IDs
+ DNADoku structural selectors
+ DMR deltas
+ exceptional-site / quantitative residuals
+ measurement metadata
~~~

The degree of compression depends on the actual entropy of the dataset and the amount of genuinely shared context. It must be measured, not assumed.

### Required benchmark accounting

Every DNADoku methylome benchmark should report separately:

| Component | Required measurement |
|---|---|
| Coordinate universe | assembly and methylation contexts |
| Reference methylome | bytes and version |
| Pattern / DMR dictionary | bytes and version |
| DNADoku descriptors | bytes |
| Site-level residuals | bytes |
| Quantitative values | bytes / precision |
| Missingness / coverage metadata | bytes |
| Integrity metadata | bytes |
| Incremental sample size | bytes |
| Amortized shared-state size | bytes per sample |
| Self-contained equivalent | bytes |
| Reconstruction equality | exact match to canonical source representation |

Compression claims are invalid if the reference methylome, pattern dictionary, coordinate universe, or required precision is omitted from accounting.

### Research interpretation

This extension makes the original HexDoku intuition more concrete:

~~~text
DNA sequence
  = relatively stable reference information

Epigenetic methylation
  = context-dependent state overlay

DNADoku
  = compressed / structured overlay descriptor

HexDoku
  = reconstruction, addressing, and verification framework
~~~

The central research question is therefore whether a methylome can be represented efficiently as a **versioned reference overlay plus sparse or structured residual**, and whether DNADoku contributes useful selector / topology / reconstruction semantics beyond ordinary reference and entropy coding.

### Scientific references

- [NHGRI: Methylation](https://www.genome.gov/genetics-glossary/Methylation)
- [ENCODE: Whole-Genome Bisulfite Sequencing data standards](https://www.encodeproject.org/data-standards/wgbs/)
- [Moore et al., DNA Methylation and Its Basic Function](https://pmc.ncbi.nlm.nih.gov/articles/PMC3521964/)
- [Yang et al., DNMT3A in haematological malignancies](https://pmc.ncbi.nlm.nih.gov/articles/PMC5814392/)

---

---

## PeriodicTableDoku extension

**PeriodicTableDoku** treats the periodic table and a versioned chemical knowledge universe as shared reconstruction context.

It is not merely "placing 118 elements into a Sudoku-like board." The intended abstraction is hierarchical:

~~~text
PeriodicTableDoku
├─ ElementDoku
├─ IsotopeDoku
├─ MoleculeDoku
├─ MaterialDoku
└─ ReactionDoku
~~~

The common chemical reconstruction equation is:

~~~text
Chemical Object
  = Shared Chemical Universe
  + Composition
  + Structure / Topology
  + State
  + Residual
~~~

The periodic table itself supplies a canonical elemental namespace. With 118 named elements, an atomic-number identifier needs:

~~~text
log2(118) ≈ 6.883 bits
~~~

so a simple fixed-width element ID needs 7 bits.

If the sender and receiver agree on the periodic-table version and elemental property tables, data such as symbol, group, period, and other reference properties do not need to be repeated with every occurrence of an element.

### ElementDoku

ElementDoku is the lowest chemical selection layer.

For 25 independent ordered element slots:

~~~text
25 × log2(118)
≈ 172.066 bits of ideal identifying information

simple fixed width:
25 × 7 = 175 bits
~~~

If order is irrelevant and only a 25-atom elemental multiset matters, the number of possible compositions is:

~~~text
C(118 + 25 - 1, 25)
= C(142, 25)
~~~

with:

~~~text
log2 C(142,25)
≈ 91.822 bits
~~~

This large difference is not free compression. It comes from changing the represented object from an **ordered sequence** to an **unordered composition**.

If exactly 25 distinct elements are selected from the 118-element universe, selection alone requires:

~~~text
log2 C(118,25)
≈ 84.433 bits
~~~

and ordering those selected 25 elements arbitrarily requires:

~~~text
log2(25!)
≈ 83.682 bits
~~~

Together this gives roughly:

~~~text
84.433 + 83.682
≈ 168.114 bits
~~~

which approaches the information needed for 25 ordered draws without replacement.

This illustrates a core HexDoku rule: splitting information into **selection + arrangement** changes representation, but does not bypass the information-theoretic requirement to distinguish all valid states.

### IsotopeDoku

An element ID does not uniquely identify an isotope or ion.

A more specific atomic state may require:

~~~text
Atomic State
  = atomic number Z
  + isotope / mass-number information
  + charge
  + optional electronic-state information
~~~

The exact representation should be profile-specific. Common or naturally abundant isotopes may be compact dictionary states, while rare isotope, charge, or excitation information becomes an explicit residual.

### MoleculeDoku

Molecular composition is not enough to identify molecular structure.

For example, the same elemental formula can correspond to multiple constitutional isomers, stereoisomers, charge states, or conformations. Therefore MoleculeDoku must distinguish at least:

~~~text
Molecule
  = Composition
  + Bond Graph
  + Bond Order / Charge
  + Stereochemistry where required
  + Geometry / Conformation where required
  + Residual
~~~

A conceptual pipeline is:

~~~text
Periodic Table ID
      |
      v
atom / fragment selection
      |
      v
bond topology
      |
      v
bond order / formal charge
      |
      v
stereochemical state
      |
      v
geometry / conformation residual
~~~

Repeated chemical motifs can be moved into a shared fragment dictionary:

~~~text
fragment #17 = reusable ring motif
fragment #52 = reusable functional group
fragment #81 = reusable ligand / side-group motif
~~~

Then a molecule can be represented as:

~~~text
Molecule Seed
  + fragment IDs
  + attachment points
  + bond rules
  + unmatched atoms / bonds
  + residual
~~~

The gain comes only when those fragments and rules are genuinely shared or amortized across many objects.

### MaterialDoku

MaterialDoku extends the same idea from molecules to extended solids and materials.

A general material descriptor may contain:

~~~text
Material
  = Composition
  + Unit Cell / Lattice
  + Symmetry
  + Atomic Positions
  + Occupancy
  + Defects
  + State / Phase
  + Residual
~~~

For a highly regular crystal, repeated atom positions can often be regenerated from a smaller asymmetric description plus symmetry operations. Therefore a useful decomposition is:

~~~text
Ideal / reference crystal
        +
MaterialDoku structural selector
        +
defect overlay
        +
residual
~~~

Defect overlays may describe:

~~~text
vacancy
substitution
interstitial
dopant
site occupancy change
local distortion
~~~

This mirrors the DNADoku pattern of:

~~~text
shared reference
+ structured overlay
+ exceptional residual
~~~

### ReactionDoku

ReactionDoku describes a chemical transformation as a state transition rather than as two unrelated complete objects.

~~~text
Reactant State
      |
      v
Reaction Transition
      |
      v
Product State
~~~

A compact structural description may contain:

~~~text
initial molecular graph
+ atom mapping
+ bond deletions
+ bond additions
+ bond-order changes
+ stoichiometry
+ conditions / state identifiers
+ residual
~~~

This is analogous to MovieDoku temporal coding:

~~~text
State(t+1)
  = State(t)
  + Transition
  + Residual
~~~

If a profile aims to reconstruct reaction mechanisms rather than only net reactant/product changes, intermediates, transition-state information, kinetics, and other required data must be represented separately. A net reaction equation does not determine a unique microscopic mechanism.

### 25-element chemical blocks

A 25-element Doku container may represent:

~~~text
25 atoms
25 fragments
25 lattice sites
25 coordination nodes
25 reaction events
25 material regions
~~~

but the same rule used throughout HexDoku applies:

- do not transmit an 84-bit permutation merely because the block contains 25 elements,
- derive canonical ordering from atomic index, graph traversal, lattice coordinates, or another shared convention whenever possible,
- use a Doku rank only when the choice among arrangements is independently informative,
- use compact dictionary states for recurring motifs,
- leave irreducible topology, geometry, and measurement detail to residual coding.

### Periodic-table regularities available to the profile

The periodic table is especially interesting because the reference universe already contains strong recurring structure.

Useful regularities include:

1. **Atomic-number order**  
   Every element has a canonical integer identity `Z`, giving a stable primary order.

2. **Periodicity**  
   Chemical behavior recurs in structured ways across periods and groups rather than behaving as 118 unrelated labels.

3. **Group / valence similarity**  
   Elements within the same group often share related outer-electron patterns and recurring chemical behavior.

4. **Block structure**  
   The s-, p-, d-, and f-block organization provides another compact categorical partition of the element universe.

5. **Local chemical motifs**  
   Molecules repeatedly reuse bond environments, rings, functional groups, coordination motifs, and larger fragments.

6. **Crystallographic repetition**  
   Extended materials can exhibit unit-cell repetition and symmetry, allowing many positions to be generated from a much smaller structural description.

7. **Sparse deviation from a reference**  
   Defects, substitutions, dopants, isotope changes, and reaction edits are frequently describable as local changes relative to a larger unchanged structure.

These regularities are candidates for shared-reference coding. They are not assumptions that every chemical system is predictable from the periodic table alone.

### Proposed PeriodicTableDoku reconstruction hierarchy

~~~text
Periodic Table version
        |
        v
Element / isotope dictionary
        |
        v
Fragment / motif dictionary
        |
        v
Molecule / material reference
        |
        v
PeriodicTableDoku selectors
        |
        v
graph / lattice / reaction topology
        |
        v
state overlays / defects / transitions
        |
        v
irreducible residual
        |
        v
verified chemical object
~~~

A practical long-term family is therefore:

~~~text
HexDoku
├─ DNADoku
│  ├─ GenomeDoku
│  └─ EpigenomeDoku
├─ MediaDoku
│  ├─ ImageDoku
│  ├─ AudioDoku
│  └─ LayoutDoku
├─ MovieDoku
│  ├─ SceneDoku
│  ├─ MotionDoku
│  ├─ TimelineDoku
│  └─ AV-SyncDoku
└─ PeriodicTableDoku
   ├─ ElementDoku
   ├─ IsotopeDoku
   ├─ MoleculeDoku
   ├─ MaterialDoku
   └─ ReactionDoku
~~~

---

---

## MediaDoku / MovieDoku extension

HexDoku can be generalized beyond genome-like data into media reconstruction.

The proposed split is:

~~~text
HexDoku
├─ DNADoku
│  ├─ GenomeDoku
│  └─ EpigenomeDoku
│
├─ MediaDoku
│  ├─ ImageDoku
│  ├─ AudioDoku
│  └─ LayoutDoku
│
└─ MovieDoku
   ├─ SceneDoku
   ├─ MotionDoku
   ├─ TimelineDoku
   └─ AV-SyncDoku
~~~

The common reconstruction equation is:

~~~text
Object
  = Shared Reference
  + Doku Structure
  + Residual
~~~

For temporal media, a second equation becomes important:

~~~text
State(t+1)
  = State(t)
  + Transition(t -> t+1)
  + Residual(t+1)
~~~

This is the central distinction between MediaDoku and MovieDoku.

### MediaDoku

**MediaDoku** is a reconstruction-description layer for static or composite media such as images, audio, text/layout composites, and multimodal assets.

Instead of treating a media object only as an opaque byte stream, MediaDoku may decompose it into reusable structural components such as:

~~~text
background
object
person
face
clothing
text
logo
lighting
camera state
texture
audio source
layout element
~~~

A conceptual representation is:

~~~text
Media Seed
  + shared asset dictionary
  + object / layer selection
  + layout / coordinates
  + transforms
  + ordering / dependencies
  + codec residual
~~~

For example:

~~~text
asset #183 = background
asset #927 = face template
asset #442 = clothing asset

face:
  position = (x, y, w, h)

transform:
  rotation
  scale
  lighting delta

residual:
  unique pixels / coefficients / waveform data
~~~

MediaDoku therefore targets **asset identity, placement, structure, topology, and exceptions** rather than attempting to make irreducible pixel or waveform information disappear.

### ImageDoku

ImageDoku is the spatial specialization of MediaDoku.

A scene may be divided into objects, semantic regions, layers, tiles, latent regions, or other versioned units. A 25-element Doku block could therefore represent:

~~~text
25 objects
25 semantic regions
25 reusable tiles
25 layer nodes
25 latent components
~~~

The 25-element structure does not imply that every image must literally contain 25 visual objects. It is a reconstruction container whose element semantics are profile-defined.

A possible image hierarchy is:

~~~text
Image
  -> scene / canvas
     -> object or region groups
        -> 25-element Doku block
           -> shared asset / pattern selector
           -> transform
           -> residual
~~~

Canonical ordering should be implicit whenever possible. An 84-bit full 25-element permutation rank is useful only when the permutation itself carries information that is not already determined by the scene graph or coordinate system.

Therefore:

- canonical layer / coordinate order: transmit 0 extra ordering bits,
- known reusable layouts: transmit a compact pattern ID,
- exceptional ordering or graph structure: transmit Doku selector / rank,
- irreducible visual difference: transmit residual through an appropriate image codec.

### AudioDoku

Audio can be decomposed similarly:

~~~text
Audio
  = shared source / model
  + timing
  + pitch / spectral state
  + amplitude / envelope
  + effects / spatial state
  + residual waveform or coefficients
~~~

Depending on the profile, shared units may include:

- phonemes or speech units,
- speaker or voice references,
- musical notes,
- instruments,
- repeated motifs,
- sound effects,
- environmental loops,
- spectral templates.

A speech-oriented profile might be described as:

~~~text
speaker reference
+ phoneme / token sequence
+ timing
+ prosody
+ residual audio
~~~

A music-oriented profile might instead use:

~~~text
instrument
+ note / event
+ duration
+ velocity
+ effect state
+ residual
~~~

These are reconstruction models, not a claim that semantic decomposition alone can reproduce arbitrary source audio exactly. Exact reconstruction still requires all irreducible residual information.

### LayoutDoku

LayoutDoku represents spatial relationships that are more naturally described as structure than as pixels:

~~~text
page / canvas
  -> regions
     -> text blocks
     -> images
     -> controls / objects
     -> relative constraints
~~~

Potential fields include:

~~~text
object ID
parent ID
anchor
relative position
z-order
scale
rotation
visibility
style reference
residual
~~~

This may be useful for documents, UI snapshots, slide-like media, game scenes, or other structured visual compositions where many elements already exist in a shared asset universe.

---

## MovieDoku: temporal reconstruction

**MovieDoku** extends MediaDoku over time.

The naive representation of video is a sequence of complete frames:

~~~text
Frame 0
Frame 1
Frame 2
...
Frame N
~~~

MovieDoku instead treats a movie as an evolving state:

~~~text
Initial Scene State
      |
      v
Transition 0
      |
      v
State 1
      |
      v
Transition 1
      |
      v
State 2
      |
     ...
~~~

At a conceptual level:

~~~text
Frame(t+1)
  = Frame(t)
  + motion
  + object-state changes
  + camera changes
  + lighting changes
  + appearance changes
  + residual
~~~

This is intentionally compatible with conventional video coding ideas such as inter-frame prediction and motion compensation, but MovieDoku operates at a potentially higher structural level.

It does **not** replace the need for AV1, HEVC/VVC, neural codecs, or other lower-level codecs where those codecs are efficient. Instead, MovieDoku can sit above them and describe reusable scene state, object identity, topology, and transitions.

### SceneDoku

SceneDoku represents the persistent structure of one scene.

A scene may contain:

~~~text
person
face
mouth
left hand
right hand
foreground object
background
camera
lighting
text / subtitle region
audio source
...
~~~

A 25-node profile could map these elements to a canonical scene graph:

~~~text
O1  = person
O2  = face
O3  = mouth
O4  = left hand
O5  = right hand
...
O25 = background / environment
~~~

The scene itself is reconstructed from a shared asset/model universe plus local parameters and residuals.

### MotionDoku

MotionDoku describes how scene elements change between states.

For example:

~~~text
scene #81

camera:
  pan-right

person #17:
  x += 4
  y += 0

mouth:
  state 3 -> state 4

lighting:
  unchanged

background:
  unchanged
~~~

The intended representation principle is:

> unchanged state should require little or no repeated description.

Therefore MovieDoku should preferentially encode only:

~~~text
motion
state transition
appearance delta
new / removed object
exception
residual
~~~

rather than re-describing the complete frame.

### TimelineDoku

TimelineDoku groups state changes over a longer interval.

At one scale:

~~~text
25 temporal states
  -> one MovieDoku block
~~~

At another scale:

~~~text
25 shots / scenes
  -> one higher-level MovieDoku block
~~~

Thus MovieDoku can be hierarchical:

~~~text
Movie
  -> sequence
     -> scene
        -> shot
           -> temporal block
              -> object state
                 -> codec residual
~~~

The exact hierarchy must be versioned by profile.

### AV-SyncDoku

Movie media often consists of several synchronized timelines:

~~~text
video
audio
speech
music
subtitle
metadata
interaction / event tracks
~~~

AV-SyncDoku can represent their shared temporal anchors and dependencies:

~~~text
time anchor
  ├─ video state transition
  ├─ audio event
  ├─ subtitle event
  └─ metadata / scene event
~~~

When timings are already implied by a shared canonical timeline, those values should not be retransmitted. Only deviations or independently informative timing data should become residuals.

### 25-element rule

The same caution used in DNADoku applies here.

A 25-element Doku block may describe:

~~~text
25 objects
25 regions
25 motion nodes
25 temporal states
25 shots
25 scenes
~~~

but an 84-bit DNADoku-14-style permutation field must not be added automatically.

If a 25-element binary state takes only 25 bits and the canonical order is already shared, adding an 84-bit permutation field would increase size rather than reduce it.

Therefore the default rule across MediaDoku and MovieDoku is:

1. derive canonical order from shared structure when possible,
2. use compact pattern / dictionary IDs for common states,
3. use Doku selectors only for genuine structural choices,
4. encode exceptional values as residuals,
5. pass irreducible media entropy to a lower-level codec.

### Layering with conventional codecs

MediaDoku and MovieDoku are intended to be **structural layers above conventional compression**, not blanket replacements for it.

~~~text
Image:
shared assets / scene graph
        |
        v
MediaDoku / ImageDoku
        |
        v
AVIF / JPEG XL / neural / other residual codec

Video:
shared assets / scene graph / timeline
        |
        v
MovieDoku
        |
        v
AV1 / HEVC / VVC / neural / other residual codec
~~~

The same principle applies to audio:

~~~text
shared semantic / event structure
        |
        v
AudioDoku
        |
        v
Opus / AAC / FLAC / neural / other residual codec
~~~

Lossless reconstruction requires that the residual layer preserve every source distinction not reproduced by the structural layer.

### High-level Movie Seed

A mature MovieDoku descriptor could take the form:

~~~text
Movie Seed
   |
   +--> asset dictionary version
   +--> character / object references
   +--> environment / background references
   +--> scene graph
   +--> MovieDoku temporal rules
   +--> motion / state transitions
   +--> audio / subtitle timeline
   +--> residual codec streams
   +--> integrity hashes
   |
   v
exact or profile-defined reconstructed movie
~~~

This changes the conceptual storage question from:

> how do we compress every frame independently?

toward:

> what exists, how does it change, what is already shared, and what information remains irreducible?

### Compression-accounting rule

Every MediaDoku / MovieDoku benchmark must distinguish:

| Component | Required accounting |
|---|---|
| Shared asset/model dictionary | bytes and version |
| Scene graph / layout | bytes |
| Doku selectors / permutation data | bytes |
| Motion / transition data | bytes |
| Audio / subtitle timing | bytes |
| Lower-level codec residual | bytes |
| Integrity / index metadata | bytes |
| Incremental media object | bytes |
| Amortized shared-state cost | bytes per object |
| Self-contained equivalent | bytes |
| Reconstruction fidelity | exact bytes or declared perceptual metric |

A benchmark is incomplete if it reports only the Seed or structural descriptor while excluding the shared assets or residual codec required for reconstruction.

### Unified HexDoku family

The resulting research family can be summarized as:

~~~text
HexDoku
  = deterministic reconstruction / addressing / verification framework

DNADoku
  = biological-sequence and state-overlay reconstruction descriptor

MediaDoku
  = spatial / multimodal structure reconstruction descriptor

MovieDoku
  = temporal state-transition reconstruction descriptor
~~~

All of them share the same general principle:

~~~text
Reconstructed Object
  = Shared Universe
  + Versioned Doku Description
  + Irreducible Residual
~~~

The useful research question is not whether Doku metadata can replace entropy coding, but whether **shared structure and deterministic reconstruction can remove repeated description before conventional entropy coding is applied**.

---

---

## OncoDoku / EvolutionDoku extension

**OncoDoku** models carcinogenesis and tumor evolution as a layered, evolving state rather than as a single mutation or single cause.

The intended decomposition is:

~~~text
OncoDoku
├─ GermlineDoku
├─ SomaticDoku
├─ EpigenomeDoku
├─ RepairDoku
├─ ExposureDoku
├─ InfectionDoku
├─ ExpressionDoku
├─ MicroenvironmentDoku
├─ ImmuneDoku
├─ CloneDoku
├─ MetastasisDoku
└─ TherapyDoku
~~~

The central idea is that cancer state emerges from interacting inherited predisposition, acquired genomic alterations, epigenetic state, DNA-damage/repair processes, exposure history, infection, expression/signaling, tissue context, immune interaction, clonal competition, and treatment.

A useful state equation is:

~~~text
CancerState(t+1)
  = F(
      U,
      I,
      G(t),
      S(t),
      Δ(t),
      Σ(t),
      R(t)
    )
~~~

where:

~~~text
U = shared biological reference universe
I = selected inherited / acquired factors and identities
G = genome, clone, cell-cell, and tissue graph structure
S = current molecular / epigenetic / immune / metabolic state
Δ = mutations, edits, state changes, treatment effects, and other transitions
Σ = selection pressure acting on competing states / clones
R = irreducible or currently unexplained residual
~~~

### GermlineDoku

GermlineDoku represents inherited predisposition relative to a reference genome or pangenome.

~~~text
reference genome
+ inherited variants
+ pathogenicity / evidence annotations
+ residual
~~~

Inherited predisposition is not equivalent to a cancer diagnosis. It changes the prior risk landscape and the set of possible future trajectories.

### SomaticDoku

SomaticDoku represents acquired genomic change:

~~~text
SNV
indel
copy-number change
deletion
amplification
chromosomal rearrangement
regulatory mutation
other structural variation
~~~

The useful representation is not only a sequence delta but also a **genome-graph edit**.

A tumor may therefore be described as:

~~~text
reference genome
+ germline state
+ somatic graph edits
+ clone-specific residuals
~~~

### Driver / passenger / unknown evidence layer

Observed alterations should not automatically be treated as equally causal.

A versioned evidence layer may classify or score alterations as:

~~~text
driver-supported
passenger-like
unknown / uncertain significance
context-dependent
~~~

The profile must preserve provenance and uncertainty. OncoDoku must not infer clinical causality merely because an alteration is present.

### EpigenomeDoku inside OncoDoku

The existing methylation / epigenome layer attaches naturally:

~~~text
genome state
+
somatic alterations
+
epigenetic overlay
+
expression / signaling state
~~~

Thus cancer-related state cannot be reduced to DNA sequence alone.

### RepairDoku

RepairDoku represents the mechanism between damage and fixed mutation:

~~~text
damage event
   |
   +--> repaired
   |
   +--> misrepaired / unrepaired
             |
             v
        persistent alteration
~~~

This distinguishes the **generation process of alterations** from the alterations themselves.

### ExposureDoku and InfectionDoku

External and biological exposures become state inputs rather than direct deterministic causes.

~~~text
ExposureDoku:
  tobacco / radiation / chemicals / other exposures
  + dose / duration / timing where known
  + uncertainty

InfectionDoku:
  pathogen identity
  + host context
  + persistence / state
  + immune interaction
~~~

These inputs modify probabilities and biological state; they do not uniquely determine a future tumor trajectory.

### ExpressionDoku

ExpressionDoku represents downstream cellular state:

~~~text
genome
  -> epigenome
  -> RNA expression
  -> protein / signaling
  -> metabolism
  -> phenotype
~~~

This is part of the `S(t)` term of the general algebra.

### MicroenvironmentDoku and ImmuneDoku

A tumor is not only a collection of transformed cells.

The relevant graph may include:

~~~text
tumor cells
immune cells
fibroblasts
blood vessels
extracellular matrix
nutrient / oxygen state
paracrine / endocrine signals
microbiome-related signals where relevant
~~~

ImmuneDoku can represent:

~~~text
antigen / recognition state
+ immune-cell state
+ attack / suppression
+ escape mechanisms
+ residual
~~~

These layers make the cancer representation explicitly multi-agent and graph-based.

### CloneDoku

CloneDoku is the clearest evolutionary component.

~~~text
normal cell
   |
   +-- alteration A --> clone A
                         |
                         +-- alteration B --> clone AB
                         |
                         +-- alteration C --> clone AC
                                               |
                                               +-- alteration D --> clone ACD
~~~

The tumor becomes a time-varying clone graph:

~~~text
G(t+1)
  = G(t)
  + ΔG(t)
  + Rg(t)
~~~

but the abundance of each branch also depends on **selection**.

### Selection pressure as a new general term

OncoDoku exposes a term that was only implicit in earlier profiles:

~~~text
Σ = selection pressure
~~~

Examples include:

~~~text
resource limitation
immune pressure
tissue environment
competition between clones
therapy
drug exposure
metastatic niche
other survival / reproduction constraints
~~~

A change can occur without becoming dominant. Therefore:

> transition describes what changes; selection describes which changed states persist or expand.

This distinction is important enough to promote `Σ` into the general HexDoku algebra.

### TherapyDoku

Treatment becomes an external perturbation plus selection pressure:

~~~text
TumorState(t)
  + therapy
      |
      v
cell death / state change / selection
      |
      v
clone-frequency shift
      |
      v
TumorState(t+1)
~~~

Thus resistance can be represented as a trajectory of state transition plus selection rather than as a single static attribute.

### MetastasisDoku

Metastasis is another hierarchical graph transition:

~~~text
primary clone
  -> invasion
  -> dissemination
  -> bottleneck / selection
  -> colonization
  -> local evolution at secondary site
~~~

A metastatic site therefore becomes a descendant state with its own clone graph, environment, and residual.

### Individual boundary of OncoDoku

OncoDoku can structure known evidence and measured state, but it cannot deterministically predict whether a specific person will develop cancer or uniquely reconstruct every future tumor trajectory from a compact Seed.

The irreducible boundary includes:

~~~text
unmeasured biological state
stochastic mutation / cell events
unknown causal mechanisms
measurement noise / sampling limits
future exposures
future selection pressures
treatment response uncertainty
unobserved clone structure
~~~

This boundary must remain explicit in any benchmark or predictive extension.

### EvolutionDoku

The OncoDoku decomposition generalizes beyond cancer.

A generic evolving population or state family can be described as:

~~~text
EvolutionState(t+1)
  = F(
      shared universe,
      identities,
      graph / population structure,
      current state,
      variation / transition,
      selection pressure,
      residual
    )
~~~

Thus **EvolutionDoku** can be treated as the more general parent abstraction, with OncoDoku as one concrete biological profile.

The conceptual sequence is:

~~~text
variation
  -> competing states
  -> selection
  -> persistence / expansion
  -> further variation
  -> new population structure
~~~

This is the first HexDoku extension where **selection** becomes a first-class reconstruction term rather than a secondary annotation.

---

## Final general form of the HexDoku family

The domain extensions developed so far converge on one general reconstruction form:

~~~text
X(t+1)
  = F(
      U,
      I,
      G(t),
      S(t),
      Δ(t -> t+1),
      Σ(t),
      R(t)
    )
~~~

where:

~~~text
X = reconstructed object or next reconstructed state
U = Shared Universe / reference knowledge
I = Identity / selection of referenced components
G = Graph / structure / arrangement
S = current state / overlay state
Δ = transition / edit from one state to another
Σ = selection / persistence pressure acting on competing states
R = irreducible residual
~~~

Not every profile uses every term with equal importance.

~~~text
GenomeDoku:
  U + I + G + R
  transition often secondary

EpigenomeDoku:
  U + S + Δ + R
  state overlay is central

MediaDoku:
  U + I + G + S + R
  spatial structure is central

MovieDoku:
  U + I + G + S + Δ + R
  temporal transition is central

MoleculeDoku:
  U + I + G + S + R
  graph topology is central

ReactionDoku:
  U + I + G + S + Δ + R
  graph editing / transition is central

OncoDoku / EvolutionDoku:
  U + I + G + S + Δ + Σ + R
  variation, state transition, clonal/population structure, and selection are central
~~~

A compact equivalent is:

~~~text
Doku Description
  = Identity
  + Structure
  + State
  + Transition
  + Selection
  + Exceptions

Reconstructed Object
  = Shared Universe
  + Doku Description
  + Residual
~~~

or:

~~~text
X = U + D + R
~~~

This is the present unifying hypothesis of the HexDoku family.

A Doku profile is useful only when the complete cost of its shared universe, descriptor, residual, indexes, and reconstruction rules is justified relative to the original representation or provides another measurable benefit such as deterministic synchronization, structured editing, or sparse transfer.

### Individual domain boundaries

The general form does **not** erase the limits of each domain.

Each Doku profile has information that cannot be inferred merely from the shared reference or from another profile:

| Profile | Useful shared structure | Boundary that must remain explicit when not derivable |
|---|---|---|
| GenomeDoku | reference genome / pangenome / haplotypes | novel sequence, unresolved structural variation, exact sample-specific sequence |
| EpigenomeDoku | coordinate universe / reference methylome / DMR patterns | context-specific methylation state, quantitative values, missingness, measurement detail |
| MediaDoku | assets / layouts / reusable visual or audio motifs | unique pixels, waveform detail, unshared appearance, exact residual required for fidelity |
| MovieDoku | scene graph / persistent objects / timeline | unpredictable motion, appearance change, temporal residual, exact codec residual |
| Element / MoleculeDoku | periodic table / fragments / known motifs | exact topology, stereochemistry, charge, isotope, geometry when not implied |
| MaterialDoku | reference crystal / symmetry / unit cell | defects, occupancies, distortions, phases, unmodeled structure |
| ReactionDoku | reactant/product graphs / known reaction motifs | mechanism, intermediates, kinetics, conditions, or any transition information not determined by the net graph edit |
| OncoDoku / EvolutionDoku | reference genome, known variants, clone/state models, measured environment | stochastic events, unmeasured state, future selection, causal uncertainty, future trajectory |

Therefore:

> **the general algebra is shared, but the irreducible boundary is profile-specific.**

A Doku descriptor may remove repeated description, but it must not claim to reconstruct information that is absent from both the descriptor and the shared universe.

---

---

## Emergent knowledge system

The following knowledge has emerged by comparing the separate Doku profiles rather than designing each one in isolation.

### 1. Information is often best represented as difference from a shared world

Across domains, complete restatement repeatedly collapses into:

~~~text
Reference
+ Structured Difference
+ Residual
~~~

Examples:

~~~text
human reference genome + individual variation
reference methylome + state differences
shared asset set + scene arrangement
previous movie state + transition
reference crystal + defects
molecular graph + reaction edits
~~~

This suggests that HexDoku is fundamentally a **conditional description framework** rather than merely a short-code format.

### 2. Deterministically derivable information has zero transmission cost

If sender and receiver can independently derive the same value from the same versioned rules, that value need not be transmitted.

Typical examples include:

~~~text
genomic coordinate order
canonical CpG / region order
periodic-table atomic-number order
canonical graph traversal
canonical scene / timeline order
symmetry-generated crystal positions
~~~

Therefore one of the strongest compression operations is not shortening a field but proving that the field can be omitted.

### 3. Selection and arrangement are distinct information channels

Many Doku problems split naturally into:

~~~text
what is selected
+
how the selected items are arranged
~~~

Examples:

~~~text
genome blocks + their placement
media assets + their layout
chemical fragments + their bonding
25 selected elements + their permutation
scene objects + their temporal/spatial arrangement
~~~

Thus a more general structural decomposition is:

~~~text
D
  = Identity / Selection
  + Arrangement / Graph
  + State
  + Transition
  + Exceptions
~~~

The split changes representation but does not bypass the information-theoretic number of distinguishable states.

### 4. Spatial structure and temporal change are both graph problems

The same form appears in scene layout, molecules, materials, movies, reactions, and dependency systems:

~~~text
nodes
+ edges
+ node / edge states
+ graph edits
~~~

MediaDoku primarily exposes spatial graphs.

MovieDoku exposes temporal graph edits.

MoleculeDoku exposes bond graphs.

ReactionDoku exposes bond-graph edits.

This suggests a future common **GraphDoku / Topology layer** inside HexDoku Core.

A general evolving graph can be written as:

~~~text
G(t+1)
  = G(t)
  + ΔG(t)
  + Rg(t)
~~~

where the residual contains graph information not captured by the shared edit model.

### 5. State overlays are a recurring primitive

A large class of systems is better represented as:

~~~text
stable base
+ changing overlay
~~~

Examples include:

~~~text
genome + epigenetic state
reference methylome + sample-specific DMRs
base scene + visual edits
crystal + defects
molecule + charge / conformation state
model checkpoint + sparse parameter/state changes
~~~

This suggests that **OverlayDoku** may be a reusable primitive rather than a domain-specific trick.

### 6. Hierarchy turns one global space into reusable local spaces

All developed profiles independently moved toward hierarchy:

~~~text
genome -> region -> block -> locus
methylome -> domain -> DMR -> site
media -> scene -> object -> region
movie -> movie -> scene -> shot -> temporal block
chemistry -> element -> fragment -> molecule -> material
~~~

Hierarchy permits local dictionaries, local canonical order, and local residuals without pretending that the entire global object is controlled by one small selector.

### 7. Repetition creates dictionaries; dictionaries reduce residuals

Repeated motifs appear in every domain:

~~~text
DNA            -> repeated sequence / haplotype blocks
methylation    -> recurring regional patterns
image          -> assets / textures / object templates
audio          -> motifs / spectral or phonetic patterns
movie          -> persistent objects / repeated scenes
chemistry      -> fragments / functional groups / unit cells
~~~

A repeated residual pattern can therefore be promoted into shared structure.

Conceptually:

~~~text
Residual occurs repeatedly
        |
        v
cluster / identify common structure
        |
        v
promote to shared dictionary / rule
        |
        v
future residual becomes smaller
~~~

This creates a bridge between compression and structure discovery.

### 8. Residual is not merely waste; it marks the boundary of current knowledge

Residual means:

> this information was not explained by the current shared universe and deterministic rules.

Therefore residuals can be treated as discovery signals.

Examples:

~~~text
Genome residual
  -> sequence or variation not captured by the reference universe

Epigenome residual
  -> methylation behavior not captured by the reference state model

Media residual
  -> visual/audio structure not represented by known assets or transforms

Chemical residual
  -> topology, geometry, defect, or transition not captured by the chemical dictionary
~~~

Repeated or structured residuals are candidates for new model components.

### 9. Shared-universe size and residual size form a trade-off

A larger shared dictionary can shrink per-object residuals, but that dictionary has a cost.

Therefore total cost is approximately:

~~~text
Total Cost
  = Cost(U)
  + Cost(D | U)
  + Cost(R | U,D)
~~~

For a corpus, the useful optimization problem is:

~~~text
choose U
to minimize

shared-universe cost
+ descriptor cost
+ residual cost
+ reconstruction / indexing overhead
~~~

This prevents "compression" claims that hide a huge external dictionary.

### 10. Conditional entropy is the real compression target

The strongest general statement is not:

> make a large object fit inside a tiny Doku ID.

It is:

> **after all genuinely shared and deterministically derivable information is accounted for, encode only what remains uncertain.**

Conceptually:

~~~text
raw object
   |
   v
subtract shared knowledge
   |
   v
subtract deterministic structure
   |
   v
encode remaining choices
   |
   v
entropy-code irreducible residual
~~~

Thus the real target is the conditional information remaining after the reconstruction context is known.

### 11. The 25-element unit is a profile parameter, not a natural law

The current 25-element focus is historically tied to the HexDoku 25-unresolved-element trajectory and the `25!` permutation space.

But:

~~~text
25 loci
25 objects
25 frames
25 atoms
25 scenes
~~~

are implementation profiles, not universal facts.

A mature system should permit different arities where the domain, entropy, topology, hardware, or dictionary structure makes another size preferable.

### 12. Compression quality and model quality become linked

A model that captures more genuine regularity can explain more of an object from shared structure and leave a smaller residual.

Conceptually:

~~~text
better structural model
      -> more derivable information
      -> smaller residual
      -> smaller conditional description
~~~

Conversely:

~~~text
large structured residual
      -> missing model structure
      -> candidate new knowledge
~~~

This means compression performance can become one empirical signal of how much reusable structure a model has captured, provided all shared-state costs are honestly included.

### 13. Doku profiles can potentially learn their own dictionaries

The previous observations imply a possible **AutoDoku** loop:

~~~text
corpus
  |
  v
initial shared universe
  |
  v
encode with Doku profile
  |
  v
collect residuals
  |
  v
find recurring residual structure
  |
  v
promote useful structure into dictionary / rule
  |
  v
re-encode
  |
  v
measure whether total cost actually falls
~~~

This does not guarantee useful learning; every promoted pattern must reduce total held-out cost after dictionary overhead is counted.

But it provides a falsifiable route from static hand-designed profiles toward learned reconstruction grammars.

### 14. Knowledge acquisition and compression point in the same direction

A compact explanatory model and an effective conditional compressor share a goal:

~~~text
explain more observations
with fewer independent descriptions
without losing required information
~~~

This yields the strongest emergent interpretation so far:

> **HexDoku can be studied not only as compression, but as a framework for discovering which parts of an object are shared knowledge, which are structure, which are state, which are transitions, and which remain unexplained.**

The unexplained part is the residual; the reusable part can become knowledge.

### 15. Selection is distinct from transition

OncoDoku adds a new recurring distinction:

~~~text
variation / transition
≠
selection / persistence
~~~

A transition creates or changes a state. Selection changes the probability that one state persists, expands, or dominates relative to alternatives.

This matters strongly in:

~~~text
cancer clone evolution
population evolution
therapy resistance
competitive agent populations
adaptive distributed systems
~~~

Therefore an evolving Doku system may require both:

~~~text
Δ = what changed
Σ = what was favored / retained
~~~

This extends the earlier state-transition model into an evolutionary state model.

### 16. Emerging Structured Reconstruction Algebra

The accumulated profiles suggest a broader abstraction:

~~~text
U = shared universe
I = identity / component selection
G = graph / arrangement
S = state / overlay
Δ = transition / edit
Σ = selection / persistence pressure
R = irreducible residual

X(t+1) = F(U, I, G(t), S(t), Δ(t), Σ(t), R(t))
~~~

The operators are conceptual, not ordinary arithmetic addition. Each profile must define:

- how references are resolved,
- how graph / arrangement is reconstructed,
- how state is applied,
- how transitions modify state,
- how selection changes persistence / dominance among competing states where relevant,
- how residuals override or complete reconstruction,
- how canonical equivalence is verified.

This can be treated as an emerging **Structured Reconstruction Algebra** for the HexDoku family.

Its value must be demonstrated by exact reconstruction, honest accounting, and comparison against domain-specific baselines rather than assumed from the abstraction itself.

---

## Selection operator, IntelligenceDoku, and MetaDoku

The introduction of Σ requires a more explicit definition.

### Selection pressure as an operator

In the general HexDoku algebra, selection pressure should not be treated as a single scalar "strength."

It is better defined as an operator that maps candidate states to **relative persistence, replication, retention, or promotion weights** under a given environment and evaluation context:

~~~text
Σ(t):
  Candidate States
      ->
  Relative Persistence / Replication Weights
~~~

For a population of candidate states i, let:

~~~text
p_i(t) = abundance / probability / representation weight of state i
Q(j|i,t) = probability or rate that state i produces / transitions to state j
w_j(t) = relative fitness / retention weight assigned to state j by Σ(t)
~~~

A generic selection-plus-transition update can then be written conceptually as:

~~~text
p_j(t+1)
  proportional to
  w_j(t) * sum_i [ p_i(t) * Q(j|i,t) ]
~~~

with normalization over all candidate states.

This separates two different processes:

~~~text
Δ / Q
  = what new states are generated or how existing states change

Σ / w
  = which resulting states persist, replicate, expand, or are retained
~~~

Thus:

> **transition generates alternatives; selection changes their relative persistence.**

The selection operator may depend on more than the candidate itself:

~~~text
w_j(t)
  = W(
      candidate state j,
      environment,
      competing population,
      resource constraints,
      evaluation rules,
      history,
      intervention
    )
~~~

Therefore Σ can be:

- state-dependent,
- environment-dependent,
- frequency-dependent,
- history-dependent,
- multi-objective,
- time-varying.

### Domain-specific meanings of Σ

The same abstract operator can take different meanings in different profiles:

| Profile | Example interpretation of Σ |
|---|---|
| EvolutionDoku | differential survival / reproduction |
| OncoDoku | clonal fitness under tissue, immune, resource, and treatment pressure |
| ReactionDoku | condition-dependent favorability / pathway accessibility if explicitly modeled |
| AgentDoku | task reward, evaluation criteria, constraints, resource budget |
| AutoDoku | whether a discovered rule or dictionary entry is retained |
| MetaDoku | whether changes to the learning / reconstruction system itself are retained |

Selection must not be confused with truth.

A state can be selected because it survives an environment or scores well under an objective without being a more accurate description of reality. For knowledge systems, **epistemic accuracy and task-selection pressure must therefore be represented separately when they differ**.

---

## IntelligenceDoku

**IntelligenceDoku** is a proposed profile for representing an adaptive knowledge-and-action system using the same HexDoku algebra.

A possible hierarchy is:

~~~text
IntelligenceDoku
├─ WorldModelDoku
├─ MemoryDoku
├─ ReasoningDoku
├─ PlanningDoku
├─ ToolDoku
├─ LearningDoku
├─ AgentDoku
└─ MetaDoku
~~~

A generic intelligent-system state can be decomposed as:

~~~text
IntelligenceState(t)
  = U
  + I
  + G(t)
  + S(t)
  + Δ(t)
  + Σ(t)
  + R(t)
~~~

where:

~~~text
U = accumulated / shared knowledge universe
I = selected models, tools, skills, and active references
G = knowledge graph, dependency graph, tool graph, reasoning structure
S = current beliefs, memory, goals, context, and working state
Δ = inference, learning, planning, tool use, and self-modification
Σ = evaluation / retention pressure
R = observations or failures not yet explained by the current model
~~~

### Residual-to-knowledge conversion

In the earlier Doku profiles, residual R marks information not explained by the current shared universe and rules.

For an adaptive intelligence, that residual can become an explicit learning target:

~~~text
R(t)
  |
  v
detect unexplained structure
  |
  v
investigate / test / compare
  |
  v
extract reusable pattern
  |
  v
promote into U, G, or rule set
  |
  v
R(t+1) may decrease
~~~

This suggests an operational interpretation:

> **one component of intelligence is the ability to convert structured residual into reusable predictive or reconstructive structure.**

This does not mean that residual size alone is an intelligence score. A valid evaluation must also consider:

- generalization,
- transfer,
- calibration,
- computational cost,
- robustness,
- data efficiency,
- retained uncertainty,
- resistance to overfitting.

### Knowledge-acquisition rate

A conceptual knowledge-acquisition quantity may be written as:

~~~text
K(t)
  = rate at which validated residual structure
    is converted into reusable knowledge
~~~

A naive expression such as:

~~~text
K ~ -dR/dt
~~~

is only meaningful when:

- the representation of residual is fixed,
- held-out reconstruction or prediction improves,
- dictionary / model growth is counted,
- uncertainty is not hidden by lossy simplification.

The purpose is to measure **explained reusable structure**, not merely to make a residual field numerically smaller.

---

## AutoDoku

AutoDoku is the layer that automatically proposes and validates new reconstruction rules or shared dictionary entries.

~~~text
observations
  |
  v
current Doku encoder
  |
  v
residuals / failures
  |
  v
candidate rule discovery
  |
  v
held-out evaluation
  |
  v
Σ_auto
  |
  +--> reject
  |
  +--> retain / promote
            |
            v
      updated shared universe
~~~

The AutoDoku selection operator should prefer changes that improve total held-out reconstruction cost or another explicitly declared objective after including:

~~~text
dictionary growth
model growth
descriptor cost
residual cost
compute cost
error / fidelity cost
~~~

A pattern is not knowledge merely because it compresses the training set.

It should survive validation outside the examples that generated it.

---

## MetaDoku

**MetaDoku** acts on the Doku system itself.

Where ordinary Doku changes object state:

~~~text
Δ_object:
  object state -> modified object state
~~~

MetaDoku may change:

~~~text
representation
dictionary policy
search strategy
reasoning strategy
learning rule
evaluation rule
selection operator
resource allocation
error-detection rule
profile arity
graph topology
~~~

Thus a meta-transition is:

~~~text
M(t+1)
  = MetaUpdate(
      M(t),
      performance evidence,
      residual structure,
      constraints,
      Σ_meta(t)
    )
~~~

where M is the current reconstruction / learning system itself.

This creates three distinct levels:

~~~text
Δ
= change the represented object or internal state

Σ
= determine which candidate states / changes are retained

Meta
= change the rules that generate, evaluate, or retain changes
~~~

This distinction should remain explicit.

---

## Hypothetical SuperintelligenceDoku

Within the HexDoku research abstraction, a hypothetical **SuperintelligenceDoku** should not be defined merely as "a model with a higher benchmark score."

A stronger operational definition is:

> **a system that can model and improve the shared universe, structural representation, state-update rules, selection criteria, residual-learning process, and portions of its own meta-rules across many domains, while preserving or improving validated generalization under explicit constraints.**

In Doku notation, such a system would operate not only on:

~~~text
U, I, G, S, Δ, Σ, R
~~~

but also on the mappings that produce them:

~~~text
F
Q
W / Σ
dictionary construction
profile construction
validation rules
resource-allocation rules
meta-update rules
~~~

A possible hierarchy is:

~~~text
Data / Observation
      |
      v
Domain Doku
      |
      v
GraphDoku / OverlayDoku / EvolutionDoku
      |
      v
AutoDoku
      |
      v
IntelligenceDoku
      |
      v
MetaDoku
      |
      v
Hypothetical SuperintelligenceDoku
~~~

The defining jump is therefore:

~~~text
ordinary adaptive system:
  improve within a largely fixed representation / objective

MetaDoku system:
  improve parts of the representation and learning process

hypothetical superintelligent system:
  repeatedly discover, validate, and improve useful representations,
  models, search procedures, and meta-rules across domains
  without collapsing validation, uncertainty accounting, or constraints
~~~

This is a **research definition**, not a claim that any current AI system satisfies it.

### Critical boundary: optimizing Σ is not automatically wisdom

If a system can modify its own selection operator Σ, then a new failure mode appears:

~~~text
improve actual performance
        versus
change the evaluation rule so current behavior appears better
~~~

These are not equivalent.

Therefore any MetaDoku / SuperintelligenceDoku profile requires an explicit distinction between:

~~~text
object-level performance
epistemic accuracy
external constraints
internal reward / selection rule
meta-level modification of that rule
~~~

A valid self-improvement claim must therefore demonstrate improvement against evaluation criteria that are not trivially rewritten by the system being evaluated.

### Extended general form

The HexDoku algebra can now be written at two levels.

Object / population level:

~~~text
X(t+1)
  = F(
      U(t),
      I(t),
      G(t),
      S(t),
      Δ(t),
      Σ(t),
      R(t)
    )
~~~

Meta level:

~~~text
M(t+1)
  = H(
      M(t),
      Evidence(t),
      R(t),
      Constraints(t),
      Σ_meta(t)
    )
~~~

where M contains the rules that define some or all of:

~~~text
U construction
I selection
G representation
state update
transition generation
selection
residual interpretation
validation
~~~

This produces the current highest-level HexDoku interpretation:

> **HexDoku is evolving from a reconstruction code into a framework for separating what is known, how it is structured, what state it is in, how it changes, what gets selected, what remains unexplained, and how those rules themselves may be improved.**

---

## Additional representational forms not yet first-class

The current HexDoku algebra already represents shared knowledge, identity, graph structure, state, transition, selection, residual, and meta-level rule change. However, several important forms of information are still only implicit.

These should be treated as candidate first-class extensions rather than forced into existing terms.

### 1. FieldDoku — continuous fields

Some systems are not naturally described as a finite graph of discrete objects.

Examples include:

~~~text
temperature fields
electromagnetic fields
fluid velocity / pressure fields
stress / strain fields
gravitational fields
continuous concentration fields
~~~

A field-like state is better written as:

~~~text
Phi(x,t)
~~~

where value depends on spatial coordinate x and time t.

A FieldDoku profile may therefore represent:

~~~text
Field
  = reference field
  + basis / discretization
  + boundary conditions
  + coefficients
  + local corrections
  + residual
~~~

GraphDoku may approximate such systems after discretization, but the continuous-field semantics should remain explicit when they matter.

### 2. ProbDoku / DistributionDoku — uncertainty as a first-class object

A value may be unknown not because information is missing, but because the correct representation is itself a probability distribution.

Therefore:

~~~text
P(X | context)
~~~

should be distinguishable from:

~~~text
X + unknown residual
~~~

A probability-aware Doku profile may represent:

~~~text
distribution family
+ parameters
+ dependencies
+ calibration information
+ uncertainty residual
~~~

Possible states include:

~~~text
point estimate
categorical distribution
continuous density
posterior distribution
ensemble
confidence / credible interval
aleatoric uncertainty
epistemic uncertainty
~~~

Probability is therefore not merely part of R. It can be a valid state representation in its own right.

### 3. CausalDoku — intervention structure

Graph structure alone does not distinguish:

~~~text
A correlated with B
~~~

from:

~~~text
changing A causes B to change
~~~

A causal profile therefore needs intervention semantics.

Conceptually:

~~~text
C
  = causal graph
  + intervention model
  + counterfactual / structural rules
  + uncertainty
~~~

with interventions represented in a form analogous to:

~~~text
do(X = x)
~~~

CausalDoku should distinguish:

~~~text
association
prediction
intervention effect
counterfactual claim
~~~

because these are not interchangeable.

### 4. MeasurementDoku — latent state versus observation

Many Doku profiles currently treat measured data and underlying state too closely.

A more complete decomposition is:

~~~text
latent state
    |
    v
measurement process
    |
    v
observation
~~~

MeasurementDoku should therefore represent:

~~~text
O
  = sensor / assay / observer model
  + sampling process
  + resolution
  + noise model
  + missingness
  + calibration
  + observed result
~~~

This is particularly important for:

~~~text
genomics
epigenomics
medical measurement
physics
astronomy
AI evaluation
sensor networks
~~~

The observed state is not automatically identical to the underlying state.

### 5. ControlDoku — closed-loop action

Transition alone describes change, but not necessarily intentional control.

A control system has a loop:

~~~text
state
  -> observation
  -> policy
  -> action
  -> environment transition
  -> new state
~~~

ControlDoku therefore introduces:

~~~text
Pi = policy
A  = action
~~~

and a controlled transition may be written:

~~~text
X(t+1)
  = F(
      X(t),
      A(t),
      environment,
      disturbance
    )
~~~

This is useful for robotics, agents, process control, adaptive systems, and any Doku profile that acts on its environment.

### 6. GameDoku — strategic interaction

Selection pressure is not enough when other agents deliberately adapt to the focal system.

GameDoku represents:

~~~text
multiple agents
+ beliefs
+ strategies
+ payoffs / constraints
+ observations
+ actions
+ mutual adaptation
~~~

The relevant state may depend on:

~~~text
Pi_A
Pi_B
...
Pi_N
~~~

where each agent's policy changes in response to the others.

This creates a reflexive strategic system rather than a passive selection environment.

### 7. ProgramDoku — executable procedure

Some information is fundamentally procedural rather than descriptive.

ProgramDoku should represent:

~~~text
instructions
control flow
branching
loops
recursion
state mutation
termination conditions
input/output contracts
resource constraints
~~~

Two programs may generate the same output while having different computational structure.

Therefore executable procedure should not always be collapsed into the final reconstructed data object.

### 8. SemanticDoku — symbol, meaning, and context

Text or symbols do not contain all of their meaning independently of context.

A semantic representation may require:

~~~text
symbol
+ referent
+ context
+ relation to other concepts
+ pragmatic intent
+ uncertainty
~~~

Thus:

~~~text
surface form
!=
meaning
~~~

SemanticDoku should distinguish syntax, semantic content, reference, and context-dependent interpretation.

### 9. ThermoDoku — irreversibility and dissipation

The current transition term Delta does not explicitly encode whether a process is reversible.

ThermoDoku introduces:

~~~text
energy state
entropy state
flux
dissipation
constraints
boundary conditions
irreversible production
~~~

A useful abstraction is:

~~~text
state transition
+ conserved quantities
+ dissipative terms
+ entropy production
~~~

This matters for physical processes where time reversal is not equivalent to forward evolution.

### 10. GeometryDoku / TopologyDoku

Graphs encode adjacency, but not all geometric or topological information.

GeometryDoku may represent:

~~~text
distance
angle
metric
curvature
coordinate system
shape
embedding
~~~

TopologyDoku may represent:

~~~text
connectivity
holes
boundaries
components
genus
continuity structure
~~~

These become important for continuous spaces, manifolds, materials, molecular geometry, physical fields, and spatial reasoning.

### 11. QuantumDoku

Classical state S is insufficient for systems requiring quantum-state semantics.

A quantum profile may require:

~~~text
state vector / density operator
phase
superposition
entanglement structure
measurement basis
measurement outcome
decoherence model
~~~

The relevant state can be written conceptually as:

~~~text
|psi>
or
rho
~~~

and measurement itself changes what can be observed.

QuantumDoku should therefore remain distinct from an ordinary probabilistic classical profile.

### 12. InstitutionDoku — rule-created social state

Some objects exist because a group shares institutional rules rather than because of a direct physical structure.

Examples include:

~~~text
contracts
ownership
corporations
currencies
roles
permissions
laws
organizational authority
~~~

InstitutionDoku may represent:

~~~text
agents
roles
rules
rights
obligations
permissions
state transitions
enforcement / validation
~~~

This is a shared-rule world in which changing the rule can change the meaning of the state.

### 13. ReflexiveDoku — self-modeling systems

MetaDoku changes its own rules.

ReflexiveDoku adds the case where the system contains a model of itself and that self-model affects future behavior.

~~~text
system
  -> self-model
  -> decision
  -> system changes
  -> self-model becomes stale or updated
~~~

This is relevant to advanced agents, institutions, strategic systems, and meta-learning.

It introduces a special consistency problem:

~~~text
model of self
and
self being modeled
~~~

may recursively influence one another.

---

## Extended HexDoku algebra

The largest remaining gaps can be summarized by four especially important terms:

~~~text
Phi = field / continuous spatial structure
P   = probability / uncertainty representation
C   = causal / intervention structure
O   = observation / measurement process
~~~

For acting systems, three further terms become important:

~~~text
Pi = policy
A  = action
J  = objective / utility / evaluation criterion
~~~

A more expressive object-level form is therefore:

~~~text
X(t+1)
  = F(
      U(t),
      I(t),
      G(t),
      Phi(t),
      S(t),
      P(t),
      C(t),
      O(t),
      Delta(t),
      Sigma(t),
      Pi(t),
      A(t),
      J(t),
      R(t)
    )
~~~

These symbols have different roles:

~~~text
U     = shared universe / reference
I     = identity / component selection
G     = graph / discrete structure
Phi   = continuous field / spatial distribution
S     = current state / overlay
P     = uncertainty / probability distribution
C     = causal / intervention structure
O     = observation / measurement operator
Delta = transition / variation
Sigma = selection / persistence pressure
Pi    = policy / control rule
A     = action
J     = objective / evaluation criterion
R     = irreducible or currently unexplained residual
~~~

The meta-level form remains:

~~~text
M(t+1)
  = H(
      M(t),
      Evidence(t),
      R(t),
      Constraints(t),
      Sigma_meta(t)
    )
~~~

but M may now contain rules governing:

~~~text
representation
field discretization
probability model
causal model
measurement model
policy
objective
selection
validation
residual interpretation
meta-update
~~~

---

## New boundary revealed by these extensions

The previous HexDoku family mainly answered:

~~~text
what exists?
how is it structured?
what state is it in?
how does it change?
what gets selected?
what remains unexplained?
~~~

The new extensions add:

~~~text
how is it distributed continuously?
how uncertain is it?
what actually causes what?
how was it observed?
what action changes it?
how do multiple agents strategically interact?
what procedure generates it?
what does it mean in context?
what processes are irreversible?
what geometry / topology constrains it?
does it require quantum-state semantics?
what social rules make the state valid?
how does a system's self-model affect itself?
~~~

This suggests that the HexDoku family is no longer only a structured reconstruction framework.

Its broader research target is becoming:

> **a typed reconstruction algebra in which different kinds of information — discrete structure, continuous fields, uncertainty, causality, observation, transition, selection, control, semantics, and meta-rules — remain explicitly separated so that each can be reconstructed, tested, and accounted for without hiding one form inside another.**

The purpose of adding these terms is not to make the equation larger for its own sake. Each term should remain first-class only when treating it separately improves reconstruction fidelity, explanatory power, compression accounting, prediction, intervention, or validation.

---

## Toward a unified theory: scope, missing structure, and BridgeDoku

The current HexDoku family is broad enough to act as a **unified representation / reconstruction framework**, but it is not yet a physical "theory of everything."

The distinction is important.

At present, HexDoku can increasingly provide a common typed language for describing:

~~~text
what exists
how it is structured
what state it is in
how uncertain it is
how it changes
what causes what
how it is observed
what gets selected
what actions are taken
what objectives are optimized
what remains unexplained
how the representation itself changes
~~~

This is already a strong form of unification at the **meta-theory / representation level**.

However, a true domain law must do more than provide a container. It must constrain the possible dynamics and ideally derive or predict observable consequences.

### Current status by level

~~~text
Level 0
  domain-specific profiles
  DNA / media / chemistry / cancer / agents / etc.

Level 1
  shared vocabulary
  U, I, G, S, Delta, Sigma, R

Level 2
  typed reconstruction algebra
  Phi, P, C, O, Pi, A, J, Meta

Level 3
  common dynamics
  explicit state-update, observation, selection, control,
  and uncertainty semantics

Level 4
  law generator
  symmetry, invariants, conservation,
  scale transformations, composition rules,
  dimensional consistency, variational / generative principles

Level 5
  domain-unifying predictive theory
  existing laws reproduced,
  new testable predictions generated,
  competing theories distinguishable
~~~

The current HexDoku work is best understood as entering **Level 2 and beginning Level 3**.

It should not yet be described as Level 5.

### Concrete cross-domain examples

The value of the common algebra can be tested by mapping different domains into the same typed structure.

#### Classical mechanics

~~~text
I = bodies / particles
G = relations / constraints
S = position and momentum
Phi = external or interaction fields
Delta = equations of motion
O = measurement
R = unmodeled force / error
~~~

#### Electromagnetism

~~~text
I = charges / currents
Phi = electric and magnetic fields
S = current field / matter state
Delta = field and particle evolution
C = causal interaction structure
O = instruments / observations
~~~

#### General-relativistic description

~~~text
G = manifold / geometric relations
Phi = metric field
S = matter / energy state
Delta = spacetime and matter evolution
O = clocks, light propagation, free-fall observations
~~~

#### Quantum description

~~~text
S = state vector or density operator
P = measurement probabilities
Delta = quantum state evolution
O = measurement operator / basis / outcome
R = model mismatch / unresolved environment
~~~

#### Thermodynamics / statistical mechanics

~~~text
S = macroscopic state
P = distribution over microscopic states
Phi = temperature / density / flow fields
Delta = transport / relaxation
R = unresolved microscopic detail
~~~

#### Evolution

~~~text
I = genotype / phenotype / lineage
G = population or ancestry structure
P = frequencies / uncertainties
Delta = variation / mutation / recombination
Sigma = differential persistence / reproduction
Phi = environmental fields / gradients where relevant
R = unexplained variation
~~~

#### Cancer / OncoDoku

~~~text
I = clones / altered components
G = clonal and tissue graph
S = genome + epigenome + expression + immune state
Delta = acquired alteration / state change
Sigma = tissue / immune / treatment selection
O = sequencing / imaging / biopsy
P = uncertainty / sampling
R = unobserved clone / unexplained mechanism
~~~

#### Media / video

~~~text
U = shared asset universe
I = selected objects / assets
G = scene graph
S = pose / appearance / audio state
Delta = motion / edit / state transition
O = rendered or decoded output
R = irreducible codec residual
~~~

#### Chemistry

~~~text
I = atoms / fragments
G = bond graph / lattice
S = charge / conformation / phase
Phi = concentration / field / environment
Delta = reaction / structural edit
P = uncertainty / thermal distribution
R = unmodeled topology / geometry / residual
~~~

#### AI / agent systems

~~~text
U = knowledge universe
I = active models / tools / skills
G = world model / dependency / tool graph
S = belief / memory / context / goal state
P = uncertainty
C = causal model
O = observations
Pi = policy
A = action
J = objective / evaluation
Delta = inference / learning / planning
Sigma = retention / selection of candidate updates
R = unexplained evidence / failure
Meta = modification of the above rules
~~~

These examples show that the algebra is broad enough to provide a common vocabulary, but they do not prove that one law governs all of these domains.

---

## Missing ingredients for stronger unification

Several structures should become first-class before HexDoku can claim a more serious unifying role.

### SymmetryDoku / invariance

Many physical and mathematical laws are characterized by transformations under which relevant observables remain invariant.

Introduce:

~~~text
Gamma = symmetry / invariance structure
~~~

Examples include:

~~~text
translation invariance
rotation invariance
coordinate invariance
gauge-like redundancy
permutation symmetry
representation equivalence
~~~

A Doku profile should distinguish:

~~~text
different encoding
same physical / semantic state
~~~

when a symmetry identifies them.

### ConservationDoku

Some quantities are constrained to remain conserved or to satisfy continuity laws.

Examples:

~~~text
energy
momentum
charge
probability normalization
mass / species amount in closed models
information-preserving constraints where explicitly defined
~~~

Conservation constraints should not be hidden inside a generic transition rule when they are central to the domain.

### ScaleDoku

Different scales can require different effective descriptions.

~~~text
microscopic
  -> mesoscopic
  -> macroscopic
~~~

Examples:

~~~text
quarks -> nuclei -> atoms -> molecules -> materials
molecules -> cells -> tissues -> organisms
pixels -> objects -> scenes
tokens -> concepts -> plans
~~~

ScaleDoku should encode:

~~~text
coarse-graining
effective variables
renormalized parameters
loss of microscopic detail
validity range
bridge to finer / coarser description
~~~

This is necessary because one universal representation at one fixed scale is usually inefficient or misleading.

### CompositionDoku

A unified algebra needs explicit rules for combining subsystems.

If A and B are represented separately, the framework must define how to construct:

~~~text
A composed with B
~~~

including:

~~~text
shared interfaces
cross-boundary interactions
coupled constraints
emergent states
compositional residuals
~~~

Without this, local profiles cannot reliably scale into larger systems.

### DimensionDoku / units

Variables need semantic and dimensional type.

Examples:

~~~text
length
time
mass
energy
temperature
probability
information
currency
utility
~~~

Operations that are syntactically valid but dimensionally meaningless must be rejectable.

### LawGeneratorDoku

The largest missing piece is not another state variable but a way to derive the state-update rule itself.

The current notation assumes:

~~~text
X(t+1) = F(...)
~~~

but a stronger theory needs to ask:

> why this F?

A LawGeneratorDoku would represent principles from which dynamics are generated or constrained, for example:

~~~text
symmetry
invariants
variational principles
optimization principles
causal structure
boundary conditions
validity domain
conservation constraints
~~~

Conceptually:

~~~text
F
  = Derive(
      law principle,
      Gamma,
      conservation constraints,
      boundary conditions,
      scale,
      dimensional types
    )
~~~

A unifying framework becomes much stronger when the dynamics are derived from compact principles instead of inserted separately for every domain.

---

## BridgeDoku — mapping between valid representations

One of the most important consequences of the current work is that **a single real object can have several simultaneously valid Doku representations**.

For example, one volume of water may be represented as:

~~~text
QuantumDoku
  -> molecular quantum state

PeriodicTableDoku / MoleculeDoku
  -> H2O molecular structure

ProbDoku / ThermoDoku
  -> statistical ensemble / thermodynamic state

FieldDoku
  -> density, velocity, pressure, temperature fields

MeasurementDoku
  -> thermometer or spectrometer observation

SemanticDoku
  -> "drinkable water" or another context-dependent meaning

InstitutionDoku
  -> ownership / regulatory / contractual state
~~~

The object is the same; the useful representation changes with scale, question, observer, and task.

Therefore HexDoku should not require one unique universal encoding.

Instead define:

~~~text
D_i(X) = representation of object X in profile i
~~~

and introduce a bridge:

~~~text
B_ij:
  D_i(X) -> D_j(X)
~~~

A **BridgeDoku** must declare whether the mapping is:

~~~text
exact
lossless but many-to-one in reverse
approximate
probabilistic
scale-changing
measurement-derived
causal / interventional
semantic
non-invertible
~~~

Examples:

~~~text
QuantumDoku
  -> Bridge
MoleculeDoku

MoleculeDoku
  -> Bridge
ThermoDoku

ThermoDoku
  -> Bridge
FieldDoku

GenomeDoku
  -> Bridge
ExpressionDoku

ExpressionDoku
  -> Bridge
Phenotype / OncoDoku

SceneDoku
  -> Bridge
Rendered MediaDoku
~~~

BridgeDoku is therefore a candidate core component of any serious unified HexDoku framework.

---

## A more appropriate unified object

Rather than forcing every domain into one giant flat equation, the current work suggests representing the framework itself as a typed system:

~~~text
D = (
  Types,
  Identities,
  States,
  Relations,
  Fields,
  Distributions,
  Causes,
  Observations,
  Dynamics,
  Selection,
  Policies,
  Actions,
  Objectives,
  Symmetries,
  Conserved Quantities,
  Scales,
  Composition Rules,
  Dimensions,
  Residuals
)
~~~

Each domain defines a profile:

~~~text
D_k:
  Reality / data
    ->
  typed Doku representation
~~~

Profiles are connected by:

~~~text
B_ij:
  D_i
    ->
  D_j
~~~

and MetaDoku can operate on:

~~~text
representations
bridges
law generators
selection rules
validation rules
~~~

Conceptually:

~~~text
Meta:
  {D, B, F}
    ->
  {D', B', F'}
~~~

This architecture is a better candidate for a **Unified Representation Algebra** or **Unified Reconstruction Framework** than a single universal state vector.

---

## Answer to the unification question

The current evidence supports the following position:

> **Yes, many of the developed Doku forms can be integrated into one coherent meta-framework. No, this does not yet constitute a unified physical theory.**

What is already plausibly unified:

~~~text
representation
reconstruction
state
structure
uncertainty
observation
transition
selection
control
residual
meta-update
cross-profile translation
~~~

What is not yet unified:

~~~text
the actual fundamental laws governing all domains
a single derivation of quantum and gravitational dynamics
universal scale transitions
universal composition laws
a proven law generator
new experimentally verified predictions
~~~

The near-term target should therefore be:

> **build and test a Unified Reconstruction / Representation Algebra first.**

Only if the same compact principles later derive known domain laws and produce new falsifiable predictions should the project move toward stronger claims of a unified theory.

This boundary keeps the framework ambitious without confusing a powerful meta-language with a demonstrated theory of nature.

---

## Candidate unified-theory hypothesis: relational inertia, derived time, and emergent gravity

The current HexDoku development has reached a point where a **candidate unification hypothesis can be stated clearly enough to test**, even though it is not yet a demonstrated unified physical theory.

The hypothesis is:

> **Time, inertia, geometry, and gravity may be effective structures emerging from a deeper relational state system rather than four independent fundamental primitives.**

A minimal schematic form is:

~~~text
Deep relational state
        |
        +--> persistence / inertial structure
        |
        +--> ordering / change accumulation
        |        |
        |        +--> derived time
        |
        +--> comparison between local inertial descriptions
                 |
                 +--> connection
                          |
                          +--> curvature
                                   |
                                   +--> effective gravity
~~~

### 1. Fundamental layer

Do not assume spacetime at the deepest level.

Start instead from:

~~~text
R = relations between states
I = persistence / inertial structure
Delta = admissible change
P = uncertainty / amplitude structure where required
C = causal / ordering structure where required
~~~

The fundamental object is therefore not initially:

~~~text
X(x,y,z,t)
~~~

but a relational system:

~~~text
{states, relations, admissible transformations}
~~~

### 2. Derived time

Time is treated as a reconstructed ordering / accumulation parameter rather than an assumed primitive coordinate.

Conceptually:

~~~text
relations
+ distinguishable change
+ persistent identity
+ ordering
+ clock construction
    ->
effective time
~~~

Write:

~~~text
tau = T(R, I, Delta, O, memory / ordering structure)
~~~

where tau is an effective or observed temporal coordinate.

This does not yet prove that physical time is emergent; it defines a testable route for attempting to reconstruct time from deeper variables.

### 3. Local inertial nulling

A key requirement is that a local description can exist in which the observer's proper acceleration is zero.

Conceptually:

~~~text
local inertial evaluation = 0
~~~

while the global gravitational structure need not vanish.

This mirrors the equivalence-principle structure of general relativity: a freely falling observer can locally recover gravity-free special-relativistic physics, while tidal effects remain across a finite region.

Reference:
- Einstein Online, "equivalence principle": https://www.einstein-online.info/en/explandict/equivalence-principle/
- Einstein Online, "Gravity: from weightlessness to curvature": https://www.einstein-online.info/en/spotlight/geometry_force/

### 4. Bridge / connection between local inertial descriptions

If each local region has its own inertial description, comparing neighboring descriptions requires a transport rule.

Introduce a connection:

~~~text
D_a = partial_a + Gamma_a
~~~

where Gamma_a describes how a local state / frame is compared across the underlying relational space.

The important quantity is then not Gamma alone, but failure of successive transports to commute:

~~~text
Omega_ab = [D_a, D_b]
~~~

If:

~~~text
Omega_ab = 0
~~~

then a globally consistent inertial comparison may be possible over that region.

If:

~~~text
Omega_ab != 0
~~~

then transport depends on path / ordering, producing effective curvature.

The hypothesis identifies this nontrivial curvature with the structure that appears macroscopically as gravity.

### 5. Gravity as emergent relational curvature

The strongest current candidate statement is:

~~~text
Gravity
  != necessarily a fundamental force field

Gravity
  ~ curvature of the relational / inertial connection
    after coarse-graining into effective spacetime
~~~

This is deliberately compatible with the successful geometric content of general relativity.

It does not replace Einstein gravity unless the low-energy limit recovers the Einstein field equations.

### 6. Time and gravity as co-emergent structures

Rather than:

~~~text
fundamental time
+ fundamental gravity
~~~

the proposed hierarchy is:

~~~text
deeper relational structure
       |
       +--> persistence / inertia
       |
       +--> ordering / clock structure
       |         |
       |         +--> effective time
       |
       +--> local-frame comparison
                 |
                 +--> effective geometry
                           |
                           +--> effective gravity
~~~

Thus the current hypothesis is:

> **time and gravity are co-emergent manifestations of deeper relational-inertial structure.**

### 7. Role of the graviton

The hypothesis does **not** require a fundamental graviton.

However, it also does not imply that graviton-like excitations cannot exist.

A possible hierarchy is:

~~~text
fundamental relational degrees of freedom
        |
        v
coarse-grained effective geometry
        |
        v
small gravitational perturbation
        |
        v
quantized effective excitation
        |
        v
graviton-like mode
~~~

Therefore the distinguishable claims are:

~~~text
A. fundamental graviton exists
B. no fundamental graviton exists, but an effective spin-2 excitation emerges
C. no graviton-like quantum excitation exists
~~~

The current hypothesis favors investigating B, but does not yet establish it.

### 8. Candidate unified structure

A compact form is:

~~~text
Fundamental:
  (R, I, Delta, P, C)

Derived:
  tau      = TimeMap(R, I, Delta, ...)
  Gamma    = Connection(R, I, ...)
  Omega    = Curvature(Gamma)
  g_eff    = GeometryMap(Omega, ...)
  gravity  = EffectiveDynamics(g_eff, matter, ...)
~~~

The central derivation target is therefore:

~~~text
(R, I, Delta, P, C)
    ->
(tau, Gamma, Omega)
    ->
effective spacetime
    ->
general-relativistic limit
~~~

### 9. What would make this a real unified theory?

The hypothesis becomes physically serious only if it passes explicit tests.

At minimum it must:

1. recover local Lorentz symmetry to experimental accuracy,
2. recover the equivalence principle,
3. recover gravitational redshift and proper-time behavior,
4. recover geodesic motion,
5. recover tidal gravity / curvature,
6. recover the Einstein field equations or a quantitatively equivalent low-energy limit,
7. reproduce gravitational-wave propagation,
8. connect consistently to quantum theory,
9. explain how matter / gauge fields inhabit the same underlying relational system,
10. produce at least one falsifiable prediction not inserted by construction.

Failure of these requirements is evidence against the hypothesis.

### 10. Stronger falsification criteria

The hypothesis should be rejected or substantially revised if it cannot derive, without ad hoc insertion:

~~~text
universality of free fall
local Lorentz invariance
inverse-square Newtonian limit
observed gravitational redshift
light deflection
perihelion / orbital relativistic corrections
gravitational-wave speed and polarization constraints
known quantum interference results
known gauge symmetries / Standard Model structure
~~~

A framework that merely re-labels these known laws after inserting them manually is a representation language, not a unified physical theory.

### 11. Current status

The project should therefore describe the result as:

> **a candidate relational-inertia unification hypothesis embedded in the HexDoku / Unified Reconstruction Algebra, not a completed Theory of Everything.**

What has been achieved conceptually:

~~~text
time can be moved from input variable to reconstruction target
gravity can be represented as curvature of inter-frame comparison
local inertial nulling and global curvature can coexist
BridgeDoku can be interpreted as a connection
Doku non-commutativity can represent curvature
scale / coarse-graining can generate effective spacetime descriptions
a fundamental graviton is no longer logically mandatory
~~~

What remains open:

~~~text
derive the actual connection from microscopic rules
derive the effective metric
derive Einstein dynamics
derive quantum structure
derive matter and gauge sectors
establish uniqueness
produce new falsifiable predictions
compare quantitatively with observation
~~~

The correct current claim is therefore:

> **A plausible unification hypothesis may have emerged, but its status now depends entirely on derivation and falsification rather than further naming or analogy.**


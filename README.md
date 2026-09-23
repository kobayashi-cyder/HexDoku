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
- [Permutation / Address Compression](docs/PERMUTATION_ADDRESSING.md)
- [Canonical order and HexDoku Hamming Rank](docs/CANONICAL_ORDER.md)
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

HDC may be computationally expensive. HDE is intended to be deterministic, reproducible, and simpler to execute.

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

The first 24 transitions use a versioned deterministic resolver. Standard Sudoku row/column/box rules are **not required**.

The final coordinate is a **Terminal Reference**. Under the 8-bit-q terminal profile, its nine q values contribute 72 bits and a terminal-only 4-bit extension contributes another 4 bits, giving a **76-bit Terminal Selector (T76)**. The terminal extension is not HR; HR remains derived state. T76 can select one member of a versioned permutation family while the final **Parity** remains the fully materialized 81-cell table.

The 25-table evaluation trajectory is **DNA**. The completed 81-cell reference table is **Parity**.

See [DNA / Parity Model v0.2](docs/DNA_PARITY_SPEC.md).

---

## 76-bit Terminal Selector

For the 25th evaluation table, the current 8-bit-q profile defines:

~~~text
q1..q9 in fixed candidate order = 9 × 8 = 72 bits
Terminal Extension              = 4 bits
------------------------------------------------
T76                             = 76 bits
~~~

T76 is a **selector-width**, not automatically a claim of 76-bit cryptographic security.

Its nominal selector space is:

~~~text
2^76 = 75,557,863,725,914,323,419,136 states
~~~

For an 81-block universe, a rule may use T76 to choose up to 2^76 unique permutations from the much larger 81! permutation space. It does not encode all 81! permutations; the complete arbitrary 81-element permutation still requires about 401.17 bits of distinguishing information.

A canonical 13-symbol text form may use the Base64url alphabet as a **radix-64 integer alphabet**, with the first symbol restricted to 16 values. This is not standard byte-oriented Base64url encoding. Standard Base64url of a 10-byte container would require 14 unpadded characters.

See [Permutation / Address Compression](docs/PERMUTATION_ADDRESSING.md).

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

The current HexDoku model uses a 9×9 board as a deterministic coordinate topology. Standard Sudoku constraints are optional rather than normative. The fully materialized 81-cell final table is called **Parity**, while the 25-stage evaluation-table trajectory is called **DNA**.

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

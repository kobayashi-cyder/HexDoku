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
- [Architecture](docs/ARCHITECTURE.md)
- [Protocol draft](docs/PROTOCOL.md)
- [Project status and milestones](docs/STATUS.md)
- [Contributing](CONTRIBUTING.md)

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

## Solved Sudoku as parity / topology

The original HexDoku idea uses a **solved Sudoku board** not merely as a puzzle answer, but as a reusable structural object.

Possible roles include:

- parity placement
- deterministic routing
- connection topology
- reconstruction coefficients
- chunk-to-cell assignment
- redundancy layout
- ordering / addressing

The solved board is therefore treated as a **layout or reconstruction map**.

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
3. a solved 9×9 Sudoku board,
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

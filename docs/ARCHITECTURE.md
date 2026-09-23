# HexDoku Architecture

## 1. Purpose

HexDoku investigates whether a large state can be reproduced from a compact, versioned bootstrap description when participating nodes already share deterministic rules and some or all of the referenced data universe.

The central requirement is **exact reproducibility**.

## 2. Conceptual origin

The project began from the intuition:

> 「エピゲノムの逆って数独じゃないか？」

This is an engineering analogy, not a biological identity.

The useful contrast is:

- epigenome-inspired direction: state/marks influence which parts of an underlying information space are expressed;
- Sudoku-inspired direction: constraints and placements can determine a larger global configuration.

HexDoku explores the second pattern as a reconstruction primitive.

## 3. Components

### 3.1 Seed Cell

The Seed Cell is the smallest bootstrap object that should be sufficient to identify the reconstruction process.

Candidate fields:

```text
format_version
hexdoku_id
rule_version
generator_version
chunking_version
manifest_hash
chunk_hashes[]
rollback_reference?
parameters?
```

A Seed Cell must not silently depend on unspecified software state.

### 3.2 HexDoku layout

A solved Sudoku board provides a deterministic topology.

Example roles:

- ordering
- grouping
- routing
- parity placement
- dependency mapping
- chunk assignment

The mapping from board values/cells to implementation behavior must be versioned.

### 3.3 Data universe

The reconstructed object may depend on:

- locally cached chunks,
- shared content-addressed storage,
- deterministic generators,
- immutable reference artifacts.

These dependencies count as real storage. HexDoku must not label shared external bytes as “free” when reporting compression or storage efficiency.

### 3.4 Deterministic expander

The expander takes the Seed Cell, exact rule versions, and referenced data, and emits canonical bytes.

Any source of nondeterminism must be removed or explicitly captured:

- RNG seed
- locale
- timestamp
- file ordering
- floating-point mode
- library version
- architecture-dependent behavior

## 4. Invariants

A conforming implementation should aim for:

### I1 — Deterministic identity

```text
R(seed, rules, universe) = B
```

For any compatible implementation:

```text
R_A(seed, rules, universe) == R_B(seed, rules, universe)
```

byte for byte.

### I2 — Hash verification

Every fetched content-addressed chunk must verify against its expected digest before use.

### I3 — Version closure

A Seed Cell must identify enough version information to prevent two rule sets from interpreting the same identifier differently.

### I4 — No hash reconstruction fallacy

A cryptographic hash may identify or validate content. It cannot, in general, recover arbitrary unknown source bytes.

### I5 — Recovery honesty

If neither a verified rollback state nor the required source material exists, the implementation reports unrecoverable state and regenerates from an allowed source path.

## 5. Recovery model

Normal path:

```text
Seed
 -> resolve
 -> verify dependencies
 -> reconstruct
 -> verify root
 -> accept
```

Failure path:

```text
verification failure
 -> rollback to last known-good state
 -> reconstruct again
 -> verify
```

Terminal path:

```text
rollback unavailable
AND required source information unavailable
 -> mark state unrecoverable
 -> regenerate
```

## 6. Parity Genome

“Parity Genome” is a working term for using a completed HexDoku/Sudoku structure as a reusable parity/dependency map.

It may encode relationships such as:

```text
cell -> chunk
row  -> group
col  -> dependency family
box  -> redundancy family
digit -> transform/routing selector
```

This does not automatically create an error-correcting code. Error correction requires a defined code construction and measurable correction bounds.

## 7. Seed Cell hierarchy

A larger system may use multiple Seed Cells:

```text
Root Seed
├─ Seed A -> subsystem A
├─ Seed B -> subsystem B
└─ Seed C -> subsystem C
```

The parent may contain only child identifiers/hashes while children hold the detailed reconstruction manifests.

This makes hierarchical reconstruction possible without requiring the root object to contain every leaf reference directly.

## 8. Security boundary

Integrity and authenticity are different.

A hash can detect content mismatch if the expected digest is trusted.

For adversarial environments, a future protocol may additionally require:

- signed manifests
- trusted public keys
- replay protection
- version pinning
- domain separation

These are not assumed to exist until implemented.

## 9. First implementation target

The first implementation should optimize for auditability, not performance:

- fixed corpus
- fixed 9x9 solved board
- deterministic chunking
- SHA-256
- canonical serialization
- one Seed Cell schema
- one reconstruction algorithm
- byte equality tests

Only after this passes should more complex layouts or distributed execution be added.


## 10. Descriptor-only communication bus

HexDoku can separate the transport layer from semantic reconstruction.

A sender may transmit only:

```text
Seed Cell
HexDoku / board identifier
rule and generator versions
root / manifest hash
chunk references
residual bits or delta
```

Intermediate transport nodes may forward these descriptors without interpreting the final reconstructed application data.

The receiver resolves the descriptors, executes the pinned reconstruction procedure, and accepts the result only if it produces the required canonical bit string and verification hash.

A unique solution alone is not sufficient. The full path from solution to bytes must also be canonical and versioned.

## 11. Canonical parallel reconstruction

Substructures may be evaluated concurrently as long as the final ordering is independent of runtime completion order.

The HexDoku layout can assign every partial result a fixed logical position.

Therefore:

```text
physical execution order != logical serialization order
```

while still preserving:

```text
same Seed + same rules + same universe -> same final bytes
```

Probabilistic internal computation is allowed only when its accepted external output is determinized by fixed seeds, canonical selection, exact numerical rules, or final hash verification.

## 12. Arithmetic reconstruction and omitted bits

When one region of the final bit string is a deterministic arithmetic function of another region, only the independent information needs explicit representation.

The expander recreates omitted predictable bits from the versioned rule.

This can reduce the explicit Seed/residual representation for structured data.

It cannot remove incompressible independent information.

## 13. Asymmetric codec hypothesis

HexDoku intentionally permits a computationally expensive compressor and a simpler deterministic expander.

The compressor may search for:

- reusable shared chunks,
- deterministic generators,
- arithmetic dependencies,
- HexDoku layouts,
- compact residual descriptions,
- Seed Cell hierarchies.

The expander only needs to execute the selected versioned reconstruction recipe.

This creates a path to transfer ratios much higher than conventional self-contained ZIP archives on suitable workloads, particularly where decoder-side shared state is large.

Any claim of total storage compression must still count all decoder dependencies and shared data.

This ZIP comparison is currently a **testable design hypothesis, not a measured benchmark result**.

## 14. Obfuscation versus security

Increasing board size or structural complexity can make direct interpretation more difficult and may serve as an obfuscation layer.

It must not be described as cryptographic confidentiality.

Security-sensitive deployments should use authenticated encryption independently of HexDoku.

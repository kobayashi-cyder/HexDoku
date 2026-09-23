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


## HDC / HDE codec boundary

HexDoku names its two primary codec stages explicitly.

### HDC — HexDoku Compressor

HDC is the analysis and reduction stage.

Responsibilities may include:

- finding shared chunks;
- finding deterministic generators;
- identifying arithmetic dependencies;
- selecting a HexDoku layout;
- constructing Seed Cells;
- emitting residual bits;
- emitting hashes and references;
- choosing a versioned reconstruction recipe.

HDC is allowed to be computationally expensive.

### HDE — HexDoku Expander

HDE is the deterministic reconstruction stage.

Responsibilities include:

- resolving the exact rule versions;
- resolving required references;
- reconstructing omitted deterministic bits;
- applying canonical ordering;
- verifying chunk hashes;
- producing the final bit string;
- validating the final root hash.

HDE should have a much narrower behavior surface than HDC.

Normative target:

```text
HDE(HDC(X), U) = X
```

where U is the exact shared reconstruction universe required by the selected HexDoku version.

If U is unavailable or verification fails, HDE must fail rather than silently producing a different state.

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


## 15. Turn-state trajectory

For a board with 25 unresolved cells, the current model evaluates unresolved coordinates before one value is fixed per turn.

The evaluated cell count is:

```text
N = sum(n=1..25) n = 325
```

For each unresolved coordinate c at turn t, HDE computes a versioned candidate table:

```text
E(t,c) = [(digit 1, q1), ..., (digit 9, q9)]
```

where each q is converted to a canonical fixed-width numerical representation.

The ordering function, sorting direction, tie-break rule, rounding, saturation, and bit order are reconstruction-critical protocol state.

With 8-bit q values, each E(t,c) contributes 72 raw bits and the 25-turn trajectory contributes 23,400 raw bits before further reduction.

## 16. Immediate-value reuse

The canonical q values are allowed to become machine-level immediate bit material directly.

The same deterministic output may be reused as:

- hash material;
- content-address keys;
- bus payload words;
- Seed derivation material;
- arithmetic operands;
- table indexes.

The protocol does not require the transport intermediary to understand the semantic meaning of q.

## 17. Hamming address layer

Let B be one canonical 72-bit cell-state vector.

A derived vector is addressed by:

```text
(B, d, k)
```

where d is the Hamming distance and k is the canonical rank of one d-element subset of the 72 bit positions.

The decoder uses combinatorial unranking to obtain the exact flip mask.

No exhaustive list is required.

Across all d, the generated address space has 2^72 possible 72-bit vectors. This is a generated/addressable space, not additional independent information.

Different base states' Hamming spaces overlap and must not be summed as if they were disjoint information stores.

The detailed definition is in `docs/TRAJECTORY.md`.


## 18. HexDoku Hamming Rank and canonical order

HexDoku defines **Hamming Rank (HR)** as a project-specific unresolved-multiplicity rank:

```text
HR(t,c) = number_of_remaining_candidates(t,c) - 1
```

Thus HR is always in the range 0..8.

- HR0: one candidate remains; logically determined, including pending/unfilled commit state.
- HR8: all nine candidates remain; maximum unresolved multiplicity.

This is not standard Hamming distance.

For each pre-fix turn, all unresolved cells are ordered by:

```text
HR ascending
-> canonical candidate table lexicographic ascending
-> row-major coordinate ID ascending
```

The first coordinate in that order is the next commit position, with its digit determined by the versioned unique-solution rule.

Both HDC and HDE use this same logical order.

Parallel execution may calculate values in any physical order, but no state transition is committed until the complete turn has been canonically ordered.

The normative definition is in `docs/CANONICAL_ORDER.md`.

## 19. Optional standard Hamming-distance layer

Standard bitwise Hamming distance remains a separate optional mechanism for deriving/addressing a bit vector relative to a canonical base state.

To avoid ambiguity:

```text
HR = HexDoku unresolved-multiplicity rank (0..8)
HD = standard bitwise Hamming distance
CR = combination rank used with HD
```

HR is part of the primary HDC/HDE ordering. HD/CR is not required for the primary turn order.

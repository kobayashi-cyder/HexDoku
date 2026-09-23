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

HexDoku Core provides a deterministic coordinate topology. The first reference implementation, **Sudoku Profile v1**, uses a conventional 9×9 Sudoku board and ordinary row/column/3×3 constraints. Future profiles may use different payload-specific rules.

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

## 6. DNA and Parity

The current model separates the evolving evaluation trajectory from the final reference state.

~~~text
DNA    = P0 || P1 || ... || P24
Parity = fully materialized 81-cell final table
~~~

For 25 initial unresolved coordinates, DNA contains 25 evaluation tables with 325 total evaluated coordinate states.

There are 24 normal commits. The remaining final coordinate is a Terminal Reference whose content may be a canonical non-numeric value and is resolved or verified from the Parity reference/source.

Standard Sudoku row/column/3×3-box constraints are not required by the architecture. What is required is deterministic, versioned resolution and bit-identical reconstruction.

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
- fixed 9x9 HexDoku coordinate board
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


## 15. DNA turn-state trajectory

For 25 initially unresolved coordinates E0..E24, fixed once in row-major order:

~~~text
P0  evaluates E0..E24
P1  evaluates E1..E24
...
P23 evaluates E23..E24
P24 evaluates E24
~~~

This is 25 evaluation tables and 325 evaluated coordinate states.

P0..P23 are followed by 24 normal commits of E0..E23 using the versioned deterministic resolver.

P24 is the terminal stage. E24 is not required to become a digit; it is resolved or checked through the Terminal Reference / Parity source.

For every active coordinate c at stage t:

~~~text
Q(t,c) = [(1,q1),...,(9,q9)]
~~~

Canonical ordering inside Q is q ascending, then digit ascending on ties.

With 8-bit q values, the raw q-only DNA stream is 23,400 bits = 2,925 bytes.

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

HexDoku HR is a project-specific unresolved-multiplicity rank:

~~~text
HR = number_of_remaining_candidates - 1
~~~

with range 0..8.

HR is state metadata only. It never selects the next coordinate.

The coordinate sequence E0..E24 is fixed at initialization by row-major order of the 25 unresolved positions.

At stage t, Et is the normal commit target for t=0..23. E24 is the Terminal Reference at the final stage.

The detailed normative order is in docs/CANONICAL_ORDER.md.

## 19. Optional standard Hamming-distance layer

Standard bitwise Hamming distance remains a separate optional mechanism for deriving/addressing a bit vector relative to a canonical base state.

To avoid ambiguity:

```text
HR = HexDoku unresolved-multiplicity rank (0..8)
HD = standard bitwise Hamming distance
CR = combination rank used with HD
```

HR is part of the primary HDC/HDE ordering. HD/CR is not required for the primary turn order.


## 20. Permutation / address layer

HexDoku may represent the order of an already-known or content-addressable block universe.

Let:

~~~text
U = {B0, B1, ... , Bn-1}
~~~

be a shared set of blocks identified by stable IDs or hashes.

The final Parity may define a canonical permutation:

~~~text
Pi_D(U) = ordered sequence of block IDs
~~~

where D is the versioned HexDoku descriptor.

HDC may search for a compact D that reproduces the source order. HDE reconstructs the same Parity and therefore the same order.

The core invariant is:

~~~text
Pi_HDC(D,U) == Pi_HDE(D,U)
~~~

This compresses the **description of order/addressing**, not automatically the block bytes themselves.

For n distinct arbitrary blocks, the full permutation space contains n! states and requires at least log2(n!) bits to distinguish in the absence of additional structure. For n=81, log2(81!) is approximately 401.17 bits.

Compression below that general arbitrary-permutation bound requires shared state, restricted valid permutations, a nonuniform distribution, deterministic generation, delta state, or residual coding.

The detailed model is in `docs/PERMUTATION_ADDRESSING.md`.

## 21. Two-layer compression model

HexDoku may be combined with a conventional content codec:

~~~text
source
  -> content/block compression
  -> IDs/hashes
  -> HexDoku permutation/address compression
  -> compact descriptor
~~~

On decode:

~~~text
descriptor
  -> HexDoku order reconstruction
  -> ID/hash resolution
  -> content decompression
  -> original stream
~~~

Order-compression gain and content-compression gain must be benchmarked separately.


## 22. T76 terminal selector

Under the baseline 8-bit-q profile, the final P24 coordinate contributes a 72-bit q table:

~~~text
q1||q2||...||q9 = 72 bits
~~~

A terminal-only four-bit extension produces:

~~~text
T76 = 72-bit q table || 4-bit extension
~~~

The extension is not HR. HR may remain derived state, but constraining these four bits to HR0..HR8 would reduce the terminal selector domain.

T76 can act as a deterministic selector for a restricted family of block permutations.

For an 81-block universe, the architecture can map each T76 value to a distinct permutation because 81! is much larger than 2^76.

The architecture therefore distinguishes:

~~~text
full arbitrary 81-element permutation space : ~401.17 bits
T76-selected permutation family             : 76-bit selector
~~~

The second is a subset selected under shared/versioned context, not universal compression of all 81! possible orders.

## 23. T76 is not cryptographic strength by definition

A 76-bit field has 2^76 possible bit patterns, but field width is not automatically entropy or security strength.

The evaluator may generate fewer reachable patterns.

Even with a uniform secret T76, exhaustive search is bounded by 2^76, below a 128-bit modern cryptographic target.

Cryptographic confidentiality/authentication remains the responsibility of separately specified standard primitives.

## 24. Rule-profile layering

HexDoku separates the stable Core from versioned rule profiles.

~~~text
HexDoku Core
  -> coordinate/order machinery
  -> DNA/Parity serialization
  -> HDC/HDE equality
  -> versioning / verification

Sudoku Profile v1
  -> digits 1..9
  -> row/column/3×3 legality
  -> deterministic q distribution
  -> validity-preserving commits
  -> Sudoku ParityGrid

Future Payload Profile
  -> payload-specific alphabet/rules
  -> block/hash permutation
  -> terminal selector or sidecar
~~~

The first benchmark MUST use Sudoku Profile v1 so later payload-specific improvements can be measured against a fixed baseline.

## 25. Sudoku v1 terminal boundary

In Sudoku Profile v1, the final 72 q bits are derived from Sudoku state and are not independent payload capacity.

The structural four-bit terminal extension is reserved as zero in v1.

Therefore full T76 selector-capacity claims are deferred to a future Payload Profile.

This separation prevents payload engineering from being mistaken for compression generated by the Sudoku trajectory itself.

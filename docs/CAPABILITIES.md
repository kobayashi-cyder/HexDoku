# What HexDoku Can Do

HexDoku is not mainly about compressing arbitrary unknown data beyond information-theoretic limits.

Its practical target is different:

> **Reduce the amount of new information that must be stored, transmitted, or synchronized when both sides already share rules, data, or history.**

## In short

HexDoku can be used to describe a large reproducible state with a much smaller **Seed Cell**, provided that the receiver already has access to the required reconstruction rules and shared data universe.

That makes the architecture potentially useful for:

- compact state synchronization
- distributed caches
- reproducible checkpoints
- model or agent state exchange
- deterministic artifact reconstruction
- partial data transfer
- rollback and regeneration
- content-addressed storage
- sparse updates between nodes

## 1. Send a state by sending its identity

If two nodes already share most of the same data, HexDoku does not need to resend the entire object.

Instead, a sender can transmit something closer to:

```text
Seed Cell
+ HexDoku ID
+ rule version
+ manifest/root hash
+ missing chunk references
```

The receiver resolves that description into the full state.

This can make the **network transfer size** dramatically smaller than the reconstructed object.

## 2. Reconstruct the same object deterministically

Given the same:

- Seed Cell
- rules
- versions
- referenced data
- canonical ordering

two compatible implementations should produce identical bytes.

This allows:

- reproducible builds
- state replication
- checkpoint reconstruction
- deterministic agent state
- cross-node verification

The target is:

```text
reconstruct(seed, universe) == original bytes
```

## 3. Transfer only what changed or is missing

A node can compare the requested chunk hashes with its local cache.

Already-known chunks require no transfer.

Only missing pieces are requested.

```text
requested state
      |
      v
compare hashes
   /      \
known    missing
 |          |
reuse      fetch
   \      /
    reconstruct
```

This means HexDoku can behave as a **sparse synchronization layer** rather than a conventional archive format.

## 4. Use shared knowledge as part of reconstruction

Suppose a 1 GB object is almost entirely derivable from data already stored by both sides.

The sender does not need to communicate that shared information again.

Only the information necessary to select or modify the shared state must cross the network.

In that situation, the apparent transfer ratio can become extremely large.

This is not magic compression.

The information still exists in:

```text
Seed Cell
+ shared universe
+ reconstruction rules
```

HexDoku's advantage is avoiding repeated transfer of information that is already known.

## 5. Content-oblivious communication bus

One proposed use is to make the transport layer carry only **HexDoku descriptors** rather than the reconstructed payload itself.

A communication bus may exchange:

```text
HexDoku ID / board ID
Seed Cell
rule/version identifier
root hash
chunk hashes or references
optional delta
```

Intermediate relays can forward those descriptors without understanding the application-level reconstructed content, provided that routing does not require the plaintext.

```text
sender
  |
  | Seed / HexDoku / hashes
  v
relay ---- relay ---- relay
  |
  | descriptors only
  v
receiver
  |
  v
unique reconstruction
  |
  v
canonical bit string
```

The receiver performs the semantic reconstruction.

This separates **transport of identity/reconstruction instructions** from **interpretation of the reconstructed data**.

It can reduce the amount of payload that must traverse the bus when sender and receiver already share the required reconstruction universe.

### Obfuscation boundary

A larger or more complex HexDoku board may make casual interpretation harder by increasing structural complexity.

However, this is **obfuscation, not cryptographic security**.

If confidentiality is required, HexDoku should be combined with conventional authenticated encryption rather than relying on board size or puzzle complexity.

## 6. Unique solution as a bit-string identifier

If a HexDoku rule set guarantees exactly one valid solution, and if the mapping

```text
solution -> canonical ordered cells -> canonical bit string
```

is also unique, then the solution can identify exactly one bit sequence.

The chain becomes:

```text
Seed / constraints
      |
      v
unique solution
      |
      v
canonical ordering
      |
      v
unique bit string
```

The important requirement is not merely that the puzzle has a solution, but that:

1. the solution is unique;
2. the serialization order is unique;
3. every transform is versioned;
4. every implementation produces the same bits.

If those conditions hold, the board can operate as a deterministic state selector.

## 7. Parallel computation without ordering ambiguity

HexDoku can also define independent subproblems that are evaluated in parallel.

Parallel execution is safe for deterministic reconstruction when the rule set defines a single canonical final order.

```text
Seed
 |
 +--> worker A --+
 +--> worker B --+--> canonical merge --> unique bit string
 +--> worker C --+
 +--> worker D --+
```

Workers may finish in any physical order.

The final bit sequence remains identical if the merge order is defined by the HexDoku solution rather than by completion timing.

This allows physical parallelism without making logical ordering ambiguous.

## 8. Probabilistic computation with deterministic output

A probabilistic or stochastic calculator can only participate in exact HexDoku reconstruction if its final externally visible result is made deterministic.

Possible approaches include:

- fixing all random seeds;
- fixing the algorithm/version;
- fixing numerical precision and rounding;
- enumerating candidates and selecting by a canonical rule;
- verifying the final output against a required hash.

The internal search may be probabilistic while the accepted output must still collapse to one canonical bit sequence.

```text
probabilistic search
      |
      v
candidate results
      |
      v
canonical selection + verification
      |
      v
one accepted bit string
```

Without this final uniqueness condition, bit-perfect reconstruction is not guaranteed.

## 9. Arithmetic omission of predictable bits

If parts of a bit sequence are mathematically derivable from other parts, the derivable bits do not have to be stored or transmitted explicitly.

Conceptually:

```text
explicit bits + arithmetic rule -> omitted predictable bits
```

or:

```text
short description
      |
      v
deterministic arithmetic expansion
      |
      v
longer exact bit string
```

This is genuine reduction of the **explicit representation** when the source contains exploitable structure.

It does not reduce the information content of incompressible random data.

HexDoku can use the solved board to define where these arithmetic or dependency relationships apply.

## HDC and HDE

The asymmetric codec is formally named:

### HDC — HexDoku Compressor

Input:

```text
source bytes
shared universe
HexDoku rules
```

Output:

```text
Seed Cell
HexDoku / board identifiers
rule and generator versions
hashes / references
arithmetic reconstruction description
residual bits
```

HDC may perform expensive analysis or search in order to minimize the explicit representation.

### HDE — HexDoku Expander

Input:

```text
Seed Cell
references
residual bits
pinned HexDoku rules
shared universe
```

Output:

```text
one canonical reconstructed bit string
```

HDE must not guess. For a valid input, it should either reconstruct the exact canonical output or fail verification.

The intended relation is:

```text
HDE(HDC(X), shared_universe) == X
```

for every supported source state X under the same versioned reconstruction universe.

## 10. Separate compressor and expander

A HexDoku codec can deliberately separate the two sides.

### Compressor

The compressor analyzes a source state and searches for a compact description:

```text
source bytes
   |
   v
structure / shared-state analysis
   |
   v
HexDoku mapping
   |
   v
Seed Cell + references + residual bits
```

### Expander

The expander does not need to repeat that search.

It receives the compact description and executes the pinned reconstruction procedure:

```text
Seed Cell + references + residual bits
   |
   v
versioned HexDoku rules
   |
   v
deterministic expansion
   |
   v
original bytes
```

This asymmetry is intentional.

Compression may be computationally expensive while decompression remains relatively simple and deterministic.

## 11. When can HexDoku exceed ZIP?

HexDoku can potentially achieve a **far higher transfer or compact-description ratio than ZIP** when it exploits information that ZIP does not assume is already available to the decoder, such as:

- a shared content-addressed store;
- a fixed deterministic generator;
- a large common model or corpus;
- previous checkpoints;
- repeated structures;
- mathematically derivable regions;
- reusable HexDoku layouts;
- a persistent Seed Cell hierarchy.

For example:

```text
ZIP:
source -> self-contained compressed stream -> source

HexDoku:
source -> Seed + rule references + residual information
                         |
                         + shared decoder universe
                         |
                         v
                       source
```

Under those conditions, the transmitted HexDoku description can be orders of magnitude smaller than a conventional self-contained archive.

This is the design hypothesis behind using a **Seed Cell + generation method** as the compact representation.

### Important qualification

This does **not** mean that HexDoku can universally beat ZIP for every arbitrary file.

A fair total-storage comparison must count:

```text
Seed Cell
+ residual bits
+ reconstruction program
+ rule tables
+ shared dictionaries/corpora
+ referenced chunks
+ any persistent external state required by the decoder
```

For completely new, random, incompressible data, HexDoku cannot remove the need to communicate essentially that information.

The strongest advantage is expected when:

```text
shared / derivable information >> genuinely new information
```

## 12. Represent large generated objects with small seeds

If an object is generated deterministically, its Seed Cell can remain small even when the generated output becomes very large.

For example:

```text
small seed
   |
   v
deterministic generator
   |
   v
large object
```

In such cases, the apparent ratio between Seed Cell size and generated output can be enormous and has no fixed finite upper bound.

The real accounting must still include the generator and any shared source data.

## 13. Build hierarchical state

Seed Cells can reference other Seed Cells.

```text
Root Seed
├── Model Seed
├── Cache Seed
├── Memory Seed
└── Environment Seed
```

This makes it possible to describe a large system as a tree of independently verifiable sub-states.

A changed subsystem can be replaced without necessarily retransmitting the others.

## 14. Potential AI / agent use

For AI systems or autonomous agents, HexDoku could be tested as a representation for:

- model-associated state
- tool state
- agent memory snapshots
- shared knowledge caches
- reproducible execution environments
- checkpoint trees
- multi-agent synchronization

For example, if two agents share the same base state, only a compact description of their divergence may need to be exchanged.

## 15. What determines the real benefit?

The strongest benefit appears when:

```text
shared information >> new information
```

The weakest case is random, previously unknown data.

If every byte is new and unpredictable, HexDoku cannot avoid transmitting nearly all of that information.

So the useful measure is not simply:

```text
original size / seed size
```

but also:

```text
new information that must be transferred
-----------------------------------------
full reconstructed state
```

and, for total-storage claims:

```text
full reconstructed state
----------------------------------------------
Seed + residual + decoder + all shared storage
```

## 16. Practical interpretation

HexDoku can be thought of as combining ideas from:

- deterministic generation
- content addressing
- deduplication
- manifests
- sparse synchronization
- checkpointing
- constraint-based topology
- asymmetric compression/decompression
- canonical parallel reconstruction

into one versioned reconstruction model.

The long-term question is not:

> “Can HexDoku compress every file infinitely?”

It is:

> **“How little genuinely new information must compatible systems exchange to reproduce exactly the same canonical bit string?”**

That is the central capability HexDoku is intended to test.


## 17. DNA / Parity trajectory

With 25 initial unresolved coordinates, HexDoku uses 25 canonical evaluation tables:

~~~text
25, 24, 23, ... , 2, 1 active coordinates
~~~

This gives 325 evaluated coordinate states.

There are only 24 normal commits. The last active coordinate is a Terminal Reference.

The 25-table evaluation history is **DNA**. The fully materialized final 81-cell table is **Parity**.

Standard Sudoku solving constraints are not required. The required property is deterministic, versioned reconstruction.

With nine 8-bit q values per evaluated coordinate:

~~~text
325 × 9 × 8 = 23,400 bits = 2,925 bytes
~~~

before HCT, prediction, delta, or entropy coding.

## 18. Fixed coordinate order

The initial 25 unresolved coordinates are fixed once in row-major order:

~~~text
top -> bottom
left -> right within each row
~~~

This gives E0..E24.

At stage t, active coordinates are Et..E24.

HR does not choose the coordinate.

## 19. Hamming Rank

HexDoku HR is:

~~~text
HR = unresolved candidate multiplicity - 1
~~~

with range 0..8.

HR0 includes a logically determined but still-unfilled coordinate.

HR8 is maximum unresolved multiplicity.

HR is state metadata; it does not define the board traversal.

## 20. HCT / most-frequent-value prepass

HDC may scan the complete canonical DNA q stream before encoding it.

It builds the HCT by frequency descending and q-value ascending on ties.

This fixes the most-frequent value before payload encoding.

HDE must either receive the HCT first or regenerate it exactly from shared state.

This enables frequency coding without a circular decoder dependency.

## 21. Terminal Reference

The final E24 coordinate does not have to be a digit.

It may hold a canonical typed number, character, byte string, reference, ID, Seed reference, or other protocol symbol.

Its final content is resolved or checked against the Parity reference/source.

## 22. Cryptographic interpretation

The public board geometry, coordinate order, and algorithm version need not be secret.

If confidentiality is required, HexDoku should use standard cryptographic primitives in a separately specified keyed profile.

The relevant security question is how much uncertainty about the final Parity remains after a defined subset of coordinates/tables is revealed.

HexDoku v0.2 does not claim proven cryptographic security.

See [DNA / Parity Model v0.2](DNA_PARITY_SPEC.md).

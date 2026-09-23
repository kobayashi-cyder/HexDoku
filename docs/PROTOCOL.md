# HexDoku Protocol Draft

Status: **Draft / experimental**

## 1. Objective

Define the minimum exchange required for two compatible nodes to agree on and reconstruct the same byte sequence.

## 2. Sender message

A minimal transmission may contain:

```json
{
  "format_version": "0",
  "hexdoku_id": "example-id",
  "rule_version": "0",
  "manifest_hash": "<digest>",
  "required_chunks": [
    "<digest-1>",
    "<digest-2>"
  ]
}
```

Exact serialization and field names are not yet frozen.

## 3. Receiver procedure

The receiver should:

1. validate the message schema;
2. resolve the HexDoku ID;
3. load the exact rule version;
4. resolve the manifest;
5. compare required chunk hashes with local content;
6. fetch only missing chunks;
7. verify every fetched chunk;
8. run deterministic reconstruction;
9. calculate the final root hash;
10. accept only if the expected and actual result match.

## 4. Hash role

Hashes are used for:

- content addressing
- deduplication lookup
- integrity verification
- manifest identity

Hashes are **not** treated as reversible encodings of arbitrary source data.

## 5. Missing data

For each missing chunk:

```text
if local(hash):
    use local chunk
else if remote(hash):
    fetch -> verify -> use
else:
    fail reconstruction
```

A failed lookup is not repaired from the digest alone.

## 6. Rollback

If the reconstructed state fails verification:

```text
if known_good_checkpoint:
    rollback
    reconstruct
else:
    declare unrecoverable
    regenerate
```

The system should never silently continue with an unverified state.

## 7. Canonicalization

Interoperability requires canonical definitions for:

- integer encoding
- byte order
- text encoding
- JSON or binary serialization
- chunk ordering
- board indexing
- hash algorithm
- hash domain
- generator seed
- rule version

## 8. HexDoku board addressing

A baseline 9x9 board has 81 deterministic addresses:

```text
r1c1 ... r1c9
...
r9c1 ... r9c9
```

A rule version may map these addresses to chunk groups, dependencies, transforms, or parity positions.

The exact mapping belongs to the rule set, not to informal implementation behavior.

## 9. Compatibility

Two nodes are compatible only when all reconstruction-critical versions match or a defined migration exists.

A future compatibility tuple may be:

```text
(format, rules, chunking, generator, hashing, canonicalization)
```

## 10. Validation

Protocol tests should include:

- complete local cache
- partial cache
- empty cache
- corrupted chunk
- wrong rule version
- wrong manifest
- missing chunk
- reordered chunks
- rollback available
- rollback unavailable
- cross-implementation byte equality


## 11. DNA trajectory

For the 25-unresolved-coordinate profile, first create the immutable row-major unresolved-coordinate list:

~~~text
E0..E24
~~~

The protocol then defines 25 evaluation tables:

~~~text
P0  = E0..E24
P1  = E1..E24
...
P23 = E23..E24
P24 = E24
~~~

For each active coordinate:

1. calculate candidates 1..9 using the versioned evaluator;
2. apply canonical numeric encoding;
3. rank candidate entries by q ascending, then digit ascending;
4. derive HR if required;
5. append q values to the canonical DNA stream.

After P0..P23, commit Et using the versioned deterministic resolver.

After P24, E24 is resolved or checked through the Terminal Reference / Parity source and is not required to be a digit.

This produces 325 evaluated coordinate states.

### 11.1 HexDoku Hamming Rank

~~~text
HR = unresolved candidate multiplicity - 1
~~~

Range: 0..8.

HR does not choose or reorder the next coordinate.

If explicitly serialized, HR uses 4 bits. If it is exactly recomputable, it should be omitted.

### 11.2 HCT header

If the compressed payload uses a frequency-derived HexDoku Canonical Table (HCT), HDC must determine it in a prepass.

Canonical HCT ordering:

~~~text
frequency descending
-> q numeric value ascending on ties
~~~

HDE must obtain the HCT before decoding any HCT-coded payload.

The HCT may be omitted only when it is deterministically regenerable from already shared state.

### 11.3 Terminal Reference / T76

For the baseline 8-bit-q terminal profile, P24 packs:

~~~text
q1..q9 in candidate identity order = 72 bits
terminal_extension                = 4 bits
T76                               = 76 bits
~~~

The terminal extension is not HR.

T76 may select a Parity/permutation entry under a versioned mapping. Its field capacity is 2^76 states, but actual entropy may be lower if the q evaluator cannot reach every 72-bit pattern.

A terminal text representation must be explicitly identified. The canonical compact 13-symbol form uses the Base64url alphabet as radix-64 integer digits and is not standard byte-oriented Base64url.

A hash can validate a known Parity but does not by itself recover unknown Parity bytes.

## 12. Optional standard Hamming-distance address record

Standard bitwise Hamming distance is written HD and is distinct from HexDoku HR.

If an optional derived-bit address is used, a record may contain:

~~~text
stage_id
coordinate_id
hd_distance
combination_rank_cr
rule_version
optional verification bits
~~~

HD/CR does not affect E0..E24 coordinate order.

## 13. Information accounting

Generated Hamming address space is not counted as independently compressed source information.

Benchmarks must distinguish:

- bits explicitly transmitted;
- bits regenerated deterministically;
- shared decoder state;
- address-space size;
- actual independent source information represented.


## 14. Permutation / address reconstruction

A permutation profile may define a block universe by stable IDs/hashes and use final Parity cells as canonical ordering references.

A logical descriptor may contain:

~~~text
hexdoku_id
rule_version
seed/reference
block_universe_id or manifest_hash
residual_order_data
parity/root verification hash
~~~

HDE procedure:

1. resolve the exact block universe/manifest;
2. reconstruct the DNA/Parity state;
3. map Parity cells to canonical block IDs;
4. apply any residual order data;
5. resolve blocks by ID/hash;
6. concatenate them in canonical order;
7. verify the final object digest.

A missing block cannot be reconstructed from its hash alone.

The protocol must distinguish:

- bytes needed to identify the permutation;
- bytes needed to identify/retrieve blocks;
- bytes used for residual order information;
- bytes used for the block contents themselves.

For arbitrary n-element permutations, compression claims must be compared with the information requirement `log2(n!)`, not only with a naive fixed-width ID list.


## 15. T76 permutation-selector record

A permutation profile may include or derive:

~~~text
terminal_selector_t76 : 76 bits
permutation_rule_version
universe_id / manifest_hash
context_rank_version
~~~

For an n-element universe with n! >= 2^76:

~~~text
s      = UInt76(T76)
N      = n!
offset = ContextRank(context) mod N
rank   = (offset + s) mod N
order  = FactoradicUnrank(n, rank)
~~~

For n=81, all T76 values can select distinct orders for a fixed context.

The receiver must reject:

- wrong T76 width;
- noncanonical terminal text;
- incompatible permutation-rule version;
- wrong universe identity;
- a mapping that is ambiguous for the selected profile;
- final object hash mismatch.

T76 is an address/selector field. A protocol requiring modern cryptographic confidentiality must use a separately specified standard cryptographic primitive.

## 16. Compression-reporting profile

A T76 benchmark must declare the baseline representation.

Required fields in a benchmark report:

~~~text
element_count
baseline_id_width_bits
baseline_order_bits
t76_bits = 76
seed_bytes_transmitted
rule_profile_bytes_transmitted
universe_reference_bytes_transmitted
residual_bytes_transmitted
verification_auth_bytes_transmitted
shared_context_bytes
full_descriptor_bytes
~~~

For a naive 25-element explicit ordering:

~~~text
baseline_order_bits = 25 × baseline_id_width_bits
~~~

Example reductions when all non-order context is already shared:

~~~text
5-bit IDs   : 125  -> 76 bits = 39.20%
32-bit IDs  : 800  -> 76 bits = 90.50%
64-bit IDs  : 1600 -> 76 bits = 95.25%
256-bit IDs : 6400 -> 76 bits = 98.81%
~~~

The protocol must not report those values as total-object compression unless the block universe and block contents are intentionally excluded and that exclusion is clearly stated.

For comparison with optimal permutation coding, a 25-element arbitrary permutation has 25! states and needs approximately 83.68 bits of information. T76 does not cover all of that state space.

## 17. Reference rule profile negotiation

The first protocol profile is:

~~~text
rule_profile = sudoku-v1
~~~

Both HDC and HDE must load the exact Sudoku Profile v1 rules before generating or consuming the 25-stage trajectory.

The profile fixes:

- 9×9 board geometry;
- symbols 1..9;
- ordinary row/column/3×3 Sudoku constraints;
- candidate-set derivation;
- integer q-distribution calculation;
- HR derivation;
- target coordinate schedule E0..E24;
- validity-preserving commit resolver;
- final Sudoku ParityGrid verification.

A future payload profile must use a different profile identifier.

## 18. Terminal field in sudoku-v1

For `sudoku-v1`:

~~~text
Q72  = deterministic Sudoku-derived final q vector
ext4 = 0000
T76  = Q72 || 0000
~~~

T76 is not an independently selectable 76-bit payload in this profile.

Any protocol that uses T76 as a free permutation selector must negotiate a future Payload Profile explicitly.

## 19. HDC-Lite mask profile

Reference profile identifier:

~~~text
sudoku-v1/hdc-lite-9-9-7-v1
~~~

Baseline mask rule:

~~~text
all digit-1 cells are holes
all digit-2 cells are holes
seven digit-3 cells are holes
two digit-3 cells remain visible
~~~

The nine digit-3 coordinates are ordered row-major and the visible pair is combination-ranked into `mask_rank` 0..35.

Wire field:

~~~text
mask_rank: 6 bits
~~~

Values 36..63 are invalid.

The six-bit rank identifies the hole pattern only. It does not encode the unknown completed Sudoku board.

The decoder reconstructs using Sudoku Profile v1 and must not repeat the encoder mask search.

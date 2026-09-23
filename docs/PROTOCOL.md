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

### 11.3 Terminal Reference

The terminal field must specify an unambiguous type/length or a deterministic reference scheme.

The terminal value may be non-numeric.

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

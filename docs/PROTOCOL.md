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


## 11. Turn trajectory fields

A rule version may define a 25-turn pre-fix evaluation trajectory.

For each turn:

1. enumerate currently unresolved coordinates in canonical order;
2. calculate candidate values for digits 1 through 9;
3. apply canonical numeric encoding;
4. apply canonical sort/tie-break rules when the protocol uses ranked candidate tables;
5. emit or reuse the resulting immediate bit vectors;
6. fix exactly one cell according to the rule;
7. continue to the next turn.

For 25 initial unresolved cells, this yields 325 evaluated cell states.

## 12. Hamming address record

When a derived bit vector is referenced relative to a canonical 72-bit base state, a compact logical record may contain:

```text
turn_id
cell_index
hamming_distance
combination_rank
rule_version
optional verification bits
```

If turn and cell are already implied by the state machine, they may be omitted.

The combination rank is interpreted only under the exact versioned combinatorial ranking convention.

The receiver:

1. recreates the canonical base state with HDE;
2. un-ranks the selected combination of bit positions;
3. flips exactly those positions;
4. obtains the exact derived bit vector;
5. optionally verifies it by hash or check value.

The protocol must never require exhaustive Hamming enumeration to resolve a single address.

## 13. Information accounting

Generated Hamming address space is not counted as independently compressed source information.

Benchmarks must distinguish:

- bits explicitly transmitted;
- bits regenerated deterministically;
- shared decoder state;
- address-space size;
- actual independent source information represented.

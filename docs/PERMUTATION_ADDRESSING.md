# Permutation / Address Compression

Status: **Draft / experimental**

HexDoku can be used as a deterministic **permutation/address description layer** for an already-known or content-addressable set of blocks.

This is distinct from compressing the block contents themselves.

## 1. Basic model

Assume both endpoints can already identify the same set of blocks:

~~~text
B0, B1, B2, ... , Bn-1
~~~

Each block may be identified by:

- a content hash;
- a stable object ID;
- a chunk ID;
- a shared-store reference;
- another canonical identifier.

The remaining information may be the order in which those blocks must be assembled.

Instead of transmitting an explicit permutation such as:

~~~text
B17, B4, B71, B2, ...
~~~

HexDoku may transmit or regenerate a smaller descriptor:

~~~text
HexDoku ID
+ rule version
+ Seed / DNA information
+ residual ordering information
~~~

HDE reconstructs the same Parity and derives the same block order.

## 2. Parity as an ordering map

The final 81-cell Parity may act as a canonical ordering/address map.

A versioned mapping defines how a Parity cell refers to a block ID or hash-table entry.

Conceptually:

~~~text
shared block set
      |
      v
hash / object IDs
      |
      v
HexDoku DNA + resolver
      |
      v
81-cell Parity
      |
      v
canonical ID permutation
      |
      v
ordered block stream
~~~

The Parity does not need to contain the block bytes themselves.

It may contain or derive references to them.

## 3. HDC role

HDC may:

1. split source data into blocks;
2. assign or calculate canonical block IDs/hashes;
3. determine the source block order;
4. search for a HexDoku Seed/rule/Parity representation that reproduces that order;
5. emit only the descriptor and any residual order information that cannot be regenerated.

Conceptually:

~~~text
source bit stream
   |
   v
chunk / block decomposition
   |
   v
content IDs / hashes
   |
   v
target permutation
   |
   v
HexDoku representation search
   |
   v
Seed + rule + residual order data
~~~

## 4. HDE role

HDE may:

1. receive the compact HexDoku descriptor;
2. recreate the 25-table DNA trajectory when required;
3. materialize or verify the final Parity;
4. convert Parity cells to block IDs;
5. resolve those IDs from the shared/content-addressed universe;
6. concatenate blocks in the reconstructed canonical order;
7. verify the final object hash.

~~~text
Seed + rules + residuals
   |
   v
HexDoku DNA / Parity
   |
   v
canonical block permutation
   |
   v
hash / ID lookup
   |
   v
ordered blocks
   |
   v
reconstructed bit stream
~~~

## 5. What is actually compressed

The primary target is:

~~~text
explicit permutation / address sequence
->
compact deterministic description of that permutation
~~~

HexDoku therefore acts first as a:

> **Permutation / Address Compressor**

It can be combined with a conventional content compressor:

~~~text
content compression
+
HexDoku order/address compression
~~~

These two gains must be measured separately.

## 6. Information-theoretic boundary

For n distinct elements, an arbitrary permutation has n! possible states.

The information needed to distinguish all of them is at least:

~~~text
log2(n!) bits
~~~

For 81 distinct elements:

~~~text
log2(81!) ≈ 401.17 bits
~~~

Therefore an arbitrary 81-element permutation cannot universally be represented losslessly by fewer than about 402 fixed bits unless additional shared information, constraints, nonuniform probability, or external state is used.

HexDoku can reduce explicit permutation bytes when one or more of the following is true:

- only a restricted subset of permutations is valid;
- the receiver shares a deterministic generator;
- the ordering distribution is strongly nonuniform;
- a previous ordering is available for delta coding;
- much of the order is implied by Parity/DNA rules;
- only residual exceptions need transmission.

A fair compression claim must count every required Seed, rule, table, dictionary, shared-store dependency, and residual.

## 7. Hash role

Hashes are appropriate for:

- block identity;
- content addressing;
- deduplication;
- final verification.

A hash does not reveal the underlying block bytes by itself.

Therefore HexDoku ordering works best when the receiver already possesses or can retrieve the block associated with each hash/ID.

## 8. Canonical ordering invariant

For a block universe U and versioned HexDoku descriptor D:

~~~text
Order_HDC(D, U) == Order_HDE(D, U)
~~~

and after block resolution:

~~~text
concat(Order_HDE(D,U)) == original bit stream
~~~

for a valid lossless representation.

## 9. Interaction with DNA / Parity

The 25-stage DNA trajectory may act as the deterministic state process that selects or constructs the final Parity.

The final Parity then acts as the ordering/address map.

~~~text
25-table DNA
     |
     v
24 normal transitions
     |
     v
Terminal Reference
     |
     v
Parity
     |
     v
ID permutation
     |
     v
ordered bit-block collection
~~~

This makes the DNA trajectory and the final Parity part of the ordering codec rather than requiring the Parity to be a conventional Sudoku solution.

## 10. Secondary compression benefit

A useful ordering may also improve downstream compression.

For example, if Parity places similar blocks or related hashes near one another, later stages may obtain better:

- delta coding;
- prefix sharing;
- dictionary reuse;
- entropy coding;
- run-length coding;
- cache locality.

That secondary gain must be benchmarked rather than assumed.

## 11. Benchmark metrics

A permutation/address benchmark should report at least:

- number of blocks;
- raw explicit permutation bytes;
- HexDoku descriptor bytes;
- residual ordering bytes;
- Seed/rule/HCT bytes;
- shared-state bytes required;
- encode/search time;
- decode time;
- exact-order reconstruction success;
- final object hash equality.

Compression ratio should be reported both with and without shared-state accounting.


## 12. T76 selector profile

A future Payload Profile may expose a 76-bit Terminal Selector:

~~~text
T76 = q1||q2||...||q9||ext4
      72 q bits       4 bits
~~~

The q fields use fixed candidate identity order 1..9 for T76 packing. `ext4` is a terminal extension nibble, not HR.

If all 76 bits are genuinely free in that future profile, the nominal selector domain contains:

~~~text
2^76 = 75,557,863,725,914,323,419,136 values
~~~

The field width must not be confused with measured entropy. If q generation only reaches a subset of 72-bit patterns, the effective selector entropy is smaller.

## 13. Mapping T76 to an 81-element order

For 81 distinct blocks, define:

~~~text
N = 81!
s = UInt76(T76)
~~~

A simple deterministic mapping is:

~~~text
offset = ContextRank(context) mod N
rank   = (offset + s) mod N
order  = FactoradicUnrank(81, rank)
~~~

where context includes the exact rule version, Seed/DNA context, and block-universe identity.

Because:

~~~text
2^76 < 81!
~~~

distinct s values remain distinct permutation ranks for a fixed context.

Therefore one context can expose up to 2^76 unique 81-block orders selected by T76.

This is not the whole 81! space. The full arbitrary 81-element order still carries approximately 401.17 bits of permutation information.

## 14. Minimum universe size for a full T76 selector

To map all 2^76 selector values injectively to permutations, n must satisfy:

~~~text
n! >= 2^76
~~~

23! is smaller than 2^76, while 24! is larger.

Therefore a full 76-bit permutation selector first fits at n=24.

For smaller n, the selector must either use fewer effective bits or map multiple T76 values to the same order, in which case it is not a unique 76-bit permutation selector.

## 15. Thirteen-character display

T76 may be rendered as 13 characters with a custom fixed-width radix-64 representation using the Base64url alphabet.

This is a display/transport encoding of a 76-bit integer, **not standard Base64url over a byte string**.

Canonical 13-symbol form:

- exactly 13 characters;
- Base64url alphabet;
- big-endian radix-64 integer digits;
- first character restricted to alphabet indices 0..15.

If interoperability requires standard Base64url bytes, store T76 in a canonical 10-byte container and use 14 unpadded Base64url characters.

## 16. Cryptographic boundary

A 76-bit selector is not equivalent to 128-bit cryptographic security.

If T76 is secret and uniformly distributed, it exposes at most a 2^76 brute-force selector space.

HexDoku should use established cryptographic primitives for confidentiality and authentication. T76 can participate as a selector or derived field, but should not be treated as a standalone modern encryption key.

## 17. Compression accounting examples

T76 is most useful when the block universe and rule context are already shared and only the ordering choice must be communicated.

For 25 distinct elements, a naive explicit list has the following sizes:

| Explicit representation | Raw order bits | T76 selector | Reduction |
|---|---:|---:|---:|
| 25 local IDs at 5 bits each | 125 | 76 | 39.20% |
| 25 IDs at 32 bits each | 800 | 76 | 90.50% |
| 25 IDs at 64 bits each | 1,600 | 76 | 95.25% |
| 25 SHA-256-style 256-bit identifiers | 6,400 | 76 | 98.81% |

The reduction formula is:

~~~text
reduction = 1 - 76 / baseline_bits
~~~

These are **ordering-description reductions**, not claims that the underlying block contents or hashes have disappeared.

If the 25 identifiers themselves must also be transmitted because the receiver does not already know the universe, their bytes must be added back.

## 18. Comparison with an optimal permutation rank

A list of 25 distinct items has:

~~~text
25! possible complete permutations
log2(25!) ≈ 83.68 bits
~~~

An optimal fixed-width rank capable of representing **every** 25-item permutation therefore requires 84 bits.

T76 is smaller only because it covers at most 2^76 orders, not all 25!.

It is invalid to claim that 84 -> 76 bits is lossless compression of the complete 25! permutation universe.

The correct comparison is:

~~~text
full arbitrary 25-item order:
    25! states -> at least ~83.68 bits

T76 family:
    at most 2^76 states -> exactly 76 selector bits
~~~

Within a full 2^76-size T76 family, the 76-bit selector itself is already optimal before protocol overhead.

## 19. Complete descriptor accounting

In a favorable persistent session, the receiver may already know the block-universe/manifest ID, Seed and DNA context, permutation-rule version, Factoradic/ContextRank convention, and verification policy.

Then the incremental order message can approach:

~~~text
76 bits
~~~

In a self-contained or cold-start transfer, the real size is:

~~~text
76-bit T76
+ Seed
+ rule/profile version
+ universe/manifest reference
+ residuals
+ integrity/authentication material
~~~

Therefore every benchmark must publish two ratios:

1. **incremental order ratio** — shared context excluded but explicitly declared;
2. **full descriptor ratio** — every required descriptor byte included.

## 20. Interpretation

The strongest HexDoku permutation-compression case is:

~~~text
same block set on both sides
+ same rule/Seed context
+ only order differs
~~~

In that case, a verbose sequence of IDs/hashes can be replaced by a 76-bit selector if the target order belongs to the negotiated T76 family.

The weaker case is a cold receiver with none of the block universe or context. In that case, T76 alone is insufficient and the apparent percentage reduction can disappear after all required data is counted.

## 21. Profile status

The T76 permutation-selector construction in this document is a **future Payload Profile design**, not the active Sudoku Profile v1 terminal semantics.

In `sudoku-v1`:

~~~text
Q72 = derived from Sudoku state
ext4 = 0000
free T76 payload entropy = not claimed
~~~

Therefore the 39.20%, 90.50%, 95.25%, and 98.81% examples are conditional order-description examples for a future profile in which a free selector is actually available and the relevant universe/context is already shared.

The first empirical HexDoku compression result must instead come from the measured Sudoku-v1 DNA trajectory.

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

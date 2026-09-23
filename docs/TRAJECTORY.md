# Turn Trajectory, Hamming Rank, and Optional Hamming Addressing

Status: **Draft / experimental**

This document defines the current interpretation of HexDoku's 25-turn reconstruction trajectory.

## 1. Twenty-five remaining turns

Assume a 9×9 board has 25 unresolved cells.

Exactly one cell becomes fixed per turn.

HexDoku evaluates the unresolved state **before the fixation of that turn**, so the number of evaluated unresolved cells is:

```text
Turn  1: 25 cells
Turn  2: 24 cells
Turn  3: 23 cells
...
Turn 24:  2 cells
Turn 25:  1 cell
```

Therefore the trajectory contains:

```text
25 + 24 + ... + 1 = 325
```

unresolved-cell evaluation states.

## 2. Per-cell candidate-value table

For every unresolved coordinate, HDE deterministically evaluates candidates 1 through 9.

Conceptually:

```text
coordinate r,c

1 -> value/probability q1
2 -> value/probability q2
3 -> value/probability q3
...
9 -> value/probability q9
```

If each finalized numerical value is represented with 8 bits, one unresolved-cell evaluation contains:

```text
9 × 8 = 72 bits
```

of candidate-value output before any additional compression or omission.

The numerical representation, scaling, rounding and saturation rules must be versioned.

## 3. Canonical evaluation order

The same logical state must always generate the same bit sequence.

A rule version therefore fixes:

1. turn order;
2. unresolved-coordinate order;
3. candidate-number order or probability-sorted order;
4. tie-breaking rule;
5. numeric quantization;
6. byte/bit order.

If the values are sorted by ascending evaluated probability/value, the digit identity must travel with the value or be recoverable by the canonical ranking rule.

Example:

```text
digit:value
6:1
9:3
2:4
8:5
4:8
7:11
1:15
5:22
3:31
```

The ordered table is deterministic only if equal values have a fixed tie-break, for example by digit number.

## 3A. HexDoku Hamming Rank

For every unresolved coordinate, HexDoku assigns a project-specific Hamming Rank:

```text
HR = number of still-unresolved candidate digits - 1
```

The range is 0 through 8.

```text
HR0 -> one candidate remains; logically determined, possibly still unfilled
HR1 -> two candidates remain
...
HR8 -> nine candidates remain; maximum unresolved multiplicity
```

This HR is the primary ordering rank for compression and expansion.

It is not the standard bitwise Hamming distance.

Within each turn, unresolved cells are canonically ordered by:

```text
HR ascending
-> Canonical Candidate Table lexicographic ascending
-> coordinate ID ascending
```

See `CANONICAL_ORDER.md` for the normative ordering rule.

## 4. Canonical trajectory bit string

With 25 pre-fix turns and 8-bit values:

```text
325 evaluated cell states
× 9 candidate values
× 8 bits
= 23,400 bits
= 2,925 bytes
```

This is the raw candidate-value trajectory only.

Coordinates do not need to be explicitly stored if turn state and coordinate traversal are themselves deterministic. If coordinates are explicitly encoded, their cost must be counted separately.

The canonical trajectory is:

```text
Seed / initial board
        |
        v
Turn 1 evaluation of 25 unresolved cells
        |
        v
fix exactly one cell
        |
        v
Turn 2 evaluation of 24 unresolved cells
        |
       ...
        |
        v
Turn 25 evaluation of 1 unresolved cell
        |
        v
canonical trajectory bit string
```

## 5. Numerical result as an immediate bit value

The finalized evaluated numbers are not merely metadata.

Once their representation is canonical, their bits may be reused directly as:

- immediate values;
- hash input;
- table keys;
- Seed material;
- bus words;
- arithmetic operands;
- next-stage deterministic state.

Conceptually:

```text
HDE numerical evaluation
        |
        v
fixed-width canonical representation
        |
        v
immediate bit vector
```

No separate semantic translation is required between the evaluated number and its canonical bit representation.

## 6. Optional standard Hamming-distance addressing

Separately from HexDoku HR, a 72-bit cell-state vector B may optionally be used with the **standard bitwise Hamming distance (HD)**. A vector at HD=d differs in exactly d bit positions.

The number of vectors at distance d is:

```text
C(72, d)
```

Rather than materializing all candidates, HexDoku can identify one candidate with:

```text
(base state B, standard Hamming distance HD=d, combination rank CR=k)
```

where:

```text
0 <= k < C(72, d)
```

A deterministic combinatorial unranking function converts (d, k) into the exact set of bit positions to flip.

Thus:

```text
B + d + k
    |
    v
combination unrank
    |
    v
exact flip positions
    |
    v
one exact 72-bit derived value
```

This is intended as **direct addressing**, not literal exhaustive enumeration.

## 7. Optional standard Hamming space

Across all Hamming distances:

```text
sum(d=0..72) C(72,d) = 2^72
```

Therefore one 72-bit base state defines an addressable Hamming space containing every possible 72-bit vector.

If fully materialized, that enumeration would contain:

```text
72 × 2^72 bits
```

of output.

HexDoku does not need to materialize it. The purpose of the Hamming representation is to address an exact derived vector directly.

Multiple base states can define multiple address contexts, but their Hamming spaces overlap; they must not be counted as independent information merely because each base can enumerate 2^72 vectors.

## 8. Bus reuse

A bus message may therefore identify a value by compact reconstruction coordinates such as:

```text
Seed / state ID
turn ID
cell position or canonical cell index
Hamming distance
combination rank
rule version
verification fragment
```

The receiver can recreate the same base 72-bit state with HDE and then derive the exact requested bit vector.

If the base state is already implied by the Seed and current turn, it need not be transmitted again.

## 9. Separation of generated address space and information

This distinction is mandatory:

> A small Seed plus deterministic Hamming rules can generate or address a very large bit space, but it does not contain that many bits of independent unknown information.

HexDoku's potential advantage is in avoiding transmission of deterministic, shared, or derivable information.

For incompressible new information, the required independent bits still have to enter the system somewhere.

## 10. HDC / HDE role

HDC may search for a compact representation in terms of:

- initial Seed;
- canonical turn trajectory;
- table/ranking reuse;
- predictable candidate values;
- Hamming distance;
- combination rank;
- residual bits.

HDE reproduces the trajectory in exactly the same order and reconstructs the selected immediate bit vectors.

Target invariant:

```text
same Seed
+ same board state
+ same rule version
+ same numeric rules
+ same turn/fix order
+ same HexDoku HR and, when used, same HD/CR address
=
same canonical bit vector
```

This deterministic equality is the basis for using the generated values as bus immediates, hashes, references, or reconstruction operands.

# HexDoku DNA Trajectory

Status: **Draft / experimental**

This document defines the 25-table DNA trajectory.

See [DNA_PARITY_SPEC.md](DNA_PARITY_SPEC.md) for the complete model.

## 1. Shape of the trajectory

Begin with 25 unresolved coordinates E0..E24 fixed once in row-major order.

~~~text
P0  : 25 coordinates
P1  : 24
P2  : 23
...
P23 : 2
P24 : 1
~~~

Total evaluated coordinate states:

~~~text
25 + 24 + ... + 1 = 325
~~~

There are 25 evaluation tables but only 24 normal commits.

The last coordinate E24 is a Terminal Reference.

## 2. Table calculation

For every active coordinate c at stage t:

~~~text
Q(t,c) = [(1,q1),...,(9,q9)]
~~~

Candidate values are computed deterministically.

Canonical ranked order is:

~~~text
q ascending -> digit ascending on ties
~~~

If q uses 8 bits:

~~~text
325 × 9 × 8 = 23,400 bits
= 2,925 bytes
~~~

for the raw q-only DNA stream.

## 3. Coordinate order

Coordinates are never chosen by HR.

The original 25 unresolved coordinates are fixed as E0..E24 using:

~~~text
top -> bottom
left -> right within each row
~~~

At stage t, active coordinates are simply:

~~~text
Et, Et+1, ... E24
~~~

## 4. State transitions

After P0..P23:

~~~text
commit Et using the versioned deterministic resolver
~~~

Then recompute the next table from the new state.

After P24, do not require a conventional numeric commit for E24.

Under the 8-bit-q terminal profile:

~~~text
Qbits24 = q1||q2||...||q9 = 72 bits
T76     = Qbits24 || ext4  = 76 bits
~~~

where q values are packed in fixed candidate identity order 1..9 and ext4 is a terminal-only nibble, not HR.

T76 may then select the terminal Parity/permutation context.

## 5. HR

~~~text
HR = unresolved candidate multiplicity - 1
~~~

HR0 means logically determined even if the coordinate is still unfilled.

HR8 means maximum unresolved multiplicity.

HR is state metadata and does not alter E-order.

## 6. DNA bit stream

~~~text
P0[E0..E24]
||
P1[E1..E24]
||
...
||
P24[E24]
~~~

Coordinates and stage boundaries can be implicit under a fixed 25-coordinate profile.

If HDE can recompute HR and candidate permutation exactly, those fields can also be omitted from the transmitted representation.

## 7. HCT compression prepass

HDC may inspect all 2,925 8-bit q symbols first.

The HCT is then ordered by:

~~~text
frequency descending
-> q ascending on ties
~~~

The most frequent q value is therefore known before encoding.

HDE must receive the HCT first or regenerate it independently from shared deterministic state.

This avoids a circular dependency.

## 8. Immediate-bit reuse

Canonical q values can be reused directly as immediate machine values, hash input, lookup-table indexes, Seed derivation material, bus payload fields, or prediction/delta bases.

## 9. Optional standard Hamming addressing

Standard bitwise Hamming distance (HD) and combination rank (CR) may still be defined as a secondary derived-bit addressing layer.

They are not HexDoku HR and do not determine the 25-stage trajectory.

## 10. Equality target

~~~text
Q_HDC(t,c) == Q_HDE(t,c)
for every active t,c
~~~

The final 81-cell Parity must also match bit-for-bit.


## 11. Terminal selector capacity

T76 has a nominal address space of 2^76 values.

For an 81-element block universe, a versioned injective mapping can assign each T76 value to a distinct permutation because:

~~~text
2^76 < 81!
~~~

The full 81! permutation space remains much larger and is not represented by T76 alone.

Actual selector entropy can be less than 76 bits if the terminal q evaluator cannot generate every 72-bit q pattern.

# Canonical Order v0.2

Status: **Draft / experimental**

This document defines the deterministic ordering shared by HDC and HDE.

The normative DNA/Parity model is described in [DNA_PARITY_SPEC.md](DNA_PARITY_SPEC.md).

## 1. Initial unresolved-coordinate order

At initialization, identify the 25 unresolved coordinates and order them strictly by board position:

~~~text
row 1: left -> right
row 2: left -> right
...
row 9: left -> right
~~~

This produces:

~~~text
E0, E1, ... E24
~~~

The sequence is immutable for that trajectory.

HR, candidate values, runtime scheduling, and Sudoku heuristics do not reorder E.

## 2. Twenty-five tables / twenty-four normal commits

~~~text
P0: E0..E24   (25 coordinates)
P1: E1..E24   (24)
...
P23: E23..E24 (2)
P24: E24      (1)
~~~

After P0..P23, Et is the normal commit coordinate.

P24 is the terminal stage. E24 is resolved from the Terminal Reference / Parity source rather than being required to become a digit.

Therefore:

~~~text
25 canonical evaluation tables
24 normal commit transitions
1 terminal reference resolution
325 evaluated coordinate states
~~~

## 3. Per-coordinate evaluation order

For every active coordinate, evaluate the baseline candidate symbols in fixed order:

~~~text
1,2,3,4,5,6,7,8,9
~~~

For canonical ranking/serialization inside that coordinate, order entries by:

~~~text
1. q ascending
2. digit ascending on equal q
~~~

## 4. HexDoku Hamming Rank

~~~text
HR = unresolved candidate multiplicity - 1
~~~

Range: 0..8.

HR describes state only.

**HR never selects or reorders the next board coordinate.**

The next normal commit coordinate is Et, fixed by the initial row-major unresolved-coordinate sequence.

## 5. Normal value resolution

At P0..P23:

~~~text
target coordinate = Et
target value = Resolve(rule_version, t, Et, state, Q(t,Et))
~~~

Resolve must return exactly one canonical result for every valid input.

Standard Sudoku solving rules are not required.

## 6. Terminal resolution

At P24:

~~~text
target coordinate = E24
~~~

E24 is the Terminal Reference coordinate.

For the 8-bit-q terminal profile:

~~~text
Qbits24 = Encode8(q1)||...||Encode8(q9)  # fixed digit order 1..9
T76     = Qbits24 || terminal_extension4
~~~

In the generic research container the four-bit extension may be versioned separately. In **Sudoku Profile v1** it is fixed to `0000` and is not HR.

Under Sudoku Profile v1, T76 is a derived terminal word and not a free permutation selector. A future Payload Profile may reinterpret a terminal field under a new version.

## 7. DNA serialization order

~~~text
stage first
  -> active coordinates in E order
    -> canonical candidate/value order
~~~

Therefore:

~~~text
P0[E0], P0[E1], ... P0[E24],
P1[E1], ... P1[E24],
...
P24[E24]
~~~

Physical parallelism may be used internally, but results must be restored to this canonical logical order before serialization, hashing, or state transition.

## 8. HCT order

If HDC constructs a frequency table over quantized q values:

~~~text
frequency descending
-> q numeric value ascending on ties
~~~

This defines HCT symbol order.

HCT must be available to HDE before any HCT-coded payload is decoded.

## 9. Strong invariants

For all active (t,c):

~~~text
Q_HDC(t,c) == Q_HDE(t,c)
~~~

For HR-bearing states:

~~~text
HR_HDC(t,c) == HR_HDE(t,c)
~~~

At P24:

~~~text
T76_HDC == T76_HDE
~~~

For t=0..23:

~~~text
Resolve_HDC(t) == Resolve_HDE(t)
~~~

And finally:

~~~text
Parity_HDC == Parity_HDE
~~~

## 10. Standard Hamming distance

Standard bitwise Hamming distance is separate terminology:

~~~text
HR = HexDoku unresolved-multiplicity rank 0..8
HD = standard bitwise Hamming distance
CR = optional combination rank used with HD
~~~

HD/CR is an optional addressing layer and is not part of coordinate selection.

## 11. Sudoku Profile v1 binding

For the first reference implementation, canonical order is evaluated under `sudoku-v1`.

At every active coordinate:

~~~text
Candidates = locally legal Sudoku digits
HR = |Candidates| - 1
q = deterministic integer distribution from SUDOKU_PROFILE_V1.md
~~~

The scheduled target remains Et; Sudoku scores and HR never reorder E0..E24.

At P24, the final Q72 is Sudoku-derived and the terminal extension is `0000`.

A future Payload Profile may define another terminal rule, but that rule must use a new profile/version.

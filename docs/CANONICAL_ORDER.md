# Canonical Order v0.1

Status: **Draft / experimental**

This document defines the current deterministic ordering rule shared by HDC and HDE.

## 1. HexDoku Hamming Rank (HR)

HexDoku defines a project-specific **Hamming Rank (HR)** in the range 0 through 8.

This is **not the standard Hamming distance** between two bit strings.

For an unresolved coordinate c at turn t, let C(t,c) be the set of candidate digits still treated as unresolved by the current rule state.

```text
HR(t,c) = |C(t,c)| - 1
```

Therefore:

| HR | Remaining candidate multiplicity | Meaning |
|---:|---:|---|
| 0 | 1 | logically determined; may still be unfilled/pending commit |
| 1 | 2 | two candidates remain |
| 2 | 3 | three candidates remain |
| 3 | 4 | four candidates remain |
| 4 | 5 | five candidates remain |
| 5 | 6 | six candidates remain |
| 6 | 7 | seven candidates remain |
| 7 | 8 | eight candidates remain |
| 8 | 9 | maximum unresolved multiplicity |

HR therefore expresses **unresolved multiplicity**, from already-determined-but-not-yet-written through maximally unresolved.

If HR is serialized explicitly, the baseline representation is 4 bits:

```text
0000 -> HR0
...
1000 -> HR8
1001..1110 -> reserved
1111 -> invalid/error
```

When HR can be recomputed exactly from the canonical state, it does not need to be transmitted.

## 2. Pre-fix turn state

With 25 unresolved cells, one cell is committed per turn.

Before each commit, HDE evaluates every still-unfilled coordinate.

```text
Turn 1: 25 cells
Turn 2: 24 cells
...
Turn 25: 1 cell
```

The complete pre-fix trajectory therefore contains 325 evaluated cell states.

A cell may have HR0 before it is physically written to the board. Logical determination and board commit are separate states.

## 3. Candidate-value table

For each unresolved coordinate, HDC/HDE compute the canonical values for digits 1 through 9.

Example:

```text
1 -> q1
2 -> q2
...
9 -> q9
```

The numeric format, precision, rounding, saturation, and evaluation formula are part of the rule version.

If q is represented as an 8-bit immediate, a full nine-value table contributes 72 raw value bits before further coding.

## 4. Candidate ordering inside a cell

Candidate entries are ordered by:

```text
1. evaluated numeric value ascending
2. digit ascending as tie-break
```

Thus equal evaluated values never create an ordering ambiguity.

The resulting ordered list is called the **Canonical Candidate Table (CCT)** for that cell and turn.

## 5. Calculation-position order inside a turn

The **calculation-position order is fixed by board geometry and never by HR**.

Coordinates are scanned row-major:

```text
r1c1 -> r1c2 -> ... -> r1c9
  -> r2c1 -> r2c2 -> ... -> r2c9
  -> ...
  -> r9c1 -> ... -> r9c9
```

Equivalent coordinate IDs are:

```text
r1c1 = 0
r1c2 = 1
...
r1c9 = 8
r2c1 = 9
...
r9c9 = 80
```

Already-filled cells are skipped, but their positions remain part of the fixed board coordinate system.

Therefore every turn calculates unresolved cells in exactly the same geometric sequence:

```text
top row: left -> right
then next row
...
bottom row: left -> right
```

This **calculation order** is distinct from later commit/compression priority.

## 5A. Commit / compression priority after calculation

Only after all unresolved coordinates for the turn have been calculated in row-major order may the implementation derive a priority key for commit or compression decisions.

Current draft priority:

```text
1. HR ascending
2. CCT lexicographic ascending
3. coordinate ID ascending
```

Thus HR does not reorder the calculation scan. It ranks already-calculated cell states for the next deterministic action.

## 6. Commit order

The first coordinate in the post-calculation commit-priority order is the next coordinate to commit.

Its committed digit must be the digit selected by the versioned unique-solution rule.

The commit operation is separate from the pre-fix evaluation.

After the commit:

1. update the board state;
2. advance the turn;
3. recompute candidate tables and HR values for the remaining coordinates;
4. repeat until no unresolved coordinates remain.

This means the canonical order is state-dependent but reproducible.

## 7. HDC order

HDC must serialize or describe source state in exactly the same logical trajectory:

```text
initial board / Seed
  ->
pre-fix evaluation
  ->
HR calculation
  ->
CCT construction
  ->
canonical cell sort
  ->
selected commit
  ->
next turn
```

HDC may search or optimize in parallel, but its emitted representation must correspond to this canonical order.

## 8. HDE order

HDE reconstructs with the same order, not a runtime-dependent order:

```text
Seed / compact representation
  ->
same pre-fix evaluation
  ->
same HR
  ->
same CCT
  ->
same cell ordering
  ->
same commit
  ->
same next state
```

Target invariant at every turn:

```text
HR_HDC(t,c)  == HR_HDE(t,c)
CCT_HDC(t,c) == CCT_HDE(t,c)
Order_HDC(t) == Order_HDE(t)
State_HDC(t) == State_HDE(t)
```

The final invariant remains:

```text
HDE(HDC(X), U) = X
```

for the same versioned reconstruction universe U.

## 9. Parallel execution

Physical execution order is not logical order.

Workers may evaluate coordinates or candidate values concurrently. Results are buffered and committed only after canonical keys are available.

```text
row-major logical scan
       |
       v
parallel workers may calculate internally
       |
       v
collect results tagged by fixed coordinate ID
       |
       v
HR + CCT commit-priority sort
       |
       v
one deterministic commit
```

This prevents CPU/GPU scheduling differences from changing the reconstructed bit sequence.

## 10. Relation to standard Hamming distance

Earlier drafts used standard bitwise Hamming distance and combination rank as a direct-address mechanism over a 72-bit state.

That mechanism, if retained, is now an **optional secondary addressing layer** and is named explicitly:

```text
HD = standard bitwise Hamming distance
CR = combination rank
```

It must not be called HexDoku Hamming Rank.

The primary HexDoku ordering quantity is:

```text
HR = unresolved candidate multiplicity - 1
```

This distinction is normative from Canonical Order v0.1 onward.

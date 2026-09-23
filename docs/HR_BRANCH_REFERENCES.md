# HR Branch Reference Channel

Status: **Draft / experimental**

This document defines how HexDoku Hamming Rank (HR) may expose deterministic branch-reference slots.

## 1. HR and branch count

HexDoku HR is:

~~~text
HR = candidate_count - 1
~~~

For a coordinate with HR = h:

~~~text
candidate_count = h + 1
~~~

If every candidate carries a reference, the coordinate has `h + 1` reference slots.

If one canonical candidate is implicit and only alternative branches carry references, the coordinate has:

~~~text
branch_reference_slots = HR = h
~~~

The second form is the reference baseline because it avoids storing a reference for the branch already implied by the canonical resolver.

## 2. Canonical anchor branch

For every HR-bearing coordinate, one candidate is the **anchor branch**.

The anchor must be determined entirely by the negotiated rule/profile. It is not transmitted.

For Sudoku Profile v1, the reference anchor is the first candidate that the normal deterministic resolver would accept under the current state and tie-break rules.

All remaining legal candidates are alternative branches.

Alternative branches are ordered canonically by the profile's candidate ordering/tie-break rule.

Therefore:

~~~text
HR0 -> 1 candidate -> 0 alternative-reference slots
HR1 -> 2 candidates -> 1 alternative-reference slot
HR2 -> 3 candidates -> 2 alternative-reference slots
...
HR8 -> 9 candidates -> 8 alternative-reference slots
~~~

## 3. What a reference may contain

An alternative branch slot may carry or derive a stable reference such as:

- content hash;
- object/chunk ID;
- manifest index;
- Seed/reference ID;
- short table index into a separately shared reference dictionary.

A hash is an identifier/integrity check, not a reversible encoding of unknown bytes.

If the referenced content is not already shared or retrievable, its bytes must be transmitted separately and counted.

## 4. Target-only channel

The smallest operational scope attaches branch references only to the scheduled target coordinate at each stage.

For the 25 target evaluations:

~~~text
B_target = sum_t HR(t, E_t)
~~~

where the terminal-stage treatment is profile-defined.

If only the 24 normal commits are used:

~~~text
B_commit = sum_{t=0..23} HR(t, E_t)
~~~

`B_target` or `B_commit` is the number of alternative-branch reference slots, not the number of independent payload bits.

## 5. Full-DNA channel

A wider research mode may attach branch references to every evaluated coordinate state in the 25-stage DNA trajectory:

~~~text
B_DNA = sum_t sum_{c in active(t)} HR(t,c)
~~~

There are 325 evaluated coordinate states in the current 25-hole profile.

Since each HR is at most 8, the structural absolute upper bound is:

~~~text
B_DNA <= 325 × 8 = 2,600 alternative-reference slots
~~~

This 2,600 figure is a structural slot bound only. Sudoku Profile v1 normally has much smaller candidate multiplicities, and repeated/derived slots are not automatically independent information.

## 6. 9+9+7 consequence

In the fixed HDC-Lite 9+9+7 profile, the intended hole values are limited to digits 1, 2, and 3 while digits 4..9 remain visible.

When Sudoku legality reduces every active hole to a subset of `{1,2,3}`, candidate count is at most 3 and:

~~~text
HR <= 2
~~~

Under that condition the full-DNA structural bound becomes:

~~~text
B_DNA <= 325 × 2 = 650 alternative-reference slots
~~~

This is still only a bound. Actual `sum(HR)` must be measured from generated trajectories.

## 7. Reference-width accounting

If every alternative slot uses a fixed `w`-bit reference index, raw side-reference width is:

~~~text
reference_bits = B × w
~~~

where B is the selected target-only, commit-only, or full-DNA slot count.

For full cryptographic hashes, use the actual digest width. For dictionary indexes, include the referenced dictionary/manifest in total-storage accounting unless it is already shared.

## 8. Information-capacity caution

`sum(HR)` counts branch-reference positions. It does not by itself prove `sum(HR) × w` bits of independent payload capacity.

Independent capacity depends on how many branch/reference assignments HDC can actually choose while preserving:

- a valid Sudoku trajectory;
- deterministic HDE reconstruction;
- exact final Parity;
- all verification constraints.

If only K complete assignments are reachable, the independent information capacity is at most:

~~~text
log2(K) bits
~~~

regardless of the raw number of slots.

## 9. HDE behavior

HDE must be able to regenerate:

1. the candidate set;
2. HR;
3. the anchor branch;
4. the canonical order of alternative branches;
5. the slot-to-reference mapping rule.

Therefore HR itself and branch positions need not be transmitted when they are exactly derivable from the received 25-hole Sudoku board and the pinned profile.

## 10. Current benchmark requirements

For every tested 9×9 / 25-hole board, record:

- `sum_hr_targets`;
- `sum_hr_commits`;
- `sum_hr_dna`;
- HR histogram 0..8;
- number of distinct branch-reference slots after deduplication;
- reference dictionary size;
- raw reference bits;
- compressed reference bits;
- number K of reachable complete branch/reference assignments where measurable;
- `log2(K)` as the actual independent branch-channel capacity estimate;
- HDE instruction/operation count needed to regenerate the same slot ordering.

These measurements separate structural slot count from real information capacity.
## 11. 500-board measured HR structure

In the 500-board fixed `9+9+7` corpus, 3,780 masks reconstructed their source Parity exactly.

Target-stage HR over those accepted masks:

~~~text
HR0 = 86,101
HR1 =  8,399
sum(HR_target) per accepted mask:
  min  = 1
  mean = 2.22196
  max  = 7
~~~

Full-DNA HR over the 325 evaluated states:

~~~text
HR0 = 241,908
HR1 = 621,408
HR2 = 365,184
sum(HR_DNA) per accepted mask:
  min  = 258
  mean = 357.61270
  max  = 467
~~~

Thus the measured structure offers many deterministic **reference positions**, especially in the full-DNA view. These counts remain structural slot counts. They do not establish hundreds of independent payload bits because branch states and references may be correlated, repeated, or derivable.

See [ORDER_HR_CORPUS_500.md](ORDER_HR_CORPUS_500.md).

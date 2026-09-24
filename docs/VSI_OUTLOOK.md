# VSI Outlook — Visual Screen Indicator as a Future Human-Facing HexDoku Layer

## Status

**Speculative research outlook / not part of the HexDoku core protocol.**

This document records a possible future direction for HexDoku: using a compact deterministic state description to drive a **nonverbal visual indicator layer** for human perception.

VSI here means **Visual Screen Indicator**.

VSI is not defined as a treatment for Visual Snow Syndrome (VSS), and this document does not claim that visual snow is an acquired information-display ability. Current VSS research supports abnormal or altered visual processing, but the mechanism remains incompletely understood.

---

## 1. Core idea

HexDoku currently focuses on deterministic reconstruction:

```text
compact state / Seed Cell
        |
        v
deterministic rules
        |
        v
reconstructed canonical state
```

VSI adds a possible human-facing output layer:

```text
HexDoku state
    |
    v
VSI encoder
    |
    v
visual modulation primitives
    |
    v
human nonverbal perception
```

The goal is not to display large amounts of text.

The goal is to encode a small number of high-value state changes into visual features that can be perceived rapidly without serial verbal interpretation.

Examples of possible visual primitives:

- motion direction
- local density
- contrast
- flicker rate
- spatial position
- coherence
- expansion / contraction
- phase change
- boundary strength
- short-lived local synchronization

A VSI should preferably remain visually quiet when nothing important has changed.

---

## 2. Why HexDoku may fit this problem

HexDoku already separates:

1. a compact identifier or Seed Cell,
2. deterministic reconstruction rules,
3. canonical ordering,
4. verification.

The same structure could be reused for human-readable nonverbal output.

A canonical VSI mapping could be versioned:

```text
state_id
rule_version
vsi_profile
visual_symbol_id
spatial_address
temporal_parameters
verification / expected response class
```

Instead of sending the full semantic state to the display layer, the system could send a small visual descriptor.

Conceptually:

```text
large internal state
      |
      v
HexDoku reduction / selection
      |
      v
small VSI descriptor
      |
      v
visual field event
```

This makes VSI closer to an **attention-routing layer** than a conventional screen.

---

## 3. Relation to visual snow

Visual snow should not be assumed to be meaningful information.

A safer working model is:

```text
perceived visual field =
external visual input
+ spontaneous / internally generated activity
+ adaptation effects
+ noise
```

The research question is whether some perceptual dimensions can be **reliably modulated and decoded**.

Relevant evidence exists that visual snow can be altered by visual adaptation.

A 2023 study reported that adaptation to high-contrast dynamic noise temporarily reduced visual snow strength, in many participants to the point that it became temporarily invisible.

A 2025 study reported that visual snow itself can exhibit a motion aftereffect after adaptation to drifting gratings; 10 of 11 VSS participants reported motion in the expected opposite direction.

These results do **not** establish a VSI channel.

They do support a narrower proposition:

> at least some properties of the visual-snow percept interact with ordinary visual adaptation and motion-processing mechanisms.

That makes controllable modulation a testable question rather than a purely metaphysical one.

---

## 4. VSI should use modulation, not raw noise

The useful carrier is not "random snow itself."

A simple model is:

```text
S(x,y,t) = B(x,y,t) + M(x,y,t) + e(x,y,t)
```

where:

- `B` = background spontaneous activity,
- `M` = reproducibly controllable modulation,
- `e` = uncontrolled variability / noise.

Only `M` is useful for a VSI.

Therefore the first target should be a small number of robust visual transformations such as:

```text
leftward coherence
rightward coherence
radial expansion
radial contraction
local density rise
local density fall
brief synchronized pulse
stable spatial hotspot
```

The system should prefer sparse, distinctive changes over continuous stimulation.

---

## 5. HexDoku-to-VSI mapping

A future profile could define a deterministic map:

```text
HexDoku symbol
    -> VSI primitive
```

Example only:

| HexDoku state class | VSI primitive |
| --- | --- |
| 0 | no event |
| 1 | leftward coherent motion |
| 2 | rightward coherent motion |
| 3 | expansion |
| 4 | contraction |
| 5 | local density increase |
| 6 | local density decrease |
| 7 | short synchronized pulse |

A larger alphabet can be built compositionally:

```text
symbol =
spatial_address
+ motion_class
+ intensity_bin
+ duration_bin
+ temporal_phase
```

The mapping must be versioned and deterministic.

The important property is not aesthetic quality.

It is **decodability**.

---

## 6. Human information-channel formulation

A VSI becomes useful only when a state can be reconstructed from perception above chance.

Let:

- `I_t` = intended internal state,
- `m_t` = VSI modulation,
- `S_t` = perceived visual state,
- `I_hat_t` = decoded state reported or acted upon by the observer.

Then:

```text
I_t
 -> encoder
 -> m_t
 -> perception
 -> I_hat_t
```

The basic research target is:

```text
mutual_information(I_t, I_hat_t) > 0
```

More practically:

- classification accuracy above chance,
- low false-positive rate,
- low confusion between symbols,
- stable performance across sessions,
- acceptable latency,
- acceptable visual load.

A nominally rich visual pattern is useless if users cannot decode it reliably.

---

## 7. Suggested development stages

### VSI-0 — External artificial field

Do not begin with biological intervention.

Create an ordinary display that visually resembles a dynamic noisy field and inject controlled patterns into it.

Measure whether users can detect:

- direction,
- location,
- density shifts,
- coherent motion,
- short pulses.

### VSI-1 — Sparse visual alphabet

Reduce the alphabet to the smallest robust symbol set.

For example:

```text
4 directions
x 2 intensity bins
x 4 spatial sectors
```

This gives 32 nominal states, but only states that are reliably distinguishable should be retained.

### VSI-2 — HexDoku profile

Define a deterministic profile such as:

```text
VSI_PROFILE_V1
```

containing:

- symbol ordering,
- visual parameters,
- timing,
- spatial addressing,
- checksum / trial verification,
- calibration parameters.

### VSI-3 — Adaptive per-user calibration

Perceptual thresholds differ across users.

The profile may therefore separate:

```text
canonical symbol semantics
from
individual rendering parameters
```

The meaning remains deterministic, while contrast, size, speed, and duration may be calibrated.

### VSI-4 — Closed-loop attention interface

Only after external-display decoding is demonstrated should a closed-loop system be considered.

Possible future inputs include:

- eye tracking,
- EEG/BCI-derived state,
- task state,
- anomaly detector,
- model confidence,
- HexDoku reconstruction state.

The VSI output then becomes a compact nonverbal status layer.

---

## 8. Desired use inside HexDoku

The strongest initial use is not "show every bit."

It is to expose only high-value state transitions.

Examples:

```text
reconstruction complete
verification failed
branch ambiguity increased
new high-value relation found
state diverged
rollback required
novel state detected
confidence changed sharply
```

This follows the same sparse-state principle as HexDoku itself:

> do not retransmit what is already known; surface only the information that changed.

For a human observer:

> do not continuously display what is already expected; surface only perceptually useful deltas.

---

## 9. Safety boundary

VSI development should not intentionally attempt to worsen, induce, or destabilize visual symptoms.

The first research path should remain ordinary-screen based.

Potentially provocative visual stimulation should be bounded by:

- user-controlled intensity,
- immediate stop,
- short exposure,
- conservative default contrast,
- optional reduced-motion mode,
- no assumption that discomfort implies useful adaptation,
- no interpretation of symptom worsening as successful training.

A VSI prototype is an HCI experiment, not a medical treatment.

Genetic intervention, unsupervised neurostimulation, drug manipulation, or intentional symptom induction are outside the scope of the HexDoku VSI profile.

---

## 10. Falsification criteria

The VSI direction should be dropped or narrowed if controlled testing shows that:

1. visual symbols cannot be decoded above chance,
2. performance is not reproducible across sessions,
3. additional visual complexity reduces decision speed,
4. latency exceeds conventional UI,
5. the channel causes unacceptable visual load,
6. individual calibration prevents a usable canonical mapping.

The project should report negative results rather than treating subjective impressions as proof.

---

## 11. Near-term research target

The immediate engineering target is:

```text
HexDoku / task state
      |
      v
8-symbol VSI alphabet
      |
      v
dynamic noise-like screen
      |
      v
forced-choice decoding
      |
      v
accuracy + latency + false positives
```

A first successful result would not need a large bandwidth.

Even a reliable 2–3 bit perceptual event that is recognized faster than reading a textual status message would justify further work.

---

## 12. Long-term outlook

If a visual modulation channel proves reliable, VSI could become a human-facing counterpart to HexDoku's compact machine-facing state representation.

Machine side:

```text
large state
 -> Seed Cell / compact descriptor
 -> deterministic reconstruction
```

Human side:

```text
large state
 -> relevance reduction
 -> compact VSI descriptor
 -> nonverbal perception
```

The shared principle is the same:

> preserve the information required for reconstruction while discarding repeated or irrelevant representation.

In the long term, VSI may therefore be explored as a **perceptual sparse bus** rather than as a conventional display.

---

## References

1. Montoya SA, et al. *Adapting to Visual Noise Alleviates Visual Snow.* Invest Ophthalmol Vis Sci. 2023;64(15):23. PMID: 38117246. https://pubmed.ncbi.nlm.nih.gov/38117246/
2. Montoya SA, et al. *Visual Snow Is Susceptible to the Motion Aftereffect.* Invest Ophthalmol Vis Sci. 2025;66(13):23. PMID: 41085357. https://pubmed.ncbi.nlm.nih.gov/41085357/
3. Schankin CJ, et al. / recent review: *Visual snow syndrome: recent advances in understanding the pathophysiology and potential treatment approaches.* PMID: 38465699. https://pubmed.ncbi.nlm.nih.gov/38465699/
4. Shibata M. *Brain dysfunction underlying visual snow syndrome: Insights into therapeutic implications.* Brain Dev. 2025;47(3):104362. PMID: 40311549. https://pubmed.ncbi.nlm.nih.gov/40311549/

---

## Scope note

This document is intentionally separate from the normative HexDoku architecture.

No VSI assumption is required for:

- HDC,
- HDE,
- Seed Cells,
- Sudoku Profile v1,
- parity layout,
- canonical reconstruction,
- compression benchmarks,
- integrity verification.

VSI remains an optional future research branch until independently measured.

# Contributing to HexDoku

HexDoku is currently an experimental research project.

Contributions are most useful when they improve **formal clarity, reproducibility, or falsifiability**.

## Good contribution areas

- Seed Cell schema design
- canonical serialization
- deterministic reconstruction
- solved-board mapping rules
- corruption tests
- rollback tests
- cross-platform determinism
- storage accounting
- benchmark harnesses
- comparison with related architectures
- security review
- mathematical formalization

## Contribution rules

Please:

1. separate measured results from hypotheses;
2. include a reproducible test for behavior changes;
3. avoid claims that a hash can reconstruct unknown source bytes;
4. count external/shared dependencies in storage comparisons;
5. pin reconstruction-critical versions;
6. preserve byte-for-byte determinism unless the change explicitly revises the protocol;
7. document any compatibility break.

## Benchmark submissions

A benchmark should report at minimum:

```text
dataset
dataset bytes
seed bytes
shared-store bytes
transferred bytes
reconstruction time
original hash
reconstructed hash
byte equality
software version
hardware / OS
```

## Experimental branches

Large speculative changes should remain isolated until they have:

- a defined hypothesis,
- a test,
- reproducible results,
- no regression in deterministic reconstruction.

## Licensing

No open-source license has been selected yet. Contributions should not assume a specific reuse license until a LICENSE file is added.

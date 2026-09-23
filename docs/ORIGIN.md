# Origin of the HexDoku Idea

The conceptual starting point of HexDoku was a deliberately unusual question:

> **「エピゲノムの逆って、数独じゃないか？」**

This should be read as a design intuition, not as a biological assertion.

## The contrast

The intuition was based on two opposite-looking directions of information use.

In a simplified analogy, epigenomic state can be thought of as influencing which parts of an already-existing information space become active or expressed.

A Sudoku puzzle points the other way: a limited set of constraints and known placements can determine a much larger completed global arrangement.

That contrast suggested an engineering question:

> Can a compact state, identifier, or constraint set select and deterministically reconstruct a much larger shared state?

HexDoku grew from that question.

## From Sudoku to HexDoku

The next step was to stop treating a solved Sudoku board merely as an answer.

Instead, the completed board can be treated as a reusable structural object:

- a connection map
- an ordering system
- a parity layout
- a dependency map
- a reconstruction coefficient map
- an addressing surface

This led to the idea of pairing that layout with a small **Seed Cell**.

## Seed Cell intuition

The Seed Cell does not contain the whole reconstructed object.

It contains enough information to identify the exact reconstruction universe, for example:

- HexDoku serial / ID
- rule version
- generator parameters
- manifest hash
- chunk hashes

If two nodes already share the same rules and much of the same data universe, the Seed Cell can act as a compact bootstrap.

## Important boundary

The idea does **not** imply that hashes contain the original data.

A hash can identify and verify content. Missing source bytes still have to be locally present, fetched, deterministically generated, or otherwise available.

That distinction is central to HexDoku's public specification.

## Why publish the idea early?

The architecture is easier to evaluate when its core assumptions are explicit.

The project is therefore being published as an experimental, falsifiable design rather than as a finished claim of superior compression or fault tolerance.

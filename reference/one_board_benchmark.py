#!/usr/bin/env python3
"""HexDoku one-board order/HR benchmark.

Scope:
- one fixed solved 9x9 Sudoku ParityGrid
- HDC-Lite fixed 9+9+7 family (36 masks)
- experimental order-bearing MRV profile
- exact deterministic feasibility checks
- no third-party dependencies

This script measures:
- accepted masks (exact HDE round trip to source Parity)
- distinct derived solve orders K
- log2(K)
- target HR and full-DNA HR histograms
- sum(HR)
- candidate-cell evaluations
- feasibility-search calls

It intentionally does NOT claim that this one sample generalizes.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
import math
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Board = List[List[int]]
Coord = Tuple[int, int]

FULL = (1 << 9) - 1

PARITY: Board = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8],
]


def bit(d: int) -> int:
    return 1 << (d - 1)


def box_id(r: int, c: int) -> int:
    return (r // 3) * 3 + (c // 3)


def copy_board(board: Sequence[Sequence[int]]) -> Board:
    return [list(row) for row in board]


def validate_complete(board: Sequence[Sequence[int]]) -> bool:
    want = set(range(1, 10))
    if len(board) != 9 or any(len(row) != 9 for row in board):
        return False
    for r in range(9):
        if set(board[r]) != want:
            return False
    for c in range(9):
        if {board[r][c] for r in range(9)} != want:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if {
                board[r][c]
                for r in range(br, br + 3)
                for c in range(bc, bc + 3)
            } != want:
                return False
    return True


def build_masks(board: Sequence[Sequence[int]]) -> Tuple[List[int], List[int], List[int]]:
    row = [0] * 9
    col = [0] * 9
    box = [0] * 9
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == 0:
                continue
            if not 1 <= d <= 9:
                raise ValueError("cell must be 0..9")
            b = bit(d)
            k = box_id(r, c)
            if (row[r] & b) or (col[c] & b) or (box[k] & b):
                raise ValueError("invalid Sudoku board")
            row[r] |= b
            col[c] |= b
            box[k] |= b
    return row, col, box


def legal_mask(row: Sequence[int], col: Sequence[int], box: Sequence[int], r: int, c: int) -> int:
    used = row[r] | col[c] | box[box_id(r, c)]
    return FULL & ~used


def iter_digits(mask: int) -> Iterable[int]:
    for d in range(1, 10):
        if mask & bit(d):
            yield d


def put(board: Board, row: List[int], col: List[int], box: List[int], r: int, c: int, d: int) -> None:
    b = bit(d)
    board[r][c] = d
    row[r] |= b
    col[c] |= b
    box[box_id(r, c)] |= b


def remove(board: Board, row: List[int], col: List[int], box: List[int], r: int, c: int, d: int) -> None:
    b = bit(d)
    board[r][c] = 0
    row[r] ^= b
    col[c] ^= b
    box[box_id(r, c)] ^= b


def has_solution(
    board: Board,
    row: List[int],
    col: List[int],
    box: List[int],
    counters: Dict[str, int],
) -> bool:
    """Exact deterministic existence test using MRV and ascending digit order."""
    counters["feasibility_calls"] += 1

    best: Optional[Coord] = None
    best_mask = 0
    best_count = 10

    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                continue
            m = legal_mask(row, col, box, r, c)
            n = m.bit_count()
            if n == 0:
                return False
            if n < best_count:
                best = (r, c)
                best_mask = m
                best_count = n
                if n == 1:
                    break
        if best_count == 1:
            break

    if best is None:
        return True

    r, c = best
    for d in iter_digits(best_mask):
        put(board, row, col, box, r, c, d)
        if has_solution(board, row, col, box, counters):
            remove(board, row, col, box, r, c, d)
            return True
        remove(board, row, col, box, r, c, d)

    return False


def solve_order_bearing(masked: Sequence[Sequence[int]]) -> Optional[Dict[str, object]]:
    """Experimental dynamic target profile.

    Target coordinate:
      minimum candidate count, then row-major tie-break.

    Value:
      smallest candidate that preserves at least one complete Sudoku solution.
    """
    board = copy_board(masked)
    row, col, box = build_masks(board)

    order: List[Coord] = []
    target_hr_hist: Counter[int] = Counter()
    dna_hr_hist: Counter[int] = Counter()

    sum_hr_targets = 0
    sum_hr_dna = 0
    candidate_cell_evaluations = 0
    counters = {"feasibility_calls": 0}

    while True:
        best: Optional[Coord] = None
        best_mask = 0
        best_count = 10
        unresolved = 0

        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    continue

                unresolved += 1
                m = legal_mask(row, col, box, r, c)
                n = m.bit_count()
                candidate_cell_evaluations += 1

                if n == 0:
                    return None

                hr = n - 1
                dna_hr_hist[hr] += 1
                sum_hr_dna += hr

                if (
                    n < best_count
                    or (
                        n == best_count
                        and (best is None or (r, c) < best)
                    )
                ):
                    best = (r, c)
                    best_mask = m
                    best_count = n

        if unresolved == 0:
            break

        assert best is not None
        r, c = best

        target_hr = best_count - 1
        target_hr_hist[target_hr] += 1
        sum_hr_targets += target_hr

        chosen: Optional[int] = None
        for d in iter_digits(best_mask):
            put(board, row, col, box, r, c, d)
            if has_solution(board, row, col, box, counters):
                chosen = d
                break
            remove(board, row, col, box, r, c, d)

        if chosen is None:
            return None

        # chosen value remains committed
        order.append((r, c))

    return {
        "board": board,
        "order": order,
        "sum_hr_targets": sum_hr_targets,
        "sum_hr_dna": sum_hr_dna,
        "target_hr_hist": dict(sorted(target_hr_hist.items())),
        "dna_hr_hist": dict(sorted(dna_hr_hist.items())),
        "candidate_cell_evaluations": candidate_cell_evaluations,
        "feasibility_calls": counters["feasibility_calls"],
    }


def make_997_board(parity: Sequence[Sequence[int]], visible_threes: Sequence[Coord]) -> Board:
    keep = set(visible_threes)
    board = copy_board(parity)
    for r in range(9):
        for c in range(9):
            d = parity[r][c]
            if d in (1, 2) or (d == 3 and (r, c) not in keep):
                board[r][c] = 0
    return board


def coord_name(coord: Coord) -> str:
    r, c = coord
    return f"r{r + 1}c{c + 1}"


def order_key(order: Sequence[Coord]) -> Tuple[Coord, ...]:
    return tuple(order)


def main() -> None:
    if not validate_complete(PARITY):
        raise SystemExit("reference Parity is invalid")

    threes = [
        (r, c)
        for r in range(9)
        for c in range(9)
        if PARITY[r][c] == 3
    ]

    tested = 0
    accepted: List[Dict[str, object]] = []
    rejected = 0

    aggregate_target_hist: Counter[int] = Counter()
    aggregate_dna_hist: Counter[int] = Counter()

    for rank, visible_pair in enumerate(combinations(threes, 2)):
        tested += 1
        masked = make_997_board(PARITY, visible_pair)
        result = solve_order_bearing(masked)

        if result is None or result["board"] != PARITY:
            rejected += 1
            continue

        accepted_record = {
            "mask_rank": rank,
            "visible_threes": [coord_name(c) for c in visible_pair],
            "order": [coord_name(c) for c in result["order"]],
            "sum_hr_targets": result["sum_hr_targets"],
            "sum_hr_dna": result["sum_hr_dna"],
            "candidate_cell_evaluations": result["candidate_cell_evaluations"],
            "feasibility_calls": result["feasibility_calls"],
            "target_hr_hist": result["target_hr_hist"],
            "dna_hr_hist": result["dna_hr_hist"],
        }
        accepted.append(accepted_record)

        aggregate_target_hist.update(
            {int(k): int(v) for k, v in result["target_hr_hist"].items()}
        )
        aggregate_dna_hist.update(
            {int(k): int(v) for k, v in result["dna_hr_hist"].items()}
        )

    unique_orders = {
        tuple(rec["order"])
        for rec in accepted
    }
    k = len(unique_orders)

    summary = {
        "profile": "sudoku-order-bearing-mrv-v0",
        "source": "single canonical solved Sudoku sample",
        "hdc_family": "fixed-9+9+7 / 36 masks",
        "masks_tested": tested,
        "accepted_exact_roundtrip": len(accepted),
        "rejected": rejected,
        "distinct_orders_K": k,
        "order_capacity_log2_K_bits": math.log2(k) if k else 0.0,
        "family_upper_bound_log2_36_bits": math.log2(36),
        "target_hr_hist_aggregate": dict(sorted(aggregate_target_hist.items())),
        "dna_hr_hist_aggregate": dict(sorted(aggregate_dna_hist.items())),
        "sum_hr_targets_min": min((int(r["sum_hr_targets"]) for r in accepted), default=0),
        "sum_hr_targets_max": max((int(r["sum_hr_targets"]) for r in accepted), default=0),
        "sum_hr_dna_min": min((int(r["sum_hr_dna"]) for r in accepted), default=0),
        "sum_hr_dna_max": max((int(r["sum_hr_dna"]) for r in accepted), default=0),
        "candidate_cell_evaluations_per_accepted_board": sorted(
            {int(r["candidate_cell_evaluations"]) for r in accepted}
        ),
        "note": (
            "Single reference Parity only. K and HR statistics are sample measurements, "
            "not general HexDoku guarantees."
        ),
    }

    print(json.dumps({"summary": summary, "accepted": accepted}, indent=2))


if __name__ == "__main__":
    main()

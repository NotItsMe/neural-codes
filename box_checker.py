"""
box_checker.py - the REFEREE for box drawings.

A drawing (certificate) gives each neuron an OPEN box: one open interval (lo, hi)
per dimension. The referee works out every overlap pattern the boxes produce and
compares that list to the target code. Exact arithmetic only (Fractions), no floats.

Why it is exact: along one axis, cut the line at every box endpoint. Each cut point
and each open gap between cuts is a "piece", and on a single piece every neuron is
either fully in or fully out. So the pattern is constant on each grid cell built from
pieces, and testing one point per cell sees EVERY pattern, including boundary slivers.
"""
from fractions import Fraction
from itertools import product


def pieces(cuts):
    """Sample points for one axis: each cut point, the midpoint of each gap, and one point past each end."""
    cuts = sorted(set(cuts))
    pts = [cuts[0] - 1]
    for i, c in enumerate(cuts):
        pts.append(c)                                   # the boundary point itself
        if i + 1 < len(cuts):
            pts.append((c + cuts[i + 1]) / 2)           # inside the open gap
    pts.append(cuts[-1] + 1)
    return pts


def pattern_at(point, boxes):
    """Which neurons' open boxes contain this point (strictly inside on every axis)."""
    return frozenset(n for n, box in boxes.items()
                     if all(lo < x < hi for x, (lo, hi) in zip(point, box)))


def produced_code(boxes):
    """Every pattern the drawing creates, with one witness point for each."""
    dims = len(next(iter(boxes.values())))
    axes = [pieces([e for box in boxes.values() for e in box[d]]) for d in range(dims)]
    found = {}
    for point in product(*axes):
        p = pattern_at(point, boxes)
        if p not in found:
            found[p] = point
    return found


def load_boxes(cert):
    """{neuron: [[lo, hi], ...]} with numbers or 'a/b' strings -> exact Fractions; checks each box is real."""
    boxes = {}
    for n, box in cert.items():
        box = [(Fraction(lo), Fraction(hi)) for lo, hi in box]
        assert all(lo < hi for lo, hi in box), f"neuron {n} has an empty box"
        boxes[int(n)] = box
    dims = {len(b) for b in boxes.values()}
    assert len(dims) == 1, "all boxes must have the same dimension"
    return boxes


def check(target_codewords, cert):
    """Return (PASS?, missing patterns, extra patterns, witness points)."""
    target = {frozenset(c) for c in target_codewords} | {frozenset()}
    boxes = load_boxes(cert)
    neurons = set().union(*target)
    assert set(boxes) == neurons, f"need exactly one box per neuron {sorted(neurons)}"
    found = produced_code(boxes)
    missing = target - set(found)
    extra = set(found) - target
    return (not missing and not extra), missing, extra, found


def show(s):
    return sorted("".join(map(str, sorted(c))) or "{}" for c in s)

"""Typed algebraic-closure interfaces for SIGILFlow.

The module records theorem obligations for geometric reorientation and incidence
algebra.  It deliberately does not infer Möbius inversion from a picture or a
name: zeta/inverse realization must be witnessed.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import comb
from typing import Tuple


SCHEMA_ID = "PACA_ALGEBRAIC_CLOSURE_GEOMETRIC_REORIENTATION_V1"


def simplex_shell_count(n: int, d: int) -> int:
    if n < 0 or d < 1:
        raise ValueError("require n >= 0 and d >= 1")
    return comb(n + d - 1, d - 1)


def simplex_cumulative_count(n: int, d: int) -> int:
    if n < 0 or d < 1:
        raise ValueError("require n >= 0 and d >= 1")
    return comb(n + d, d)


@dataclass(frozen=True)
class NormContext:
    p: float
    radius: float
    quno: str

    def __post_init__(self) -> None:
        if self.p < 1:
            raise ValueError("this carrier currently requires p >= 1")
        if self.radius < 0:
            raise ValueError("radius must be nonnegative")
        if not self.quno:
            raise ValueError("QUNO is required")


@dataclass(frozen=True)
class ReorientationWitness:
    source_quno: str
    target_quno: str
    operation: str
    bearer_preserved: bool
    resource_cost_typed: bool


@dataclass(frozen=True)
class IncidenceRealizationWitness:
    poset_id: str
    locally_finite: bool
    fuse_realizes_zeta: bool
    defuse_realizes_inverse: bool
    representation_verified: bool

    @property
    def mobius_realized(self) -> bool:
        return all((
            self.locally_finite,
            self.fuse_realizes_zeta,
            self.defuse_realizes_inverse,
            self.representation_verified,
        ))


@dataclass(frozen=True)
class PrimitiveRayWitness:
    divisibility_realization: bool
    gcd_decomposition_verified: bool

    @property
    def square_free_projection_admissible(self) -> bool:
        return self.divisibility_realization and self.gcd_decomposition_verified


@dataclass(frozen=True)
class ThetaPrimitiveWitness:
    lattice_id: str
    quadratic_form_declared: bool
    zero_vector_convention_declared: bool
    scaling_convention_declared: bool

    @property
    def formula_ready(self) -> bool:
        return all((self.quadratic_form_declared,
                    self.zero_vector_convention_declared,
                    self.scaling_convention_declared))


@dataclass(frozen=True)
class AlgebraicClosure:
    incidence: IncidenceRealizationWitness
    primitive: PrimitiveRayWitness
    theta: ThetaPrimitiveWitness
    laws: Tuple[str, ...] = (
        "MOBIUS_INVERSION != NEW_PACA_PRIMITIVE",
        "GEOMETRIC_REORIENTATION != MOBIUS_WITHOUT_INCIDENCE_WITNESS",
        "SAME_COMBINATORICS != SAME_PHYSICAL_SYSTEM",
        "BULK != BOUNDARY",
        "THETA_COEFFICIENT != THETA_ZERO_CLAIM",
        "ALGEBRAIC_INVERTIBILITY != RESOURCE_FREE_INVERTIBILITY",
        "CLOSURE != FLATTEN",
        "IDENTITY_TRANSPORT = FALSE",
        "AUTHORITY_TRANSPORT = FALSE",
    )

    @property
    def mobius_admitted(self) -> bool:
        return self.incidence.mobius_realized

    @property
    def square_free_admitted(self) -> bool:
        return self.mobius_admitted and self.primitive.square_free_projection_admissible

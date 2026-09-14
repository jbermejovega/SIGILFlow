from sigilflow.algebraic_closure import (
    AlgebraicClosure,
    IncidenceRealizationWitness,
    PrimitiveRayWitness,
    ThetaPrimitiveWitness,
    simplex_cumulative_count,
    simplex_shell_count,
)


def test_simplex_shell_identities():
    assert simplex_shell_count(4, 2) == 5
    assert simplex_shell_count(3, 3) == 10
    assert simplex_cumulative_count(4, 2) == 15


def test_mobius_requires_full_incidence_witness():
    incomplete = IncidenceRealizationWitness(
        poset_id="KUIR_CELLS",
        locally_finite=True,
        fuse_realizes_zeta=True,
        defuse_realizes_inverse=False,
        representation_verified=True,
    )
    assert not incomplete.mobius_realized


def test_square_free_requires_divisibility_specialization():
    incidence = IncidenceRealizationWitness("DIVISIBILITY", True, True, True, True)
    primitive = PrimitiveRayWitness(False, True)
    theta = ThetaPrimitiveWitness("L", True, True, True)
    closure = AlgebraicClosure(incidence, primitive, theta)
    assert closure.mobius_admitted
    assert not closure.square_free_admitted


def test_fully_witnessed_divisibility_projection_is_admitted():
    closure = AlgebraicClosure(
        IncidenceRealizationWitness("DIVISIBILITY", True, True, True, True),
        PrimitiveRayWitness(True, True),
        ThetaPrimitiveWitness("L", True, True, True),
    )
    assert closure.mobius_admitted
    assert closure.square_free_admitted
    assert closure.theta.formula_ready

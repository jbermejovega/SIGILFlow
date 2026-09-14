from sigilflow.ast_renormalization import normalize_kernel_ast, renormalize_ast
from sigilflow.kernel import build_reference_kernel


def test_normalization_is_stable_projection():
    kernel = build_reference_kernel(epoch=0)
    a = normalize_kernel_ast(kernel)
    b = normalize_kernel_ast(kernel)
    assert a.canonical_digest == b.canonical_digest
    assert a.ast_id == b.ast_id
    assert a.normalize_is_renormalize is False
    assert a.same_projection_is_same_bearer is False


def test_renormalization_allocates_fresh_occurrence():
    ast = normalize_kernel_ast(build_reference_kernel(epoch=0))
    r1 = renormalize_ast(ast, epoch=1)
    r2 = renormalize_ast(ast, epoch=2)
    assert r1.projection_digest == r2.projection_digest == ast.canonical_digest
    assert r1.occurrence_digest != r2.occurrence_digest
    assert r1.occurrence_id != r2.occurrence_id
    assert {n.bearer_id for n in r1.nodes}.isdisjoint({n.bearer_id for n in ast.nodes})
    assert {n.bearer_id for n in r1.nodes}.isdisjoint({n.bearer_id for n in r2.nodes})
    assert r1.identity_transport is False
    assert r1.authority_transport is False


def test_admission_spine_survives_normalization():
    ast = normalize_kernel_ast(build_reference_kernel(epoch=0))
    relations = [(e.source_node, e.relation, e.target_node) for e in ast.edges]
    assert ("ast:sigilbook:poetry", "COMPILE_TO_PACAPDG", "ast:sigilbook:pacapdg") in relations
    assert ("ast:sigilbook:pacapdg", "ADMISSION", "ast:sigilbook:uap") in relations
    assert ("ast:sigilbook:uap", "SAFE_REPLAY", "ast:sigilbook:safe-replay") in relations


def test_renormalization_requires_epoch_advance():
    ast = normalize_kernel_ast(build_reference_kernel(epoch=3))
    try:
        renormalize_ast(ast, epoch=3)
    except ValueError as exc:
        assert "RENORMALIZED_EPOCH_MUST_ADVANCE" in str(exc)
    else:
        raise AssertionError("expected epoch guard")

import pytest

from sigilflow import (
    FlowCapability,
    FlowRequest,
    build_default_registry,
)


def test_qaoa_routes_across_multiple_flow_libraries() -> None:
    registry = build_default_registry()
    route = registry.route(
        FlowRequest(
            request_id="qaoa-1",
            capability=FlowCapability.QAOA,
            payload={"problem": "fixture"},
            source_quno="quno://request/source",
            target_quno="quno://request/target",
        )
    )
    assert {"openqaoa", "dmrg", "rqaoa"} <= set(route.adapter_ids)
    assert route.pacapdg_required
    assert route.uap_required
    assert route.safe_replay_required


def test_poetry_route_is_source_bound_and_not_execution_authority() -> None:
    registry = build_default_registry()
    poetry = next(adapter for adapter in registry.adapters if adapter.adapter_id == "poetry")
    assert poetry.source_bound
    assert poetry.semantic_equivalence_claimed is False
    assert poetry.execution_authority is False


def test_unknown_capability_surface_is_not_silently_invented() -> None:
    registry = build_default_registry()
    request = FlowRequest(
        request_id="dependency",
        capability=FlowCapability.DEPENDENCY_FLOW,
        payload={},
        source_quno="quno://a",
        target_quno="quno://b",
    )
    route = registry.route(request)
    assert route.adapter_ids == ("pacapdg",)

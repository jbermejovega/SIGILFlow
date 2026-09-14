from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, Literal, Mapping, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .kernel import FlowLibrary

STRICT = ConfigDict(extra="forbid", frozen=True, strict=True, validate_default=True, str_strip_whitespace=True)
NonEmpty = Annotated[str, Field(min_length=1)]


class FlowCapability(StrEnum):
    CIRCUIT_SIMULATION = "CIRCUIT_SIMULATION"
    VARIATIONAL_OPTIMIZATION = "VARIATIONAL_OPTIMIZATION"
    TENSOR_NETWORK = "TENSOR_NETWORK"
    DMRG = "DMRG"
    QAOA = "QAOA"
    RQAOA = "RQAOA"
    POETRY_TRANSFORM = "POETRY_TRANSFORM"
    DEPENDENCY_FLOW = "DEPENDENCY_FLOW"
    ADMISSION = "ADMISSION"


class FlowAdapter(BaseModel):
    model_config = STRICT
    adapter_id: NonEmpty
    library: FlowLibrary
    source_path: NonEmpty
    capabilities: tuple[FlowCapability, ...] = Field(min_length=1)
    input_schema: NonEmpty
    output_schema: NonEmpty
    quno_context: NonEmpty
    source_bound: Literal[True] = True
    semantic_equivalence_claimed: Literal[False] = False
    execution_authority: Literal[False] = False


class FlowRequest(BaseModel):
    model_config = STRICT
    request_id: NonEmpty
    capability: FlowCapability
    payload: Mapping[str, Any]
    source_quno: NonEmpty
    target_quno: NonEmpty
    require_safe_replay: bool = True


class FlowRoute(BaseModel):
    model_config = STRICT
    request_id: NonEmpty
    adapter_ids: tuple[NonEmpty, ...] = Field(min_length=1)
    capability: FlowCapability
    pacapdg_required: Literal[True] = True
    uap_required: Literal[True] = True
    safe_replay_required: bool = True


class FlowKernelRegistry(BaseModel):
    model_config = STRICT
    adapters: tuple[FlowAdapter, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_adapters(self) -> Self:
        ids = [a.adapter_id for a in self.adapters]
        if len(ids) != len(set(ids)):
            raise ValueError("ADAPTER_IDS_MUST_BE_UNIQUE")
        return self

    def route(self, request: FlowRequest) -> FlowRoute:
        candidates = [a.adapter_id for a in self.adapters if request.capability in a.capabilities]
        if not candidates:
            raise ValueError(f"NO_FLOW_ADAPTER_FOR:{request.capability.value}")
        return FlowRoute(
            request_id=request.request_id,
            adapter_ids=tuple(candidates),
            capability=request.capability,
            safe_replay_required=request.require_safe_replay,
        )


def build_default_registry() -> FlowKernelRegistry:
    return FlowKernelRegistry(
        adapters=(
            FlowAdapter(adapter_id="openqaoa", library=FlowLibrary.OPENQAOA, source_path="OpenQAOA/", capabilities=(FlowCapability.QAOA, FlowCapability.VARIATIONAL_OPTIMIZATION), input_schema="QAOAProblem", output_schema="QAOAResult", quno_context="quno://flow/openqaoa"),
            FlowAdapter(adapter_id="qibo", library=FlowLibrary.QIBO, source_path="Qibo/", capabilities=(FlowCapability.CIRCUIT_SIMULATION, FlowCapability.VARIATIONAL_OPTIMIZATION), input_schema="Circuit", output_schema="SimulationResult", quno_context="quno://flow/qibo"),
            FlowAdapter(adapter_id="quimb", library=FlowLibrary.QUIMB, source_path="Qimb/", capabilities=(FlowCapability.TENSOR_NETWORK, FlowCapability.DMRG), input_schema="TensorNetworkProblem", output_schema="TensorNetworkResult", quno_context="quno://flow/quimb"),
            FlowAdapter(adapter_id="dmrg", library=FlowLibrary.DMRG, source_path="Quantum-Circuit-Simulator-DMRG/", capabilities=(FlowCapability.DMRG, FlowCapability.TENSOR_NETWORK, FlowCapability.QAOA), input_schema="MPSCircuitProblem", output_schema="MPSCircuitResult", quno_context="quno://flow/dmrg"),
            FlowAdapter(adapter_id="rqaoa", library=FlowLibrary.RQAOA, source_path="RQAOA/", capabilities=(FlowCapability.RQAOA, FlowCapability.QAOA), input_schema="RQAOAProblem", output_schema="RQAOAResult", quno_context="quno://flow/rqaoa"),
            FlowAdapter(adapter_id="tensorcircuit", library=FlowLibrary.TENSORCIRCUIT, source_path="TensorCircuit/", capabilities=(FlowCapability.CIRCUIT_SIMULATION, FlowCapability.TENSOR_NETWORK), input_schema="Circuit", output_schema="TensorCircuitResult", quno_context="quno://flow/tensorcircuit"),
            FlowAdapter(adapter_id="cirq", library=FlowLibrary.CIRQ, source_path="cirq/", capabilities=(FlowCapability.CIRCUIT_SIMULATION,), input_schema="Circuit", output_schema="SimulationResult", quno_context="quno://flow/cirq"),
            FlowAdapter(adapter_id="pennylane", library=FlowLibrary.PENNYLANE, source_path="pennylane/", capabilities=(FlowCapability.CIRCUIT_SIMULATION, FlowCapability.VARIATIONAL_OPTIMIZATION), input_schema="QNodeProblem", output_schema="QNodeResult", quno_context="quno://flow/pennylane"),
            FlowAdapter(adapter_id="poetry", library=FlowLibrary.POETRY_KERNEL, source_path="sigilbook://poetry-kernel", capabilities=(FlowCapability.POETRY_TRANSFORM,), input_schema="PoetryType", output_schema="FreshPoetryOccurrence", quno_context="quno://flow/poetry"),
            FlowAdapter(adapter_id="pacapdg", library=FlowLibrary.PACAPDG, source_path="sigilbook://pacapdg", capabilities=(FlowCapability.ADMISSION, FlowCapability.DEPENDENCY_FLOW), input_schema="FlowCandidate", output_schema="PACAPDGRecord", quno_context="quno://flow/pacapdg"),
        )
    )


__all__ = [
    "FlowCapability", "FlowAdapter", "FlowRequest", "FlowRoute", "FlowKernelRegistry", "build_default_registry",
]

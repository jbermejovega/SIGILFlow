from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_ID = "SIGILFLOW_PRESHEAF_SHEAF_PREIMAGE_KERNEL_FUSION_V1"
TFG_REPO = "mbenitezzs31-cloud/TFG"
TFG_COMMIT = "3f06c29063334e42d97218355adf02118d794a40"
SIGILBOOK_REPO = "jbermejovega/sigilbook"
SIGILBOOK_COMMIT = "1ac6415d83adcde8d17df06f94fa324dd96acbce"
SIGILFLOW_REPO = "jbermejovega/SIGILFlow"
PROTECTED_PI = "PIORNALEGO_ES_CANON"
STRICT = ConfigDict(extra="forbid", frozen=True, strict=True, validate_default=True, str_strip_whitespace=True)
NonEmpty = Annotated[str, Field(min_length=1)]


class SourceRole(StrEnum):
    COMPUTATIONAL = "COMPUTATIONAL"
    SEMANTIC = "SEMANTIC"
    FUSION = "FUSION"


class RepoPin(BaseModel):
    model_config = STRICT
    repository: NonEmpty
    commit: NonEmpty
    role: SourceRole
    source_bound: Literal[True] = True
    authority_transport: Literal[False] = False
    identity_transport: Literal[False] = False


class FlowLibrary(StrEnum):
    OPENQAOA = "OpenQAOA"
    QIBO = "Qibo"
    QUIMB = "Qimb"
    DMRG = "Quantum-Circuit-Simulator-DMRG"
    RQAOA = "RQAOA"
    TENSORCIRCUIT = "TensorCircuit"
    CIRQ = "cirq"
    PENNYLANE = "pennylane"
    RESULTADOS = "Resultados y Discusión"
    POETRY_KERNEL = "PoetryKernel"
    PACAPDG = "PACAPDG"
    UAP = "UAP"
    SAFE_REPLAY = "SAFE_REPLAY"


class Section(BaseModel):
    model_config = STRICT
    section_id: NonEmpty
    repo: NonEmpty
    path: NonEmpty
    quno_context: NonEmpty
    library: FlowLibrary
    epoch: int = Field(ge=0)
    bearer_id: NonEmpty


class RestrictionMap(BaseModel):
    model_config = STRICT
    map_id: NonEmpty
    source_section: NonEmpty
    target_section: NonEmpty
    preserves_context: bool = True
    preserves_provenance: Literal[True] = True

    @model_validator(mode="after")
    def distinct(self) -> Self:
        if self.source_section == self.target_section:
            raise ValueError("RESTRICTION_REQUIRES_DISTINCT_SECTIONS")
        return self


class Presheaf(BaseModel):
    model_config = STRICT
    presheaf_id: NonEmpty
    sections: tuple[Section, ...] = Field(min_length=1)
    restrictions: tuple[RestrictionMap, ...] = ()

    @model_validator(mode="after")
    def validate_references(self) -> Self:
        ids = [s.section_id for s in self.sections]
        if len(ids) != len(set(ids)):
            raise ValueError("SECTION_IDS_MUST_BE_UNIQUE")
        known = set(ids)
        bearers = [s.bearer_id for s in self.sections]
        if len(bearers) != len(set(bearers)):
            raise ValueError("SECTION_BEARERS_MUST_BE_DISTINCT")
        for r in self.restrictions:
            if r.source_section not in known or r.target_section not in known:
                raise ValueError("RESTRICTION_REFERENCES_UNKNOWN_SECTION")
        return self


class SheafPreimage(BaseModel):
    model_config = STRICT
    preimage_id: NonEmpty
    source_presheaf_id: NonEmpty
    target_repo: NonEmpty
    gluing_witnesses: tuple[NonEmpty, ...] = Field(min_length=1)
    local_compatibility_required: Literal[True] = True
    global_section_is_identity_merge: Literal[False] = False


class JoinMeetFusion(BaseModel):
    model_config = STRICT
    fusion_id: NonEmpty
    left_repo: Literal[TFG_REPO] = TFG_REPO
    right_repo: Literal[SIGILBOOK_REPO] = SIGILBOOK_REPO
    carrier_repo: Literal[SIGILFLOW_REPO] = SIGILFLOW_REPO
    meet: tuple[NonEmpty, ...] = Field(min_length=1)
    join: tuple[NonEmpty, ...] = Field(min_length=1)
    meet_is_identity_intersection: Literal[False] = False
    join_is_flatten: Literal[False] = False
    fusion_bearer_is_source_bearer: Literal[False] = False


class SyncPolicy(BaseModel):
    model_config = STRICT
    mode: Literal["PINNED_READ_VALIDATE"] = "PINNED_READ_VALIDATE"
    tfg_pin: RepoPin
    sigilbook_pin: RepoPin
    sigilflow_pin: RepoPin
    auto_pull: Literal[False] = False
    auto_merge: Literal[False] = False
    auto_push: Literal[False] = False
    diff_before_update: Literal[True] = True
    human_review_required: Literal[True] = True


class SigilFlowKernel(BaseModel):
    model_config = STRICT
    schema_id: Literal[SCHEMA_ID] = SCHEMA_ID
    sync: SyncPolicy
    presheaf: Presheaf
    preimage: SheafPreimage
    fusion: JoinMeetFusion
    libraries: tuple[FlowLibrary, ...] = Field(min_length=8)
    pacapdg_precedes_uap: Literal[True] = True
    uap_precedes_safe_replay: Literal[True] = True
    protected_pi: Literal[PROTECTED_PI] = PROTECTED_PI

    @model_validator(mode="after")
    def validate_kernel(self) -> Self:
        if self.preimage.source_presheaf_id != self.presheaf.presheaf_id:
            raise ValueError("PREIMAGE_MUST_REFERENCE_PRESHEAF")
        required = {FlowLibrary.PACAPDG, FlowLibrary.UAP, FlowLibrary.SAFE_REPLAY}
        if not required <= set(self.libraries):
            raise ValueError("ADMISSION_SPINE_LIBRARIES_REQUIRED")
        return self


def build_reference_kernel(epoch: int = 0) -> SigilFlowKernel:
    tfg_pin = RepoPin(repository=TFG_REPO, commit=TFG_COMMIT, role=SourceRole.COMPUTATIONAL)
    sigilbook_pin = RepoPin(repository=SIGILBOOK_REPO, commit=SIGILBOOK_COMMIT, role=SourceRole.SEMANTIC)
    sigilflow_pin = RepoPin(repository=SIGILFLOW_REPO, commit=TFG_COMMIT, role=SourceRole.FUSION)

    sections = tuple(
        Section(
            section_id=f"tfg:{lib.value}",
            repo=TFG_REPO,
            path=f"{lib.value}/",
            quno_context=f"quno://tfg/{lib.name.lower()}",
            library=lib,
            epoch=epoch,
            bearer_id=f"bearer:tfg:{lib.name.lower()}:{epoch}",
        )
        for lib in (
            FlowLibrary.OPENQAOA,
            FlowLibrary.QIBO,
            FlowLibrary.QUIMB,
            FlowLibrary.DMRG,
            FlowLibrary.RQAOA,
            FlowLibrary.TENSORCIRCUIT,
            FlowLibrary.CIRQ,
            FlowLibrary.PENNYLANE,
        )
    ) + (
        Section(section_id="sigilbook:poetry", repo=SIGILBOOK_REPO, path="sigilapi/poemario_primitive_poetry_type_kernel_v1.py", quno_context="quno://sigilbook/poetry", library=FlowLibrary.POETRY_KERNEL, epoch=epoch, bearer_id=f"bearer:sigilbook:poetry:{epoch}"),
        Section(section_id="sigilbook:pacapdg", repo=SIGILBOOK_REPO, path="pipelines/pacapdg/", quno_context="quno://sigilbook/pacapdg", library=FlowLibrary.PACAPDG, epoch=epoch, bearer_id=f"bearer:sigilbook:pacapdg:{epoch}"),
        Section(section_id="sigilbook:uap", repo=SIGILBOOK_REPO, path="sigilbook://uap", quno_context="quno://sigilbook/uap", library=FlowLibrary.UAP, epoch=epoch, bearer_id=f"bearer:sigilbook:uap:{epoch}"),
        Section(section_id="sigilbook:safe-replay", repo=SIGILBOOK_REPO, path="sigilbook://safe-replay", quno_context="quno://sigilbook/safe-replay", library=FlowLibrary.SAFE_REPLAY, epoch=epoch, bearer_id=f"bearer:sigilbook:safe-replay:{epoch}"),
    )

    presheaf = Presheaf(presheaf_id=f"sigilflow:presheaf:{epoch}", sections=sections)
    preimage = SheafPreimage(
        preimage_id=f"sigilflow:sheaf-preimage:{epoch}",
        source_presheaf_id=presheaf.presheaf_id,
        target_repo=SIGILFLOW_REPO,
        gluing_witnesses=("source_pin", "quno_context", "typed_flow_interface", "provenance_preserved"),
    )
    fusion = JoinMeetFusion(
        fusion_id=f"sigilflow:join-meet:{epoch}",
        meet=("typed_flow_interface", "dependency_provenance", "epoch_lineage", "python_notebook_surface"),
        join=("quantum_flow_libraries", "poetry_kernel_semantics", "PACAPDG", "UAP", "SAFE_REPLAY"),
    )
    return SigilFlowKernel(
        sync=SyncPolicy(tfg_pin=tfg_pin, sigilbook_pin=sigilbook_pin, sigilflow_pin=sigilflow_pin),
        presheaf=presheaf,
        preimage=preimage,
        fusion=fusion,
        libraries=tuple(s.library for s in sections),
    )


__all__ = [
    "SCHEMA_ID", "TFG_REPO", "TFG_COMMIT", "SIGILBOOK_REPO", "SIGILBOOK_COMMIT", "SIGILFLOW_REPO",
    "SourceRole", "RepoPin", "FlowLibrary", "Section", "RestrictionMap", "Presheaf", "SheafPreimage",
    "JoinMeetFusion", "SyncPolicy", "SigilFlowKernel", "build_reference_kernel",
]

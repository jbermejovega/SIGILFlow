from __future__ import annotations

from hashlib import sha256
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .kernel import (
    PROTECTED_PI,
    SIGILBOOK_COMMIT,
    SIGILBOOK_REPO,
    SIGILFLOW_REPO,
    TFG_COMMIT,
    TFG_REPO,
    SigilFlowKernel,
)

AST_SCHEMA_ID = "SIGILFLOW_TOTAL_AST_RENORMALIZATION_V1"
STRICT = ConfigDict(extra="forbid", frozen=True, strict=True, validate_default=True, str_strip_whitespace=True)


class ASTSourcePin(BaseModel):
    model_config = STRICT
    repository: str = Field(min_length=1)
    commit: str = Field(min_length=7)
    source_bound: Literal[True] = True


class ASTNode(BaseModel):
    model_config = STRICT
    node_id: str = Field(min_length=1)
    bearer_id: str = Field(min_length=1)
    kind: str = Field(min_length=1)
    source_repo: str = Field(min_length=1)
    source_path: str = Field(min_length=1)
    quno_context: str = Field(min_length=1)
    epoch: int = Field(ge=0)
    projection: str = Field(min_length=1)


class ASTEdge(BaseModel):
    model_config = STRICT
    edge_id: str = Field(min_length=1)
    source_node: str = Field(min_length=1)
    target_node: str = Field(min_length=1)
    relation: str = Field(min_length=1)
    preserves_provenance: Literal[True] = True
    identity_transport: Literal[False] = False
    authority_transport: Literal[False] = False

    @model_validator(mode="after")
    def distinct_nodes(self) -> Self:
        if self.source_node == self.target_node:
            raise ValueError("AST_EDGE_REQUIRES_DISTINCT_OCCURRENCES")
        return self


class NormalizedAST(BaseModel):
    model_config = STRICT
    ast_id: str = Field(min_length=1)
    epoch: int = Field(ge=0)
    nodes: tuple[ASTNode, ...] = Field(min_length=1)
    edges: tuple[ASTEdge, ...] = ()
    canonical_digest: str = Field(min_length=64, max_length=64)
    normalize_is_renormalize: Literal[False] = False
    same_projection_is_same_bearer: Literal[False] = False

    @model_validator(mode="after")
    def validate_ast(self) -> Self:
        node_ids = [n.node_id for n in self.nodes]
        bearer_ids = [n.bearer_id for n in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise ValueError("AST_NODE_IDS_MUST_BE_UNIQUE")
        if len(bearer_ids) != len(set(bearer_ids)):
            raise ValueError("AST_BEARERS_MUST_BE_DISTINCT")
        known = set(node_ids)
        for edge in self.edges:
            if edge.source_node not in known or edge.target_node not in known:
                raise ValueError("AST_EDGE_REFERENCES_UNKNOWN_NODE")
        return self


class RenormalizedAST(BaseModel):
    model_config = STRICT
    schema_id: Literal[AST_SCHEMA_ID] = AST_SCHEMA_ID
    source_ast_id: str = Field(min_length=1)
    occurrence_id: str = Field(min_length=1)
    source_epoch: int = Field(ge=0)
    epoch: int = Field(ge=1)
    projection_digest: str = Field(min_length=64, max_length=64)
    occurrence_digest: str = Field(min_length=64, max_length=64)
    source_pins: tuple[ASTSourcePin, ...] = Field(min_length=2)
    nodes: tuple[ASTNode, ...] = Field(min_length=1)
    pacapdg_precedes_uap: Literal[True] = True
    uap_precedes_safe_replay: Literal[True] = True
    protected_pi: Literal[PROTECTED_PI] = PROTECTED_PI
    fresh_occurrence: Literal[True] = True
    identity_transport: Literal[False] = False
    authority_transport: Literal[False] = False

    @model_validator(mode="after")
    def validate_renormalization(self) -> Self:
        if self.epoch <= self.source_epoch:
            raise ValueError("RENORMALIZED_EPOCH_MUST_ADVANCE")
        if self.projection_digest == self.occurrence_digest:
            raise ValueError("PROJECTION_DIGEST_MUST_NOT_BE_OCCURRENCE_IDENTITY")
        return self


def _digest(parts: list[str]) -> str:
    return sha256("\n".join(parts).encode("utf-8")).hexdigest()


def normalize_kernel_ast(kernel: SigilFlowKernel) -> NormalizedAST:
    """Canonical projection of the fused kernel.

    Normalization sorts by stable semantic coordinates and preserves every source
    section as an identity-distinct bearer. It is a projection, not a fresh
    occurrence.
    """
    ordered = sorted(
        kernel.presheaf.sections,
        key=lambda s: (s.repo, s.path, s.quno_context, s.section_id),
    )
    nodes = tuple(
        ASTNode(
            node_id=f"ast:{section.section_id}",
            bearer_id=section.bearer_id,
            kind=section.library.value,
            source_repo=section.repo,
            source_path=section.path,
            quno_context=section.quno_context,
            epoch=section.epoch,
            projection=f"{section.repo}:{section.path}:{section.library.value}",
        )
        for section in ordered
    )
    edge_specs = [
        ("poetry->pacapdg", "sigilbook:poetry", "sigilbook:pacapdg", "COMPILE_TO_PACAPDG"),
        ("pacapdg->uap", "sigilbook:pacapdg", "sigilbook:uap", "ADMISSION"),
        ("uap->safe-replay", "sigilbook:uap", "sigilbook:safe-replay", "SAFE_REPLAY"),
    ]
    known = {n.node_id for n in nodes}
    edges = tuple(
        ASTEdge(
            edge_id=edge_id,
            source_node=f"ast:{src}",
            target_node=f"ast:{dst}",
            relation=relation,
        )
        for edge_id, src, dst, relation in edge_specs
        if f"ast:{src}" in known and f"ast:{dst}" in known
    )
    digest = _digest(
        [f"{n.projection}|{n.quno_context}" for n in nodes]
        + [f"{e.source_node}>{e.relation}>{e.target_node}" for e in edges]
    )
    epoch = max(n.epoch for n in nodes)
    return NormalizedAST(
        ast_id=f"sigilflow:normalized-ast:{epoch}:{digest[:16]}",
        epoch=epoch,
        nodes=nodes,
        edges=edges,
        canonical_digest=digest,
    )


def renormalize_ast(ast: NormalizedAST, *, epoch: int | None = None) -> RenormalizedAST:
    """Emit a fresh occurrence of a normalized projection.

    RENORMALIZE(NF, e) keeps the projection digest while allocating fresh node
    bearers and occurrence identity. It never rewrites the pinned source repos.
    """
    next_epoch = ast.epoch + 1 if epoch is None else epoch
    if next_epoch <= ast.epoch:
        raise ValueError("RENORMALIZED_EPOCH_MUST_ADVANCE")
    fresh_nodes = tuple(
        node.model_copy(
            update={
                "node_id": f"{node.node_id}:occ:{next_epoch}",
                "bearer_id": f"renorm:{next_epoch}:{node.bearer_id}",
                "epoch": next_epoch,
            }
        )
        for node in ast.nodes
    )
    occurrence_digest = _digest(
        [ast.canonical_digest, str(next_epoch)]
        + [f"{n.node_id}|{n.bearer_id}" for n in fresh_nodes]
    )
    return RenormalizedAST(
        source_ast_id=ast.ast_id,
        occurrence_id=f"sigilflow:renormalized-ast:{next_epoch}:{occurrence_digest[:16]}",
        source_epoch=ast.epoch,
        epoch=next_epoch,
        projection_digest=ast.canonical_digest,
        occurrence_digest=occurrence_digest,
        source_pins=(
            ASTSourcePin(repository=TFG_REPO, commit=TFG_COMMIT),
            ASTSourcePin(repository=SIGILBOOK_REPO, commit=SIGILBOOK_COMMIT),
            ASTSourcePin(repository=SIGILFLOW_REPO, commit="feature-branch-occurrence"),
        ),
        nodes=fresh_nodes,
    )


def normalize_and_renormalize(kernel: SigilFlowKernel, *, epoch: int | None = None) -> RenormalizedAST:
    return renormalize_ast(normalize_kernel_ast(kernel), epoch=epoch)


__all__ = [
    "AST_SCHEMA_ID",
    "ASTSourcePin",
    "ASTNode",
    "ASTEdge",
    "NormalizedAST",
    "RenormalizedAST",
    "normalize_kernel_ast",
    "renormalize_ast",
    "normalize_and_renormalize",
]

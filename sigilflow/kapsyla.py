from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

KAPSYLA_SCHEMA_ID = "SIGILFLOW_KAPSYLA_RENORMALIZED_KERNEL_V1"
SIGILBOOK_KAPSYLA_COMMIT = "e21451ae9bb50af2ffee1756d7bace4592365592"
STRICT = ConfigDict(extra="forbid", frozen=True, strict=True, validate_default=True)


class KapsylaReceipt(BaseModel):
    model_config = STRICT
    schema_id: Literal[KAPSYLA_SCHEMA_ID] = KAPSYLA_SCHEMA_ID
    source_kernel: str = Field(min_length=1)
    normalized_projection_digest: str = Field(min_length=1)
    renormalized_occurrence_digest: str = Field(min_length=1)
    fresh_bearer: bool = True
    pacapdg_admitted: bool = True
    uap_admitted: bool = True
    safe_replay_receipt: bool = True
    projection_preserved: bool = True
    bearer_preserved: Literal[False] = False
    identity_transport: Literal[False] = False
    authority_transport: Literal[False] = False
    scheduler_transport: Literal[False] = False
    runtime_transport: Literal[False] = False
    kapsyla_sealed: bool = True

    @model_validator(mode="after")
    def validate_seal(self):
        if not (self.pacapdg_admitted and self.uap_admitted and self.safe_replay_receipt):
            raise ValueError("KAPSYLA_REQUIRES_PACAPDG_UAP_SAFE_REPLAY")
        if self.normalized_projection_digest == self.renormalized_occurrence_digest:
            raise ValueError("NORMALIZE_AND_RENORMALIZE_MUST_REMAIN_DISTINCT")
        if not self.fresh_bearer:
            raise ValueError("KAPSYLA_REQUIRES_FRESH_BEARER")
        return self


def seal_kapsyla(*, source_kernel: str, projection_digest: str, occurrence_digest: str) -> KapsylaReceipt:
    return KapsylaReceipt(
        source_kernel=source_kernel,
        normalized_projection_digest=projection_digest,
        renormalized_occurrence_digest=occurrence_digest,
    )


__all__ = ["KAPSYLA_SCHEMA_ID", "SIGILBOOK_KAPSYLA_COMMIT", "KapsylaReceipt", "seal_kapsyla"]

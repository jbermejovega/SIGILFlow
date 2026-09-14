# SIGILFlow

`SIGILFlow` is a typed programming-library kernel for computational and semantic flows sourced from:

- `mbenitezzs31-cloud/TFG` — quantum simulation / optimization / tensor-network experiment sources;
- `jbermejovega/sigilbook` — SIGIL/PACA kernel semantics, PoetryType, PACAPDG, UAP and Safe Replay.

The repository history begins from the upstream TFG source commit and preserves that provenance. The new `sigilflow/` package adds a source-bound presheaf/sheaf-preimage layer and a join/meet fusion kernel without treating either source repository as identical to the fusion carrier.

## Canonical kernel

```text
TFG local sections ---------\
                            >-- PRESHEAF / SHEAF PREIMAGE
SIGILBOOK local sections ---/          |
                                       v
                              JOIN / MEET FUSION
                                       |
                                       v
                                  SIGILFlow
                                       |
                      PACAPDG -> UAP -> SAFE_REPLAY
```

The source pins for V1 are:

```text
mbenitezzs31-cloud/TFG@3f06c29063334e42d97218355adf02118d794a40
jbermejovega/sigilbook@1ac6415d83adcde8d17df06f94fa324dd96acbce
```

## Flow-library registry

The first-class adapters cover:

- OpenQAOA
- Qibo
- Quimb
- Quantum-Circuit-Simulator-DMRG
- RQAOA
- TensorCircuit
- Cirq
- PennyLane
- PoetryKernel
- PACAPDG

Each adapter is source-bound and typed by capability. Routing a flow selects compatible adapters, but does not imply semantic equivalence between libraries.

## Sync policy

V1 intentionally uses `PINNED_READ_VALIDATE` rather than automatic GitHub workflow mutation:

```text
auto_pull  = false
auto_merge = false
auto_push  = false
diff_before_update = true
human_review_required = true
```

This keeps source updates observable while the wider SIGILBOOK Actions surface is experiencing startup failures. No Actions workflow is added by this kernel PR.

## Laws

```text
MEET != IDENTITY_INTERSECTION
JOIN != FLATTEN
FUSION_BEARER != SOURCE_BEARER
SOURCE_PIN != AUTHORITY_TRANSPORT
SAME_PROJECTION != SAME_BEARER
PACAPDG < UAP < SAFE_REPLAY
PLURA_MANENT
PIORNALEGO_ES_CANON
```

See `docs/SIGILFLOW_PRESHEAF_SHEAF_PREIMAGE_KERNEL_FUSION_V1.md`.

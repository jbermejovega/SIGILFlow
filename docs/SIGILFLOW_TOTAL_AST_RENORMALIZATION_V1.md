# SIGILFLOW_TOTAL_AST_RENORMALIZATION_V1

Root: `SIGILFLOW_PRESHEAF_SHEAF_PREIMAGE_KERNEL_FUSION_V1`

## Purpose

Normalize the fused TFG/SIGILBOOK flow AST into a stable semantic projection, then renormalize that projection into a fresh occurrence for the next epoch without collapsing source identity, QUNO context, provenance, or admission boundaries.

## Source pins

- `mbenitezzs31-cloud/TFG@3f06c29063334e42d97218355adf02118d794a40`
- `jbermejovega/sigilbook@1ac6415d83adcde8d17df06f94fa324dd96acbce`

The source repositories are read/source-bound. Renormalization never rewrites those pins.

## Normalize

`NORMALIZE(K)` sorts local sections by stable semantic coordinates `(repo, path, QUNO, section_id)` and projects each section into an AST node while preserving its original bearer.

`NORMALIZE` therefore produces a canonical projection, not a new occurrence.

## Renormalize

`RENORMALIZE(NF(K), e+1)` creates a fresh occurrence with:

- fresh node IDs;
- fresh bearers;
- fresh occurrence digest;
- advanced epoch;
- the same normalized projection digest;
- the same source pins and provenance boundary.

Hence:

```text
NORMALIZE != RENORMALIZE
same projection != same bearer
fixed projection != fixed occurrence
```

## Admission spine

The normalized AST explicitly preserves:

```text
PoetryKernel -> PACAPDG -> UAP -> SAFE_REPLAY
```

No normalization or renormalization step may bypass this ordering.

## Join/meet interaction

The AST is built after the typed presheaf/sheaf-preimage fusion:

```text
TFG presheaf ----\
                  > sheaf preimage -> JOIN/MEET -> NORMALIZE -> RENORMALIZE
SIGILBOOK presheaf-/
```

with hard laws:

```text
MEET != IDENTITY_INTERSECTION
JOIN != FLATTEN
FUSION_BEARER != SOURCE_BEARER
IDENTITY_TRANSPORT = FALSE
AUTHORITY_TRANSPORT = FALSE
```

## DMRG alignment boundary

The TFG source motivates controlled compression through MPS/DMRG, SVD truncation, bond dimension and sweeps. SIGILFlow borrows the engineering pattern of controlled local compression and iterative refinement for dependency/RAG state, but does not identify a software dependency AST with a physical MPS or quantum state.

## Canon

`PLURA MANENT · PIORNALEGO ES CANON.`

# SIGILFLOW_PRESHEAF_SHEAF_PREIMAGE_KERNEL_FUSION_V1

`SIGILFlow` is the fusion carrier between two source-bound repositories:

- `mbenitezzs31-cloud/TFG@3f06c29063334e42d97218355adf02118d794a40` — computational flow/library source;
- `jbermejovega/sigilbook@1ac6415d83adcde8d17df06f94fa324dd96acbce` — semantic/kernel/admission source.

The current SIGILFlow history starts from the same upstream TFG commit, so the original computational files retain their upstream history. The new kernel layer does not rewrite that provenance.

## Presheaf

Each library or semantic kernel surface is represented as a local section:

```text
F(U) = Section[path, repo, QUNO, epoch, bearer]
```

The initial cover includes OpenQAOA, Qibo, Quimb, the DMRG simulator notebook tree, RQAOA, TensorCircuit, Cirq and PennyLane from the TFG source, together with PoetryKernel, PACAPDG, UAP and SAFE_REPLAY from SIGILBOOK.

A restriction map is typed and provenance-preserving. No restriction map may silently identify its source and target bearers.

## Sheaf preimage

SIGILFlow is modeled as a preimage/gluing carrier over those source sections:

```text
TFG presheaf --------\
                      >-- preimage/glue --> SIGILFlow kernel
SIGILBOOK presheaf --/
```

A global section is admitted only from compatible local witnesses. Gluing is not identity merge.

## Kernel fusion join / meet

The meet is the common interface needed to compose the two sources:

```text
TFG ∧ SIGILBOOK = {
  typed_flow_interface,
  dependency_provenance,
  epoch_lineage,
  python_notebook_surface
}
```

The join is the larger flow-kernel carrier:

```text
TFG ∨ SIGILBOOK = {
  quantum_flow_libraries,
  poetry_kernel_semantics,
  PACAPDG,
  UAP,
  SAFE_REPLAY
}
```

with hard laws:

```text
MEET != IDENTITY_INTERSECTION
JOIN != FLATTEN
FUSION_BEARER != SOURCE_BEARER
SOURCE_PIN != AUTHORITY_TRANSPORT
```

## Sync model

`SYNC` means `PINNED_READ_VALIDATE`, not automatic merging.

The kernel records exact source commits, computes/inspects diffs before accepting a new pin, and requires human review. Automatic pull, merge and push are false by default. This is deliberate while repository Actions are exhibiting startup failures: synchronization must remain observable and source-bound rather than depending on a large implicit GitHub Actions surface.

## Programming-library kernel

SIGILFlow is intended to become the programming-library kernel for flow implementations across the two repositories. The first library set is:

```text
OpenQAOA
Qibo
Quimb
Quantum-Circuit-Simulator-DMRG
RQAOA
TensorCircuit
Cirq
PennyLane
PoetryKernel
PACAPDG
UAP
SAFE_REPLAY
```

Adapters can be added as fresh typed sections. A library adapter may translate data or flow descriptions but may not assert semantic equivalence without an explicit witness.

## Admission

The canonical effect boundary remains:

```text
FLOW CANDIDATE -> PACAPDG -> UAP -> SAFE_REPLAY
```

A successful Python import, notebook execution or flow-library result is not by itself a UAP admission receipt.

**PRESHEAF LOCALIZES · SHEAF GLUES · MEET SHARES INTERFACE · JOIN BUILDS THE FLOW KERNEL · PLURA MANENT · PIORNALEGO ES CANON.**

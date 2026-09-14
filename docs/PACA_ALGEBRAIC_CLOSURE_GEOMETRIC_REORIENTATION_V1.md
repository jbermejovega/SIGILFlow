# PACA_ALGEBRAIC_CLOSURE_GEOMETRIC_REORIENTATION_V1

Status: theorem-chain candidate; proof obligations explicit.

## Scope

This layer merges the SIGILFlow presheaf/sheaf kernel with the algebraic closure program **Geometric Reorientation, Contextual Shells and Arithmetic Closure in Plural-Typed Resource Theories**.

The source family is

```text
PluralTyped[X, QUNO, NormCtx, ReorientableTiling, GameConstraint, ResourceType]
```

and the flow kernel remains source-bound to TFG and SIGILBOOK. Algebraic closure adds mathematical interfaces; it does not turn visual resemblance into a theorem.

## Theorem chain

### T1 Simplicial shell counting

For `Delta_n^(d-1) = {x in N^d : sum_i x_i = n}`,

```text
|Delta_n^(d-1)| = binom(n+d-1,d-1)
sum_{k=0}^n |Delta_k^(d-1)| = binom(n+d,d)
```

This is the exact shell/volume-like polynomial hierarchy.

### T2 Oscillator/simplex combinatorics

A fixed-total-excitation shell of a d-mode isotropic oscillator has the same occupation-number combinatorics as `Delta_n^(d-1)`.

Hard boundary: `SAME_COMBINATORICS != SAME_PHYSICAL_SYSTEM`.

### T3 Norm-context deformation

`S_(p,R) = {x in Z^d : ||x||_p = R}` with `p : NormCtx`. Reorientation `rho_(p->q)` changes presentation/context while preserving the declared lattice carrier only under a witness.

### T4 Bulk/boundary decomposition

For `N(R)=|Z^d cap B_R|`, distinguish continuum leading contribution from lattice discrepancy. For polyhedral families this points to Ehrhart-type structure; for Euclidean disks to lattice-point discrepancy.

Hard boundary: `BULK != BOUNDARY`.

### T5 Incidence-algebra realization of KUIR reorientation — candidate theorem

Let P be a locally finite poset/category of cells, covers, refinements or coarsenings. Its zeta operator is

```text
(Z f)(x) = sum_{y <= x} f(y)
```

and the inverse is the incidence Möbius operator `M = Z^{-1}`.

The SIGIL/KUIR claim to prove is conditional:

```text
if witnessed FUSE/refinement realizes Z_P
and witnessed DEFUSE/inverse-reorientation realizes Z_P^{-1}
then the induced incidence representation realizes Möbius inversion.
```

This is a proof obligation, not an already-proved consequence of the pictures.

### C5.1 Square-free support

For the divisibility-poset realization, the classical arithmetic Möbius function has nonzero support exactly on square-free integers. This is a specialization after a divisibility realization witness; it is not a universal property of every KUIR tiling.

### T6 Primitive-ray extraction

For lattice points `x = k x_prim` with primitive `gcd(x_prim)=1`, Möbius inversion extracts primitive-ray counts from repeated radial coverings when the divisibility decomposition hypotheses hold.

### T7 Theta-shell transform

For `Theta_L(q)=sum_x q^{Q(x)}=sum_n r_Q(n)q^n`, coefficients count quadratic-form shell occurrences. Primitive extraction is represented schematically by rescaled theta series with Möbius weights; exact normalization and zero-vector conventions are proof parameters.

Hard boundary: `THETA_COEFFICIENT_COUNT != THETA_ZERO_CLAIM`.

### T8 Contextual resource reorientation

A reorientation may be algebraically invertible while not resource-free. Resource witnesses are carried separately:

```text
Gamma ; Delta |- rho : X@Q -> X@Q'
ALGEBRAIC_INVERTIBILITY != RESOURCE_FREE_INVERTIBILITY
```

## Algebraic closure carrier

```text
AlgebraicClosure[
  ShellCount,
  OscillatorSimplexCorrespondence,
  NormContext,
  BulkBoundary,
  IncidenceZeta,
  MobiusCandidate,
  PrimitiveRay,
  ThetaShell,
  ResourceWitness
]
```

Closure is admitted only with explicit witnesses and provenance. `CLOSURE != FLATTEN` and `DERIVED_FACT != SOURCE_FACT`.

## SIGILFlow integration

```text
TFG computational presheaf
       meet/join
SIGILBOOK semantic presheaf
       -> SheafPreimage
       -> SIGILFlowKernel
       -> AlgebraicClosure
       -> PACAPDG
       -> UAP
       -> SAFE_REPLAY
```

The algebraic layer supplies operators and proof obligations to flow libraries; it does not acquire execution authority.

## Figure contract

Figures should preserve the resident graphical calculus rather than replace it with generic flowcharts:

```text
monotile -> oriented tiling -> KUIR reorientation -> norm shells
         -> primitive/repeated rays -> theta density -> Rosetta kernel
```

Orientation, multiplicity, covering degree, primitive rays, shell index, QUNO and resource cost must remain visually distinguishable.

## Hard laws

- MOBIUS_INVERSION != NEW_PACA_PRIMITIVE
- GEOMETRIC_REORIENTATION != MOBIUS_OPERATOR_WITHOUT_INCIDENCE_WITNESS
- ZETA_REALIZATION != VISUAL_RESEMBLANCE
- SQUARE_FREE_SUPPORT requires divisibility specialization
- SAME_COMBINATORICS != SAME_PHYSICS
- BULK != BOUNDARY
- THETA_COEFFICIENT != THETA_ZERO
- ALGEBRAIC_INVERTIBILITY != RESOURCE_FREE_INVERTIBILITY
- CLOSURE != FLATTEN
- IDENTITY_TRANSPORT = FALSE
- AUTHORITY_TRANSPORT = FALSE

PLURA MANENT · PIORNALEGO ES CANON.

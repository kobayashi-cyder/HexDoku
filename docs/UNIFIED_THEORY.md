# Unified Theory Research Framework

This is the canonical research note for the unified-theory direction associated with HexDoku.

**Status: exploratory and falsifiable research framework, not an established physical theory.**

The purpose is to keep three layers separate:

1. **Established physics** — results already supported by standard mechanics, statistical mechanics, quantum theory, quantum field theory, and general relativity.
2. **Structural interpretation** — a common language based on degrees of freedom, symmetry, conservation, coarse-graining, closure, connection, and curvature.
3. **New hypothesis** — claims that would require derivation and experimental discrimination from existing theories.

The central working pipeline is:

~~~text
deeper degrees of freedom
    ->
admissible transformations + conservation
    ->
symmetry / redundancy
    ->
coarse-graining
    ->
effective variables
    ->
closure, memory, noise, transport
    ->
effective laws
~~~

A candidate unification succeeds only if it derives known structures with fewer independent assumptions and produces new quantitative predictions.

For experimental targets and residual tests, see [UNIFIED_THEORY_OBSERVABLES.md](UNIFIED_THEORY_OBSERVABLES.md).

---

## Candidate unified-theory hypothesis: relational inertia, derived time, and emergent gravity

The current HexDoku development has reached a point where a **candidate unification hypothesis can be stated clearly enough to test**, even though it is not yet a demonstrated unified physical theory.

The hypothesis is:

> **Time, inertia, geometry, and gravity may be effective structures emerging from a deeper relational state system rather than four independent fundamental primitives.**

A minimal schematic form is:

~~~text
Deep relational state
        |
        +--> persistence / inertial structure
        |
        +--> ordering / change accumulation
        |        |
        |        +--> derived time
        |
        +--> comparison between local inertial descriptions
                 |
                 +--> connection
                          |
                          +--> curvature
                                   |
                                   +--> effective gravity
~~~

### 1. Fundamental layer

Do not assume spacetime at the deepest level.

Start instead from:

~~~text
R = relations between states
I = persistence / inertial structure
Delta = admissible change
P = uncertainty / amplitude structure where required
C = causal / ordering structure where required
~~~

The fundamental object is therefore not initially:

~~~text
X(x,y,z,t)
~~~

but a relational system:

~~~text
{states, relations, admissible transformations}
~~~

### 2. Derived time

Time is treated as a reconstructed ordering / accumulation parameter rather than an assumed primitive coordinate.

Conceptually:

~~~text
relations
+ distinguishable change
+ persistent identity
+ ordering
+ clock construction
    ->
effective time
~~~

Write:

~~~text
tau = T(R, I, Delta, O, memory / ordering structure)
~~~

where tau is an effective or observed temporal coordinate.

This does not yet prove that physical time is emergent; it defines a testable route for attempting to reconstruct time from deeper variables.

### 3. Local inertial nulling

A key requirement is that a local description can exist in which the observer's proper acceleration is zero.

Conceptually:

~~~text
local inertial evaluation = 0
~~~

while the global gravitational structure need not vanish.

This mirrors the equivalence-principle structure of general relativity: a freely falling observer can locally recover gravity-free special-relativistic physics, while tidal effects remain across a finite region.

Reference:
- Einstein Online, "equivalence principle": https://www.einstein-online.info/en/explandict/equivalence-principle/
- Einstein Online, "Gravity: from weightlessness to curvature": https://www.einstein-online.info/en/spotlight/geometry_force/

### 4. Bridge / connection between local inertial descriptions

If each local region has its own inertial description, comparing neighboring descriptions requires a transport rule.

Introduce a connection:

~~~text
D_a = partial_a + Gamma_a
~~~

where Gamma_a describes how a local state / frame is compared across the underlying relational space.

The important quantity is then not Gamma alone, but failure of successive transports to commute:

~~~text
Omega_ab = [D_a, D_b]
~~~

If:

~~~text
Omega_ab = 0
~~~

then a globally consistent inertial comparison may be possible over that region.

If:

~~~text
Omega_ab != 0
~~~

then transport depends on path / ordering, producing effective curvature.

The hypothesis identifies this nontrivial curvature with the structure that appears macroscopically as gravity.

### 5. Gravity as emergent relational curvature

The strongest current candidate statement is:

~~~text
Gravity
  != necessarily a fundamental force field

Gravity
  ~ curvature of the relational / inertial connection
    after coarse-graining into effective spacetime
~~~

This is deliberately compatible with the successful geometric content of general relativity.

It does not replace Einstein gravity unless the low-energy limit recovers the Einstein field equations.

### 6. Time and gravity as co-emergent structures

Rather than:

~~~text
fundamental time
+ fundamental gravity
~~~

the proposed hierarchy is:

~~~text
deeper relational structure
       |
       +--> persistence / inertia
       |
       +--> ordering / clock structure
       |         |
       |         +--> effective time
       |
       +--> local-frame comparison
                 |
                 +--> effective geometry
                           |
                           +--> effective gravity
~~~

Thus the current hypothesis is:

> **time and gravity are co-emergent manifestations of deeper relational-inertial structure.**

### 7. Role of the graviton

The hypothesis does **not** require a fundamental graviton.

However, it also does not imply that graviton-like excitations cannot exist.

A possible hierarchy is:

~~~text
fundamental relational degrees of freedom
        |
        v
coarse-grained effective geometry
        |
        v
small gravitational perturbation
        |
        v
quantized effective excitation
        |
        v
graviton-like mode
~~~

Therefore the distinguishable claims are:

~~~text
A. fundamental graviton exists
B. no fundamental graviton exists, but an effective spin-2 excitation emerges
C. no graviton-like quantum excitation exists
~~~

The current hypothesis favors investigating B, but does not yet establish it.

### 8. Candidate unified structure

A compact form is:

~~~text
Fundamental:
  (R, I, Delta, P, C)

Derived:
  tau      = TimeMap(R, I, Delta, ...)
  Gamma    = Connection(R, I, ...)
  Omega    = Curvature(Gamma)
  g_eff    = GeometryMap(Omega, ...)
  gravity  = EffectiveDynamics(g_eff, matter, ...)
~~~

The central derivation target is therefore:

~~~text
(R, I, Delta, P, C)
    ->
(tau, Gamma, Omega)
    ->
effective spacetime
    ->
general-relativistic limit
~~~

### 9. What would make this a real unified theory?

The hypothesis becomes physically serious only if it passes explicit tests.

At minimum it must:

1. recover local Lorentz symmetry to experimental accuracy,
2. recover the equivalence principle,
3. recover gravitational redshift and proper-time behavior,
4. recover geodesic motion,
5. recover tidal gravity / curvature,
6. recover the Einstein field equations or a quantitatively equivalent low-energy limit,
7. reproduce gravitational-wave propagation,
8. connect consistently to quantum theory,
9. explain how matter / gauge fields inhabit the same underlying relational system,
10. produce at least one falsifiable prediction not inserted by construction.

Failure of these requirements is evidence against the hypothesis.

### 10. Stronger falsification criteria

The hypothesis should be rejected or substantially revised if it cannot derive, without ad hoc insertion:

~~~text
universality of free fall
local Lorentz invariance
inverse-square Newtonian limit
observed gravitational redshift
light deflection
perihelion / orbital relativistic corrections
gravitational-wave speed and polarization constraints
known quantum interference results
known gauge symmetries / Standard Model structure
~~~

A framework that merely re-labels these known laws after inserting them manually is a representation language, not a unified physical theory.

### 11. Current status

The project should therefore describe the result as:

> **a candidate relational-inertia unification hypothesis embedded in the HexDoku / Unified Reconstruction Algebra, not a completed Theory of Everything.**

What has been achieved conceptually:

~~~text
time can be moved from input variable to reconstruction target
gravity can be represented as curvature of inter-frame comparison
local inertial nulling and global curvature can coexist
BridgeDoku can be interpreted as a connection
Doku non-commutativity can represent curvature
scale / coarse-graining can generate effective spacetime descriptions
a fundamental graviton is no longer logically mandatory
~~~

What remains open:

~~~text
derive the actual connection from microscopic rules
derive the effective metric
derive Einstein dynamics
derive quantum structure
derive matter and gauge sectors
establish uniqueness
produce new falsifiable predictions
compare quantitatively with observation
~~~

The correct current claim is therefore:

> **A plausible unification hypothesis may have emerged, but its status now depends entirely on derivation and falsification rather than further naming or analogy.**

---

## Addendum: coarse-graining, conservation, memory, and effective inertia

The current unification hypothesis should also preserve a stricter distinction between microscopic dynamics and macroscopic effective laws.

### 1. Microscopic-to-macroscopic continuity requires coarse-graining

The macroscopic description is not assumed to be a literal magnified copy of the microscopic description.

Conceptually:

~~~text
microscopic state
    ->
coarse-graining / information reduction
    ->
effective macroscopic state
~~~

A macroscopic variable is therefore treated as a compressed description of many compatible microscopic states.

Examples:

~~~text
microscopic coordinates / momenta
    -> temperature

microscopic collisions
    -> pressure / viscosity

microscopic correlations
    -> memory / hysteresis / relaxation structure
~~~

The continuity is physical, but the description changes with scale.

### 2. Conservation rather than "force immortality"

The framework should not assume that force itself is conserved.

Instead, the physically stronger starting point is conservation of appropriate quantities in the relevant closed-system limit.

Conceptually:

~~~text
input energy / momentum / charge / other conserved quantity
    ->
redistribution among available degrees of freedom
    ->
different observable channels
~~~

Apparent conversion loss is therefore first interpreted as redistribution into unresolved or less-useful degrees of freedom, not disappearance.

A schematic energy accounting is:

~~~text
E_total
  =
E_observed
+ E_internal
+ E_field
+ E_thermal
+ E_unresolved
~~~

Any claimed anomaly must first close this accounting as far as experimentally possible.

### 3. Coarse-graining can generate memory and fluctuations together

If microscopic degrees of freedom are removed from the explicit description, their influence may re-enter the effective equation as memory and noise.

A generic candidate form is:

~~~text
dx/dt
  =
F[x(t)]
+ integral K(t - t') x(t') dt'
+ xi(t)
~~~

where:

~~~text
K   = memory kernel
xi  = effective fluctuation / unresolved-degree contribution
~~~

This makes "history dependence" an expected effective phenomenon in many systems without requiring a new fundamental history field.

Examples that motivate this distinction include:

~~~text
hysteresis
viscoelastic response
glassy relaxation
non-Markovian open-system behavior
Mpemba-like preparation dependence
~~~

### 4. New history degrees of freedom require a stronger test

Preparation history alone is not evidence for a new field.

The stronger criterion is:

~~~text
same presently resolved state
+ different preparation history
    ->
reproducibly different future behavior
~~~

after all known internal variables, non-equilibrium modes, environmental couplings, and statistical fluctuations have been controlled as far as possible.

Only then should an additional hidden or history-carrying degree of freedom be introduced.

### 5. Effective inertia hypothesis

A stronger current candidate is:

> **inertia may be an effective response emerging after coarse-graining deeper degrees of freedom, rather than a primitive force-like entity transmitted through a separate medium.**

The standard relation:

~~~text
F = m a
~~~

is therefore treated as a possible effective law to be derived in the appropriate scale and regime.

The derivation target becomes:

~~~text
fundamental / deeper dynamics
    ->
coarse-graining
    ->
effective inertial response
    ->
F = m a in the validated limit
~~~

Possible deviations should be sought as:

~~~text
memory dependence
nonlocality
scale dependence
response-rate dependence
anomalous fluctuation structure
~~~

rather than by assuming an arbitrary new force.

### 6. Dark-matter caution

The simple hypothesis:

~~~text
dark-matter-like effects
  =
ordinary matter plus a delayed inertial / gravitational response
~~~

should not be treated as a leading branch.

Simple propagation delay, simple time-only memory, or a gravitational field that merely tracks earlier baryonic positions do not naturally reproduce the combined observational constraints from galaxy dynamics, lensing, colliding clusters, the CMB, and structure formation.

If a modified-inertia or memory theory is retained, it must independently reproduce all of those observations with one consistent rule set.

Adding enough new field content to do so may amount physically to introducing a new dark degree of freedom under another description.

### 7. Unified-theory methodological principle

The preferred hierarchy is now:

~~~text
fundamental degrees of freedom
    ->
conservation / admissible transformations
    ->
coarse-graining
    ->
effective variables
    ->
memory + fluctuations + transport
    ->
effective inertia / geometry / thermodynamics / other laws
~~~

The central research question is therefore not:

> "What single force explains everything?"

but rather:

> **"What minimal deeper dynamics, under scale-dependent coarse-graining, generates the observed effective laws while preserving the required symmetries, conservation laws, and falsifiable predictions?"**

### 8. Falsification discipline

New entities should not be introduced while known unresolved degrees of freedom can explain the observation.

A candidate extension becomes scientifically meaningful only when it predicts a measurable residual such as:

~~~text
unexpected memory after full state matching
nonlocal response not reducible to known transport
scale-dependent inertia outside existing theory
fluctuation spectra inconsistent with known baths / couplings
a quantitatively new cross-domain relation
~~~

The intended principle is:

> **Known degrees of freedom first; new degrees of freedom only after reproducible residuals remain.**

This addendum is part of the candidate unified-theory research direction, not evidence that the theory has been established.

---

## Standard-Model bridge: what is established and what remains to derive

The Standard Model should currently be treated as a highly successful quantum field theory whose observed gauge structure is:

~~~text
SU(3)_C x SU(2)_L x U(1)_Y
~~~

The present framework does **not** derive this group yet.

A genuine derivation must explain, without inserting them by hand:

~~~text
why SU(3)_C
why SU(2)_L
why U(1)_Y
why the observed fermion representations
why chirality is asymmetric in the weak interaction
why there are three generations
why the observed hypercharges are what they are
why Higgs/Yukawa structure has its observed form
~~~

### Gauge symmetry is not itself a field

A group such as SU(2) is a set of allowed transformations.

For a two-component complex state:

~~~text
psi = (a, b)^T
~~~

preservation of the Hermitian norm:

~~~text
|a|^2 + |b|^2
~~~

naturally admits U(2) transformations.

Imposing determinant one selects SU(2).

Strictly:

~~~text
U(2) ~= [SU(2) x U(1)] / Z_2
~~~

rather than a simple direct product.

This mathematical fact alone does **not** explain the electroweak gauge group. It only shows how SU(2)-type structure can arise from norm-preserving transformations of a two-component complex state.

### Local symmetry introduces a connection

If the allowed transformation is global:

~~~text
psi(x) -> U psi(x)
~~~

no gauge field is required merely to state the symmetry.

If the transformation may vary with position:

~~~text
psi(x) -> U(x) psi(x)
~~~

ordinary derivatives no longer transform covariantly.

Introduce a connection:

~~~text
D_mu = partial_mu - i g A_mu
~~~

For SU(2):

~~~text
A_mu = A_mu^a T_a
a = 1,2,3
~~~

because the Lie algebra su(2) has three generators.

The associated curvature / field strength is schematically:

~~~text
F_mu_nu
  =
partial_mu A_nu
- partial_nu A_mu
- i g [A_mu, A_nu]
~~~

Thus the physically meaningful sequence is:

~~~text
state space
    ->
transformation symmetry
    ->
local redundancy
    ->
connection
    ->
curvature / gauge field strength
~~~

This parallels, but does not identify, the role of connection and curvature in spacetime geometry.

---

## Spin SU(2) and weak SU(2)_L must remain distinct

Two different physical uses of SU(2) appear here.

### Spin / Lorentz structure

Spatial rotations are described by SO(3), while spin-1/2 states transform under its double cover SU(2).

A spinor can acquire a minus sign under a 2-pi rotation and return to itself after 4-pi.

Relativistically, the proper Lorentz group is related to SL(2,C), and left/right Weyl spinors transform as:

~~~text
(1/2, 0)
(0, 1/2)
~~~

This is the correct mathematical setting for chirality of relativistic spinors.

### Weak internal gauge structure

The Standard Model SU(2)_L is an internal gauge symmetry acting on weak-isospin multiplets.

It is not simply the same SU(2) as spatial spin.

Therefore the heuristic route:

~~~text
propagation + rotation -> helicity
~~~

is useful only as intuition.

It does **not** derive the weak SU(2)_L interaction.

A real unification must explain why spinorial Lorentz structure and internal weak gauge structure coexist and whether they arise from a deeper common architecture without conflating them.

---

## Propagation, helicity, chirality, and the limit of the torque analogy

Adding an axial rotational degree of freedom to a propagating classical mode can generate right- and left-handed helical modes.

Schematically:

~~~text
propagation
+ axial rotation
+ coupling
    ->
right/left helical eigenmodes
~~~

This is physically meaningful in classical wave systems.

However:

~~~text
classical torsional wave
!=
spin-1/2 particle
~~~

Spin-1/2 requires spinor representation structure, not merely mechanical torque.

For massless Weyl fields, helicity and chirality align.

For massive fermions, helicity and chirality are distinct concepts.

Therefore the theory must not promote the torque analogy into a derivation unless it reproduces the correct Lorentz representation and spin-statistics structure.

---

## Degrees of freedom: growth, constraint, coarse-graining, reorganization

A useful structural rule is:

~~~text
composition
    -> raw state space grows

constraints / conservation / gauge redundancy
    -> physical degrees of freedom are reduced

coarse-graining
    -> microscopic variables are hidden

collective organization
    -> new effective modes appear
~~~

For N independent d-state quantum subsystems:

~~~text
dim(H) = d^N
~~~

so state-space dimension grows multiplicatively, while its logarithm grows additively:

~~~text
log dim(H) = N log d
~~~

This distinguishes the number of possible states from an additive information measure.

A rough constrained counting principle is:

~~~text
physical DOF
=
raw DOF
- independent constraints
- gauge redundancies
~~~

with the warning that gauge theories and field theories require careful Hamiltonian / constraint counting rather than naive subtraction.

The unification problem is therefore not "why do degrees of freedom only increase?"

The more useful cycle is:

~~~text
generation
-> constraint
-> identification
-> coarse-graining
-> reorganization
-> effective mode
~~~

Particles may then be investigated as stable propagating excitations of an effective state space, but that statement is only a research direction until the correct quantum field structure is derived.

---

## Why the next problem is the origin of a two-component complex state

The immediate next question is:

> Why should the minimal relevant state be a two-component complex object at all?

This must not be assumed merely because SU(2) is desired.

The comparison should begin from simpler candidate state spaces:

~~~text
R^1        one real component
R^2        two real components
C^1        one complex component
C^2        two complex components
~~~

and ask what new structures first become possible at each stage.

### R^1

Allows magnitude / sign but no continuous internal phase or nontrivial two-state mixing.

### R^2

Allows planar rotations SO(2), equivalent to one continuous angular degree of freedom.

### C^1

Allows a phase:

~~~text
psi -> exp(i theta) psi
~~~

with U(1)-type norm-preserving symmetry.

This is already sufficient for a continuous phase degree of freedom, but not for a non-Abelian two-component mixing group.

### C^2

Allows norm-preserving mixing of two complex amplitudes:

~~~text
psi -> U psi
U in U(2)
~~~

and contains noncommuting SU(2) transformations.

This is the first item in this simple ladder that simultaneously supplies:

~~~text
relative phase
two-state mixing
non-Abelian continuous transformations
spinor-compatible two-component mathematics
Bloch-sphere / projective-state geometry
~~~

But this observation is still **selection by mathematical capability**, not a physical derivation.

The real task is to identify a more primitive physical principle that forces C^2 or an equivalent structure.

Candidate principles to test include:

~~~text
composition consistency
continuous reversible transformations
probability / norm preservation
locality
Lorentz covariance
existence of binary alternatives
noncommuting observables
minimal faithful spinor representation
~~~

A successful derivation would show that a simpler state space fails one or more required physical conditions, while C^2 is the minimal surviving structure.

---

## Projective state space and why global phase matters

For a normalized two-component complex state:

~~~text
psi in C^2
<psi|psi> = 1
~~~

an overall phase:

~~~text
psi -> exp(i alpha) psi
~~~

does not change the physical pure state in ordinary quantum mechanics.

Therefore the physical pure-state space is not simply C^2.

After normalization and phase identification it is:

~~~text
CP^1
~~~

which is geometrically equivalent to the two-sphere S^2.

This is the Bloch sphere for a two-level quantum system.

That means a useful structural chain is:

~~~text
C^2
-> norm constraint
-> quotient by global U(1) phase
-> CP^1 ~= S^2
~~~

This is one place where:

~~~text
constraint
+ identification
~~~

produces a lower-dimensional physical state space from a larger raw state space.

It is therefore directly relevant to the broader coarse-graining / quotient-space language of this project.

---

## What would count as a real derivation of SU(2)

The following would **not** be enough:

~~~text
assume two complex amplitudes
observe that SU(2) acts on them
declare SU(2) fundamental
~~~

That simply inserts the desired structure.

A stronger derivation must begin with physically motivated axioms that do not name SU(2), then show that the allowed reversible transformations are isomorphic to SU(2) or contain it uniquely.

A candidate derivation program is:

~~~text
1. define minimal state information
2. require continuous reversible transformations
3. require a conserved probability / norm
4. define composition of subsystems
5. require local causal consistency
6. require relativistic transformation consistency where applicable
7. classify the allowed transformation groups
8. test whether SU(2) appears uniquely or only as one arbitrary choice
~~~

If many groups satisfy the same axioms, the derivation is incomplete.

---

## Toward the Standard Model: the actual hard test

The strongest next-stage target is not merely to obtain SU(2).

It is to derive:

~~~text
SU(3)_C x SU(2)_L x U(1)_Y
~~~

together with the observed representations and anomaly cancellation.

The current project should therefore treat the following as mandatory checkpoints:

~~~text
[ ] derive or strongly constrain the primitive state space
[ ] derive the relevant transformation group
[ ] distinguish spacetime and internal symmetry
[ ] derive local connection structure
[ ] derive gauge curvature / dynamics
[ ] derive fermionic representation content
[ ] recover chirality
[ ] recover observed charge assignments
[ ] explain or constrain three generations
[ ] recover Standard-Model interactions
[ ] recover GR or its tested low-energy limit
[ ] produce a new falsifiable prediction
~~~

Until these are met, the framework is a unification research program rather than a unified physical theory.

---


---

## Higgs sector: vacuum geometry, degrees of freedom, and particle excitations

The Standard Model Higgs field is a complex SU(2)_L doublet:

~~~text
H in C^2
~~~

so it contains four real field degrees of freedom.

A convenient schematic decomposition is:

~~~text
4 real Higgs-field DOF
    ->
3 angular / broken-symmetry directions
+
1 radial direction
~~~

After electroweak symmetry breaking:

~~~text
SU(2)_L x U(1)_Y
    ->
U(1)_EM
~~~

three generators are broken. Correspondingly, three Goldstone directions are absorbed into the longitudinal polarizations of:

~~~text
W+
W-
Z
~~~

The remaining independent scalar excitation is the physical Higgs boson.

Thus the physical reorganization is:

~~~text
4 Higgs-field DOF
    ->
3 Goldstone DOF + 1 radial DOF
    ->
W_L+, W_L-, Z_L + h
~~~

The useful geometric picture is not a literal tetrahedron. The Higgs vacuum manifold is continuous.

For fixed Higgs magnitude:

~~~text
H^dagger H = v^2 / 2
~~~

the raw four-real-dimensional field space contains an S^3-type constant-radius surface before gauge identifications are accounted for.

The radial fluctuation:

~~~text
H = <H> + h + ...
~~~

moves away from the vacuum radius and corresponds to the physical Higgs excitation.

The Higgs mass is determined by local curvature of the scalar potential in the radial direction:

~~~text
m_h^2
=
d^2 V / d h^2
evaluated at the vacuum
~~~

while symmetry directions are flat before gauge fields reorganize them.

This supports the structural language:

~~~text
tangent / symmetry directions
    ->
Goldstone directions
    ->
longitudinal gauge modes

normal / radial direction
    ->
Higgs scalar mode
~~~

### What a Higgs quantum can and cannot do

Quantizing the radial Higgs-field excitation produces Higgs bosons.

Thus:

~~~text
Higgs-field oscillation
    ->
one Higgs quantum
~~~

A Higgs quantum can transfer its energy into excitations of other coupled fields and decay into allowed final states such as fermion pairs or massive gauge bosons when kinematics permit.

However:

~~~text
ordinary particles do not exist because the Higgs field continually vibrates them into existence
~~~

Instead:

~~~text
electron field excitation -> electron
quark-field excitation     -> quark
photon-field excitation    -> photon
Higgs-field excitation     -> Higgs boson
~~~

The Higgs vacuum expectation value modifies the dynamics of several of those fields through gauge and Yukawa couplings, giving masses after electroweak symmetry breaking.

The unification hypothesis should therefore use the stronger statement:

> Different observed particles may be distinct excitation modes of different effective field directions, while interactions allow energy to move between those modes.

A deeper unification would require deriving the Higgs direction, gauge directions, and fermionic directions from one more primitive state structure rather than merely placing them next to one another.

### Higgs as a possible effective order parameter

The current framework may test, but must not assume, the possibility:

~~~text
deeper degrees of freedom
    ->
coarse-graining / condensation
    ->
effective Higgs order parameter
~~~

If this branch is pursued, the theory must derive rather than fit:

~~~text
why the Higgs is a complex doublet
why its hypercharge is Y = 1/2
why its potential has the observed form
why electroweak symmetry breaks at the observed scale
why Yukawa couplings take their observed values
why the observed Higgs behaves so nearly like the Standard Model scalar
~~~

At present, the Standard Model description of the Higgs as an elementary scalar field remains the validated baseline.

### Next structural question

The next useful question is no longer merely:

~~~text
Can the Higgs create other particles?
~~~

but:

~~~text
Can Higgs, gauge, and fermion modes be obtained as different tangent,
normal, and spinorial excitations of one deeper state space?
~~~

If so, that deeper structure must reproduce the Standard Model representation content and interactions quantitatively.


---

## Higgs as an internal connection between left and right sectors

A stronger unification branch is to treat the Higgs not as a completely independent primitive scalar, but as an internal-direction component of a more general connection.

Write the fermionic state schematically as:

~~~text
Psi = (psi_L, psi_R)^T
~~~

and define a generalized Dirac / connection operator:

~~~text
D_gen =
[ i D_L      Y H       ]
[ Y^dag H^dag  i D_R   ]
~~~

The diagonal blocks propagate left- and right-handed sectors through spacetime and gauge connections.

The off-diagonal block connects:

~~~text
psi_L <-> psi_R
~~~

and has the transformation structure of the Higgs-Yukawa sector.

Expanding:

~~~text
bar(Psi) D_gen Psi
~~~

produces the ordinary kinetic / gauge pieces together with terms of the schematic form:

~~~text
bar(psi_L) Y H psi_R + h.c.
~~~

Thus the Yukawa interaction can be interpreted geometrically as motion / connection in an internal left-right direction.

This is a candidate structural explanation for why the Higgs couples left- and right-chiral fermions.

### Generalized connection and curvature

A minimal block connection can be written schematically as:

~~~text
A_gen =
[ A_L      H       ]
[ H^dag    A_R     ]
~~~

with generalized curvature:

~~~text
F_gen = d A_gen + A_gen^2
~~~

which contains schematic components:

~~~text
F_L
F_R
D H
H H^dag
H^dag H
~~~

Therefore one generalized curvature can, in principle, contain structures corresponding to:

~~~text
gauge kinetic terms
Higgs covariant kinetic terms
Higgs self-interaction terms
~~~

This is not yet a derivation of the Standard Model, but it is stronger than simply placing a gauge field and an unrelated scalar side by side.

### Relation to gauge-Higgs unification

A distinct but related route appears in higher-dimensional gauge theories:

~~~text
A_M = (A_mu, A_extra)
~~~

where the extra-dimensional component can appear as a scalar from a four-dimensional viewpoint.

In that language:

~~~text
gauge field in the full space
    ->
4D gauge component + 4D scalar component
~~~

so a Higgs-like scalar can be reinterpreted as another directional component of one higher-dimensional gauge connection.

The current framework does not choose between higher-dimensional and discrete/internal-direction realizations yet.

### What must be derived

The internal-connection picture only becomes physically significant if it explains, rather than assumes:

~~~text
H ~ (1, 2, +1/2)
why left and right fermions occupy their observed representations
why quarks and leptons carry their observed hypercharges
why one Higgs doublet is sufficient at low energy
why Yukawa matrices have their observed structure
why the Higgs potential and electroweak scale take their observed values
~~~

The next test is therefore representation-theoretic:

> Given the observed left/right fermion representation mismatch, how much of the Higgs representation is forced by the requirement that an internal connection map one sector into the other?

This test is useful because it distinguishes a genuine structural consequence from merely inserting a Higgs field by hand.


---

## Higgs representation from left-right representation mismatch

Using the Standard Model convention:

~~~text
Q = T3 + Y
~~~

the one-generation fermion representations are:

~~~text
L_L  ~ (1, 2, -1/2)
e_R  ~ (1, 1, -1)

Q_L  ~ (3, 2, +1/6)
u_R  ~ (3, 1, +2/3)
d_R  ~ (3, 1, -1/3)
~~~

If the Higgs-like internal connection maps a right-handed singlet into a left-handed SU(2)_L doublet, then its SU(2)_L transformation law must itself be doublet-like.

For the charged-lepton Yukawa structure:

~~~text
bar(L_L) H e_R
~~~

U(1)_Y invariance requires:

~~~text
-Y(L_L) + Y(H) + Y(e_R) = 0
~~~

hence:

~~~text
+1/2 + Y(H) - 1 = 0
Y(H) = +1/2
~~~

Color does not need to be changed by the connection, so:

~~~text
H ~ (1, 2, +1/2)
~~~

The same H then supports the down-type Yukawa coupling:

~~~text
bar(Q_L) H d_R
~~~

while the conjugate doublet:

~~~text
H_tilde = i sigma_2 H*
~~~

with hypercharge -1/2 supports the up-type coupling:

~~~text
bar(Q_L) H_tilde u_R
~~~

Thus, once the observed left/right fermion representations are given, the Higgs representation is strongly constrained by the requirement that one internal connection make the Yukawa maps gauge invariant.

This is not yet a derivation of the Higgs from first principles because the fermion representations were used as input.

The deeper problem is therefore shifted to:

~~~text
Why do the left/right fermion sectors carry exactly these gauge representations and hypercharges?
~~~

The next test combines:

~~~text
Yukawa-connectability
+
gauge-anomaly cancellation
~~~

to determine how much of the hypercharge pattern can be fixed without inserting the observed numbers independently.


---

## Pre-geometric phase, vacuum bubble transition, and emergence of internal directions

A stronger version of the current hypothesis does not assume that the presently observed internal state space existed from the beginning.

Instead, distinguish two phases:

~~~text
pre-transition phase
    ->
vacuum / phase transition
    ->
post-transition effective internal geometry
~~~

In the pre-transition phase, later notions such as:

~~~text
color direction
weak-isospin direction
Higgs radial direction
left/right internal connection
~~~

need not yet be separately meaningful observables.

The correct statement is therefore stronger than "they were present but hidden":

> The later internal coordinates may not have been physically defined before the phase transition.

This is analogous to a crystal: lattice directions become meaningful only after the ordered phase forms.

### Bubble language

If the transition is first order, a useful physical realization is vacuum bubble nucleation.

Schematically:

~~~text
metastable / high-symmetry phase
    ->
critical bubble of lower-energy phase
    ->
bubble expansion
    ->
new vacuum occupies the region
~~~

The phrase "bubble bursts" should therefore be interpreted as nucleation and growth of a new vacuum phase, not as a literal shell exploding into pre-existing particle directions.

### Tangent / normal decomposition after vacuum selection

Let a generic order parameter be Phi and the selected vacuum be Phi_0.

After the transition:

~~~text
Phi = Phi_0 + delta Phi
~~~

The fluctuation can be decomposed relative to the vacuum manifold:

~~~text
delta Phi
=
normal component
+
tangent components
~~~

The tangent directions correspond to motion along the degenerate vacuum manifold.

The normal direction corresponds to changing the magnitude / radial displacement away from the vacuum manifold.

For a simple scalar sector this gives the structural pattern:

~~~text
tangent directions
    -> symmetry / Goldstone directions

normal direction
    -> radial Higgs-like excitation
~~~

The local curvature of the potential in a normal direction sets a mass scale:

~~~text
m_normal^2
=
second derivative of V at the vacuum
~~~

and the associated correlation length is schematically:

~~~text
xi ~ 1 / m_normal
~~~

so the user's intuitive notion of "thickness" can be related to stiffness, correlation length, or bubble-wall thickness.

### If time and space are also emergent

If ordinary spacetime already exists before the transition, "before" and "after" can be interpreted in the usual temporal sense.

If spacetime itself is emergent, then the pre-transition structure may not admit an ordinary time coordinate.

In that stronger branch:

~~~text
pre-geometric ordering relation
    ->
transition / instability
    ->
effective spacetime + internal state geometry
~~~

and the word "before" means precedence in the deeper state dynamics rather than earlier coordinate time.

This branch remains speculative and must eventually recover Lorentzian spacetime, causal structure, and the observed low-energy field content.

---

## Correct group-theoretic realization of a 3+1 internal split

A four-component internal state by itself does not automatically produce the Standard Model color structure.

This distinction is essential.

### Fundamental-vector vacuum

If a fundamental scalar:

~~~text
Phi in C^4
~~~

transforms under SU(4) and develops a vacuum expectation value such as:

~~~text
<Phi> proportional to (0,0,0,v)
~~~

then the stabilizer is:

~~~text
SU(4) -> SU(3)
~~~

not generically:

~~~text
SU(3) x U(1)
~~~

For a gauged SU(4), seven generators are broken:

~~~text
15 - 8 = 7
~~~

so this model contains seven Goldstone directions before the Higgs mechanism reorganizes them.

Therefore a simple four-vector vacuum is not the correct mechanism for preserving a physical 3+1 split with an additional U(1).

### Adjoint / matrix order parameter

A more suitable order parameter is an SU(4)-adjoint matrix Sigma.

Choose a vacuum of the form:

~~~text
<Sigma>
proportional to
diag(1, 1, 1, -3)
~~~

which is traceless as required for su(4).

This vacuum preserves transformations acting among the first three components together with one commuting generator.

Thus:

~~~text
SU(4)
    ->
SU(3) x U(1)
~~~

up to the usual discrete quotient in the exact global group structure.

Now a fundamental four-component matter state decomposes under the unbroken subgroup as:

~~~text
4
    ->
3 + 1
~~~

with the first three components forming an SU(3) triplet and the fourth an SU(3) singlet.

This is the correct group-theoretic version of the intuitive:

~~~text
four undifferentiated internal components
    ->
three equivalent directions
+
one distinguished direction
~~~

### Physical interpretation of the current hypothesis

The stronger candidate history is therefore:

~~~text
pre-geometric / high-symmetry phase
    ->
vacuum transition
    ->
matrix-like order parameter acquires structured expectation value
    ->
internal symmetry breaks
    ->
3+1 representation split becomes meaningful
    ->
low-energy gauge, Higgs, and matter sectors emerge
~~~

The background order parameter itself may appear experimentally only as part of the vacuum structure, while its excitations and the fields defined relative to it appear as particles.

This formulation is preferable to saying that "three colors are three vacuum fluctuations."

The real requirement is:

> The post-transition vacuum must possess a stabilizer group and representation decomposition that reproduce the observed internal quantum numbers.

The next task is to determine whether one minimal order-parameter structure can simultaneously support:

~~~text
SU(3)_C
SU(2)_L
U(1)_Y
left/right chirality
a Higgs-like internal connection
~~~

without inserting these factors independently.


---

## Constrained state spaces, excitation gaps, and the "local cosmo" analogy

The current framework should distinguish between:

~~~text
microscopic degrees of freedom that exist
~~~

and:

~~~text
effective degrees of freedom that are actually accessible at a given energy and timescale
~~~

A degree of freedom can exist while remaining effectively invisible if it is strongly constrained or separated by a large excitation gap.

For a mode q_i with local quadratic dynamics:

~~~text
V(q_i) ~= (1/2) k_i q_i^2
~~~

the characteristic frequency is schematically:

~~~text
omega_i ~ sqrt(k_i / I_i)
~~~

and the excitation scale is:

~~~text
Delta_i ~ hbar omega_i
~~~

If an experiment satisfies:

~~~text
E << Delta_i
~~~

then that direction is effectively frozen.

If:

~~~text
E >= Delta_i
~~~

the mode becomes dynamically accessible.

This motivates a scale-dependent effective degree-of-freedom count:

~~~text
N_eff(E)
=
number of modes with Delta_i below the accessible energy scale
~~~

### Geometrically compact directions

A hidden direction can also be difficult to excite because it is geometrically compact.

For an internal direction of characteristic size r_i, a generic Kaluza-Klein-like excitation scale behaves as:

~~~text
E_i ~ hbar c / r_i
~~~

so:

~~~text
smaller r_i
    ->
higher excitation threshold
    ->
less visible low-energy freedom
~~~

This gives a precise version of the intuitive phrase "the direction is shrunk."

The present framework should therefore distinguish:

~~~text
geometrically small direction: r_i small
dynamically stiff direction:    Delta_i large
~~~

Both can make a degree of freedom effectively absent from low-energy observations.

### Phase transitions as release of effective freedom

A phase transition need not create degrees of freedom from nothing.

A more conservative candidate mechanism is:

~~~text
strongly constrained / gapped state space
    ->
control parameter changes
    ->
some gaps decrease
    ->
previously frozen modes become accessible
    ->
new effective coordinates and collective modes appear
~~~

If a common order parameter chi controls several sectors, write schematically:

~~~text
r_i = r_i(chi)
Delta_i = Delta_i(chi)
~~~

Then a transition in chi can reorganize which directions are dynamically available.

The release can occur simultaneously or in stages.

This is preferable to saying that a transition literally creates all later dimensions and internal degrees of freedom ex nihilo.

---

## Water evaporation as a controlled analogy

Liquid water provides a useful classical analogy for constrained versus accessible state space.

A water molecule already possesses translational, rotational, vibrational, and electronic degrees of freedom.

In the liquid, however, neighboring molecules and the hydrogen-bond network strongly constrain the set of configurations explored on a given timescale.

Evaporation changes the accessible state space:

~~~text
liquid local environment
    ->
molecular escape through the interface
    ->
gas-phase motion with much larger accessible translational phase space
~~~

The entropy relation:

~~~text
S = k_B ln Omega
~~~

expresses this in terms of accessible microstate count.

For vaporization:

~~~text
Omega_gas >> Omega_liquid
~~~

and therefore, under ordinary conditions:

~~~text
Delta S_vap > 0
~~~

The important lesson is not that water literally contains a separate universe.

The useful structural analogy is:

> A local interacting system can possess many microscopic degrees of freedom while only a restricted subset of its state space is effectively accessible; a phase transition can greatly enlarge that accessible region.

This is the intended physical meaning of the informal "local cosmo" language.

### A minimal working definition of "cosmo" for this project

To prevent the word from becoming purely metaphorical, define a local effective cosmo as a triple:

~~~text
C = (X, C_constraints, Delta)
~~~

where:

~~~text
X              = state space
C_constraints  = active constraints / couplings
Delta          = excitation-gap spectrum
~~~

Optionally include a metric or response kernel:

~~~text
G_ij
~~~

that determines distances, kinetic cost, or response in state space.

A phase transition is then represented as:

~~~text
C_before
    ->
C_after
~~~

with changes in:

~~~text
accessible region of X
constraint structure
gap spectrum
effective dimensionality
collective modes
symmetry
~~~

This definition is intentionally general enough to describe:

~~~text
molecular phase transitions
condensed-matter order
Higgs-like vacuum transitions
compact / hidden internal directions
candidate pre-geometric transitions
~~~

without claiming that these systems are physically identical.

### Current preferred interpretation

The strongest current formulation is:

> The pre-transition phase need not be "undefined." It may instead contain a larger underlying state space whose directions are strongly constrained, compact, gapped, or not yet separated into the effective coordinates used by the post-transition observer.

The corresponding emergence chain is:

~~~text
underlying state space
    ->
strong constraints / large gaps
    ->
phase transition
    ->
gap reduction / constraint reorganization
    ->
effective directions become accessible
    ->
collective modes become observable as particles / fields
~~~

This is currently a better-defined branch than saying that the later degrees of freedom did not exist at all.


---

## Reverse inference from present conserved quantities

The present branch can be made more concrete by reversing the usual direction of the cosmological problem.

Instead of asking:

~~~text
What initial microstate should be assumed?
~~~

ask:

~~~text
Given quantities and correlations that survive to the present,
what pre-transition state spaces remain compatible with them?
~~~

### Conservation law to use

In general relativity the robust local conservation statement is:

~~~text
nabla_mu T^(mu nu) = 0
~~~

For a homogeneous expanding universe this becomes the continuity equation:

~~~text
dot(rho) + 3 H (rho + p) = 0
~~~

This does not imply that a unique global "total energy of the whole universe" must exist in the same sense as in ordinary Newtonian mechanics.

The useful conserved / transported information is instead encoded in local stress-energy evolution, conserved charges, entropy flow, and relic correlations.

For standard components:

~~~text
nonrelativistic matter: rho_m proportional to a^-3
radiation:             rho_r proportional to a^-4
vacuum-like energy:    rho_vac approximately constant
~~~

These scaling laws allow present densities to constrain earlier states.

### Entropy as a probe of accessible state count

Energy alone cannot determine how many degrees of freedom carried it.

Entropy adds information about accessible state count:

~~~text
S = k_B ln Omega
~~~

For a relativistic thermal plasma:

~~~text
s proportional to g_*s T^3
~~~

and under approximately adiabatic expansion:

~~~text
s a^3 approximately constant
~~~

The effective thermal degree count g_*s therefore provides an established example of scale- and temperature-dependent accessible degrees of freedom.

This is directly analogous to the project quantity:

~~~text
N_eff(E, chi)
~~~

but the two should not be identified without a model.

The useful principle is:

> Present entropy and relic temperatures can constrain how many effective degrees of freedom were active at earlier epochs.

### Reverse-problem data vector

Define a schematic present-information vector:

~~~text
I_now =
{
stress-energy densities,
entropy density,
conserved charges,
particle abundances,
radiation temperatures,
correlation functions,
relic spectra,
topological / defect constraints
}
~~~

Then the theory should solve an inverse problem:

~~~text
C_before
    ->
transition dynamics
    ->
C_after
    ->
I_now
~~~

and retain only pre-transition models whose forward evolution reproduces the measured I_now.

This is stronger than fitting one present quantity at a time.

### Degree release versus geometric expansion

Two distinct effects must be separated.

First, accessible state space may expand:

~~~text
N_eff increases
Omega increases
effective dimensionality may increase
~~~

Second, physical spacetime may expand:

~~~text
a(t) increases
~~~

A phase transition can produce the first without producing the second.

To drive accelerated geometric expansion in ordinary GR, the effective stress-energy must satisfy:

~~~text
rho + 3 p < 0
~~~

For vacuum-like energy:

~~~text
p approximately -rho
~~~

so accelerated expansion is possible.

The working "Bang" hypothesis should therefore be written as two coupled transitions:

~~~text
release / reorganization of effective degrees of freedom
+
conversion or persistence of vacuum-like stress-energy that drives geometry
~~~

rather than as a simple explosion into empty space.

### A minimal instability model

Let chi control the constrained state-space phase.

Near a local configuration chi_0:

~~~text
V(chi) ~= V(chi_0)
          + (1/2) V''(chi_0) (delta chi)^2
~~~

If:

~~~text
V''(chi_0) > 0
~~~

small deviations oscillate.

If:

~~~text
V''(chi_0) = 0
~~~

a critical soft mode appears.

If:

~~~text
V''(chi_0) < 0
~~~

the configuration is unstable and the relevant mode grows rather than oscillates.

This provides a precise version of:

~~~text
stable constrained cosmo
    ->
softening
    ->
critical point
    ->
instability
    ->
rapid state-space reorganization
~~~

The characteristic expansion / growth rate and the geometric Hubble rate are not automatically the same quantity; a model must specify how chi couples to stress-energy and geometry.

### Stored energy and redistribution

The current framework should avoid saying that a Bang requires externally supplied fuel.

A more conservative possibility is redistribution:

~~~text
energy stored in vacuum / constraints / curvature / internal modes
    ->
expansion work
+ particle excitations
+ radiation
+ internal excitations
+ residual vacuum energy
~~~

The relevant question is then not:

~~~text
How much external energy was injected?
~~~

but:

~~~text
What pre-transition energy-density and constraint structure
could evolve into the observed post-transition contents?
~~~

### Falsifiable inverse target

A useful candidate model must predict several present observables from the same pre-transition parameters.

For example:

~~~text
theta_pre
    ->
rho_r today
rho_m today
entropy per comoving volume
relic abundance pattern
gravitational-wave / defect constraints
coupling relations
~~~

If different observables require unrelated retuning of theta_pre, the model has not achieved unification.

The strongest version of the present program is therefore:

> Reconstruct the smallest pre-transition constrained state space consistent with all surviving conservation, entropy, charge, and correlation information.

This turns the "ask today's conserved quantities" intuition into a concrete inverse problem rather than a metaphor.


---

## Conservation, conversion, information loss, and constraint reconstruction

The reverse-inference program must distinguish three different questions:

~~~text
1. What quantity is conserved?
2. Into what form can that quantity be converted?
3. What information is lost when the conversion is coarse-grained?
~~~

A conserved quantity may survive while its carrier changes.

Schematically:

~~~text
Q_total = Q_A + Q_B + Q_C + ...
~~~

and a transition may perform:

~~~text
Q_A -> Q_B + Q_C
~~~

while still satisfying:

~~~text
Delta Q_total = 0
~~~

Energy redistribution is one example:

~~~text
vacuum / constraint energy
    ->
radiation
+ matter excitations
+ kinetic energy
+ internal excitations
+ residual vacuum energy
~~~

Therefore conservation alone does not imply that the pre-transition state can be uniquely reconstructed.

### Invertible versus many-to-one evolution

If the effective transformation is:

~~~text
X_after = F(X_before)
~~~

and F is invertible, then:

~~~text
X_before = F^-1(X_after)
~~~

and the previous state can, in principle, be reconstructed.

If instead:

~~~text
F(X_1) = F(X_2)
~~~

for distinct earlier states X_1 and X_2, the present state does not uniquely determine the past.

This is the generic coarse-graining problem:

~~~text
many microscopic histories
    ->
same macroscopic observables
~~~

The inverse program must therefore use as many independent surviving invariants and correlations as possible.

### Three-layer reconstruction model

For the present project, organize the surviving information into three layers.

Layer A: conserved or continuity-constrained quantities

~~~text
Q = {
stress-energy flow,
exact or approximate conserved charges,
topological invariants where applicable
}
~~~

Layer B: transformed but traceable quantities

~~~text
T = {
energy partition among sectors,
particle abundances,
entropy distribution,
radiation temperatures,
spectral distortions,
relic populations
}
~~~

Layer C: reconstructed constraints

~~~text
K = {
coupling relations,
symmetry restrictions,
selection rules,
allowed transitions,
gap structure,
effective dimensionality
}
~~~

The working inverse problem is then:

~~~text
(Q_now, T_now, correlations_now)
    ->
candidate transformation history
    ->
K_before
    ->
candidate C_before
~~~

The goal is not to reconstruct one arbitrary microscopic state, but the smallest pre-transition constraint structure consistent with all surviving data.

---

## Freedom release is not sufficient: emergence also requires constraint formation

The previous discussion emphasized that a phase transition may release previously frozen or gapped degrees of freedom.

That is only half of a stable emergence process.

A long-lived structured phase generally requires new constraints to appear as old ones are relaxed.

The preferred schematic is therefore:

~~~text
old constraints
    ->
instability / transition
    ->
degree release
    +
new constraint formation
    ->
stable higher-level organization
~~~

This suggests a useful distinction:

~~~text
stable emergence
=
increase or reorganization of accessible freedom
+
formation of compatible higher-level constraints
~~~

versus:

~~~text
runaway local release
=
loss of higher-level constraints
+
self-amplifying local dynamics
~~~

### Biological analogy and its limit

Cancer provides a useful analogy for the second pattern.

In a multicellular organism, cellular proliferation and survival are constrained by:

~~~text
growth-control signaling
apoptosis
tissue architecture
resource allocation
immune surveillance
~~~

Cancer can involve partial escape from these higher-level constraints, followed by local self-amplifying growth.

Structurally:

~~~text
loss of organism-level constraints
    ->
increased local proliferative freedom
    ->
self-reinforcing expansion
~~~

This resembles the abstract pattern of constraint loss plus local freedom release.

However:

> Similar dynamical structure does not imply physical identity.

A tumor, a phase transition, a vacuum bubble, a civilization, and an expanding universe are not the same physical system merely because some coarse-grained equations may share growth, threshold, or constraint-release motifs.

The analogy is retained only as a test of the abstract framework.

### Stronger unification criterion

The theory should not classify two systems as manifestations of one mechanism merely because they both show:

~~~text
boundaries
growth
energy intake
instability
expansion
~~~

A stronger claim requires some combination of:

~~~text
same governing variables
same transformation law
same dimensionless control parameters
same critical scaling
same conserved quantities
same residual prediction
~~~

Without those, the relationship remains analogy rather than unification.

### Updated emergence principle

The current framework therefore upgrades:

~~~text
emergence = release of effective freedom
~~~

to:

~~~text
emergence
=
reorganization of conserved quantities
+
release / suppression of effective degrees of freedom
+
reconstruction of constraints
~~~

This three-part structure is now the preferred general template.

## Canonical current map

The current physically disciplined map is:

~~~text
deeper degrees of freedom
    |
    +-> admissible transformations
    +-> conservation laws
    +-> composition rules
    |
    v
state space
    |
    +-> symmetry / redundancy
    +-> constraints
    |
    v
connection
    |
    +-> internal connection ----> gauge curvature
    |
    +-> spacetime connection ---> geometric curvature
    |
    v
scale-dependent coarse-graining
    |
    +-> memory
    +-> noise
    +-> dissipation
    +-> transport
    +-> stable effective modes
    |
    v
effective theories
    |
    +-> hydrodynamics / thermodynamics
    +-> quantum effective dynamics
    +-> Standard Model candidate limit
    +-> GR candidate limit
~~~

The unresolved bridge is:

~~~text
primitive physical principles
    ->
specific state space
    ->
specific symmetry group
    ->
specific particle / field content
~~~

That is the next derivation target.

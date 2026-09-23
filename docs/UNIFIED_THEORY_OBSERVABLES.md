# Unified-Theory Research Target: What Must Be Explained

This document defines the next research target for the candidate unified-theory branch of HexDoku.

The goal is **not** to force every domain into one microscopic equation.

The stronger target is to explain why different effective laws appear at different scales, which information survives coarse-graining, which information is discarded, and how discarded degrees of freedom can return as measurable memory, noise, dissipation, transport, or backreaction.

---

## 1. Central claim to test

A candidate unified framework should explain the chain:

~~~text
deeper degrees of freedom
    ->
conservation + admissible transformations
    ->
coarse-graining
    ->
effective state variables
    ->
effective dynamics
~~~

The research question is:

> **Can apparently different macroscopic laws be derived as scale-dependent effective descriptions of one deeper dynamical structure?**

The framework must therefore explain not only states, but also the transition between descriptions.

---

## 2. What "coarse-graining" means here

A macroscopic description keeps only a small set of variables and discards most microscopic information.

For a fluid, the microscopic state may include:

~~~text
positions of molecules
momenta of molecules
rotational / vibrational states
pair and higher-order correlations
collision history
wall interactions
~~~

The macroscopic description may retain only:

~~~text
density rho
velocity field v
temperature T
pressure p
internal energy e
~~~

Thus:

~~~text
microstate Gamma
    ->
coarse-graining C
    ->
macrostate X = C(Gamma)
~~~

Many different microscopic states can map to the same macroscopic state.

The theory must therefore distinguish:

~~~text
same macrostate
!=
same microstate
~~~

without assuming that every microscopic difference matters macroscopically.

---

## 3. The closure problem

An effective theory is useful only when the retained variables approximately close the dynamics.

For ordinary hydrodynamics:

~~~text
mass conservation
+ momentum conservation
+ energy conservation
+ constitutive relations
+ equation of state
~~~

produce an effective closed description.

Schematically:

~~~text
dX/dt = F(X)
~~~

But if discarded degrees of freedom still matter, the effective equation may require:

~~~text
dX/dt
  =
F(X)
+ integral K(t-t') X(t') dt'
+ xi(t)
~~~

where:

~~~text
K   = memory kernel
xi  = unresolved-degree fluctuation term
~~~

The candidate unified theory should explain when the simple local equation is valid and when memory / noise / nonlocal corrections are required.

---

## 4. Concrete example: recorder acoustics

A recorder is a useful example because the macroscopic output is simple while the internal flow has many degrees of freedom.

Two students may play the same instrument and nominally produce the same note.

The air itself does not acquire a student-specific fundamental viscosity.

The differences arise from boundary conditions and flow history, including:

~~~text
breath pressure
jet velocity
mouth and tongue geometry
temperature and humidity
flow separation
vortex structure
boundary-layer state
condensation / wall condition
~~~

The internal fluid state is high-dimensional.

The audible result compresses that state into a small number of acoustic observables:

~~~text
pitch
attack time
harmonic spectrum
amplitude
noise content
decay
~~~

Thus:

~~~text
many fluid degrees of freedom
    ->
nonlinear coupling
    ->
small set of acoustic modes
~~~

The important lesson is not that hidden variables are mysterious.

The lesson is:

> **Degrees of freedom discarded by the simplest macroscopic description can still leave structured signatures in a lower-dimensional observable.**

This is the type of cross-scale effect the unified framework must characterize.

---

## 5. Concrete example: fluid state and constitutive memory

For a simple equilibrium fluid, an equation of state may be written:

~~~text
p = p(rho, T)
~~~

But this is not universal for every material and every regime.

A material with internal structure can require additional state variables:

~~~text
p = p(rho, T, xi_1, xi_2, ...)
~~~

where xi may encode, for example:

~~~text
orientation
polymer conformation
internal stress
phase fraction
structural relaxation
chemical composition
~~~

If these variables are not explicitly retained, their effects can appear as memory.

Therefore the candidate unified theory should explain:

~~~text
when p(rho,T) is sufficient
when extra internal variables are required
when eliminating those variables produces a memory kernel
~~~

---

## 6. Concrete example: thermal "loss"

The framework should not treat apparent dissipation as disappearance of a conserved quantity.

Instead:

~~~text
ordered motion
    ->
internal vibration
+ rotation
+ deformation
+ heat
+ radiation
+ unresolved modes
~~~

For a closed system:

~~~text
E_total = constant
~~~

while the useful or observed component can decrease:

~~~text
E_observed < E_initial
~~~

Thus an apparent conversion loss can arise because conserved energy is redistributed among many degrees of freedom.

The unified framework must distinguish:

~~~text
true violation of conservation
from
redistribution into unresolved channels
~~~

before introducing new physics.

---

## 7. Concrete example: preparation history

Suppose two systems are prepared through different paths:

~~~text
A: high state -> target state
B: low state  -> target state
~~~

At the comparison time, the usual macroscopic variables are matched:

~~~text
X_A = X_B
~~~

If future behavior still differs, there are several possibilities:

1. known internal variables were not actually matched;
2. the system is not equilibrated;
3. environmental correlations remain;
4. a non-Markovian memory term is required;
5. an additional degree of freedom is missing from the state description.

The theory should not jump directly to item 5.

The experimental hierarchy is:

~~~text
control known variables
    ->
measure relaxation
    ->
identify residual memory
    ->
test known environmental explanations
    ->
only then propose a new degree of freedom
~~~

---

## 8. Quantum-scale extension

The same logic can be applied to an open quantum system.

Let the observed system have reduced state rho.

Two preparations may satisfy:

~~~text
rho_A(t0) = rho_B(t0)
~~~

while differing in correlations with an environment.

If:

~~~text
rho_A(t0 + dt) != rho_B(t0 + dt)
~~~

then the reduced state alone is not dynamically closed.

That does **not** by itself prove a new fundamental field; known system-environment correlations can produce the effect.

The stronger target is a reproducible residual that remains after known environmental degrees of freedom and preparation correlations are accounted for.

---

## 9. Spacetime-scale extension

A much stronger unification test asks whether information normally discarded by a coarse-grained matter description influences gravitational or spacetime observables.

Construct two source states with the same resolved macroscopic stress-energy:

~~~text
<T_mn>_A = <T_mn>_B
~~~

but different higher-order correlations or internal structure.

Then compare gravitational observables:

~~~text
mean field
timing
phase
noise spectrum
correlation spectrum
~~~

The key candidate residual is:

~~~text
same resolved source
+
different unresolved correlations
    ->
different spacetime response
~~~

If such a difference survives all known electromagnetic, thermal, mechanical, and environmental explanations, it would show that the coarse-grained source description is incomplete.

This would be much stronger evidence than merely observing noise.

---

## 10. Cross-scale observable

The most valuable observable is not a single unexplained anomaly.

It is a **shared residual law across scales**.

For each domain define:

~~~text
R = observed response - effective-theory prediction
~~~

Examples:

~~~text
R_fluid
R_quantum
R_gravity
~~~

A strong unification candidate would require the same underlying parameter or kernel to predict more than one domain:

~~~text
H
  -> K_fluid -> R_fluid
  -> K_quant -> R_quantum
  -> K_grav  -> R_gravity
~~~

where H is one deeper degree-of-freedom structure.

If each domain needs unrelated fitted corrections, no meaningful unification has occurred.

---

## 11. Scale test

Let k represent inverse length scale.

Define a residual:

~~~text
R(k, omega)
=
Observed(k, omega)
-
EffectiveTheory(k, omega)
~~~

Ordinary microscopic corrections are expected to become negligible in the regime where the macroscopic effective theory is valid.

A particularly important test is therefore:

~~~text
limit k -> 0 of R(k, omega)
~~~

If:

~~~text
R -> 0
~~~

the correction is consistent with a finite-scale microscopic effect.

If a structured residual persists to much larger scales, then the missing degree of freedom or nonlocal structure must be incorporated into the larger-scale effective theory.

Persistence alone is not proof of fundamental physics; systematic errors and known long-range couplings must still be excluded.

---

## 12. What the unified theory must explain

A serious unified theory should eventually explain all of the following in one architecture.

### A. Why effective variables exist

Why can enormous microscopic state spaces be compressed into a few robust macroscopic variables?

### B. Why some information becomes irrelevant

What determines which microscopic differences wash out under coarse-graining?

### C. Why some discarded information returns

Why do some eliminated variables reappear as:

~~~text
noise
memory
dissipation
viscosity
transport
hysteresis
backreaction
~~~

### D. Why conservation laws survive scale change

Which conserved quantities remain exact, approximate, or emergent after coarse-graining?

### E. Why effective laws change with scale

Why do different regimes admit different descriptions such as:

~~~text
microscopic mechanics
kinetic theory
hydrodynamics
thermodynamics
effective field theory
geometry / gravity
~~~

### F. When an effective theory closes

What conditions allow:

~~~text
dX/dt = F(X)
~~~

and what conditions require:

~~~text
memory
nonlocality
additional variables
stochastic terms
~~~

### G. Whether one deeper structure generates several domains

Can one deeper structure predict residual behavior in fluid, quantum, and gravitational systems without unrelated ad hoc corrections?

---

## 13. Candidate principle: cross-scale closure

A useful provisional principle is:

> **At each scale, the correct effective state is the minimal set of variables that makes the dynamics predictively closed to the required accuracy.**

If closure fails:

~~~text
first add known internal variables
then add memory / environmental structure
then test nonlocality
only then introduce genuinely new degrees of freedom
~~~

This prevents the unified theory from becoming an unrestricted explanation machine.

---

## 14. Candidate principle: coarse-graining backreaction

A second provisional principle is:

> **Discarded degrees of freedom may be absent from the explicit state while still contributing effective noise, memory, transport, or backreaction to the retained variables.**

This is not automatically new physics.

The new-physics threshold is reached only when a residual:

~~~text
is reproducible
survives improved state reconstruction
survives known environmental corrections
has a stable scaling law
predicts new data
and preferably appears across more than one physical domain
~~~

---

## 15. Experimental program

The practical research sequence should be:

### Stage 1 — Classical benchmark

Use a controllable many-degree-of-freedom system such as a fluid / acoustic system.

Measure:

~~~text
input history
macroscopic state
response spectrum
relaxation time
memory dependence
scale dependence
~~~

Fit the smallest closed effective model.

### Stage 2 — Quantum benchmark

Repeat the logic with a controlled open quantum system.

Test whether the present reduced state is sufficient or whether preparation correlations are required.

### Stage 3 — Cross-scale comparison

Compare the mathematical form of the inferred memory / fluctuation kernels.

Do not assume they are the same.

### Stage 4 — Gravitational / spacetime test

Only after a robust residual law exists in controlled systems should an analogous gravitational observable be sought.

### Stage 5 — Unified prediction

A true unification step requires one deeper model to predict at least two distinct domains before fitting the new data.

---

## 16. Falsification criteria

This research direction should be rejected or narrowed if:

~~~text
all residuals vanish after known variables are included
memory effects are fully explained by known environmental coupling
different domains require unrelated kernels with no common structure
the proposed deeper model merely re-labels existing equations
no new quantitative prediction can be produced
~~~

The theory must not count successful post-hoc description as unification.

---

## 17. Current working interpretation

The strongest current statement is:

> **A possible route to unification is not a single universal force, but a common theory of degrees of freedom, conservation, coarse-graining, closure, memory, and scale-dependent effective laws.**

The immediate research target is therefore:

~~~text
identify where effective descriptions close
identify where they fail
measure the residual
derive its scale law
test whether one deeper structure predicts residuals across domains
~~~

Until that program succeeds, this remains a research framework and falsifiable hypothesis architecture, not an established unified theory.

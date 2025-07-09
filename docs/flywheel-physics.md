# Flywheel Physics

A spinning flywheel stores energy as rotational inertia.
This short explainer shows how to estimate that energy
and how GitHub renders formulas using LaTeX.

## Moment of inertia

For a solid cylinder,
$$I = \tfrac{1}{2} m r^2$$
where $m$ is mass and $r$ is radius.
Larger and heavier wheels have more inertia.

## Stored energy

The kinetic energy of a rotating wheel is
$$E = \tfrac{1}{2} I \omega^2$$
with angular velocity $\omega$ in radians per second.

GitHub automatically displays these formulas when
LaTeX expressions are wrapped in dollar signs.

## Forces on the adapter

When you spin the wheel, torque $T$ from the motor or handle acts on the adapter. If the adapter slips, the wheel will not accelerate. Approximate the shear stress on the clamp as
$$\tau \approx \frac{T}{r A}$$
where $r$ is the shaft radius and $A$ is the contact area.

Choose an adapter material with yield strength safely above $\tau$.
Nylon or metal inserts work for higher torques, while PETG suffices for lighter loads.

Tightening the bolts increases normal force $F_n$ on the shaft. Friction then resists the twisting force:
$$T_{max} = \mu F_n r$$
with friction coefficient $\mu$ around 0.2--0.3 for plastic on steel.
Use stronger bolts or more clamp area if you need higher torque capacity.

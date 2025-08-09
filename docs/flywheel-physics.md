# Flywheel Physics

A spinning flywheel stores energy as rotational inertia.
This short explainer shows how to estimate that energy
and how GitHub renders formulas using LaTeX.

## Moment of inertia

For a solid cylinder,
$$I = \tfrac{1}{2} m r^2$$
where $m$ is mass and $r$ is radius.
Most flywheels include a bore for the shaft.  Treating the wheel as a
thick-walled cylinder with inner radius $r_i$ and outer radius $r_o$ gives
$$I = \tfrac{1}{2} m (r_o^2 + r_i^2)$$
Setting $r_i \to 0$ recovers the solid-disk formula, while the thin-rim limit
($r_i \approx r_o$) approaches $$I = m r_o^2,$$ doubling inertia for the same mass.

```mermaid
graph LR
    A[Solid disk] -->|I = \tfrac{1}{2} m r^2| B[Inertia]
    C[Thin rim] -->|I = m r^2| B
```

Integrating the mass distribution shows where this expression comes from:

$$I = \int_0^r r'^2\, \mathrm{d}m = \int_0^r r'^2 (2\pi \rho h r'\, \mathrm{d}r') = \tfrac{1}{2}\pi \rho h r^4 = \tfrac{1}{2} m r^2$$

where $\rho$ is the material density and $h$ the cylinder height.

## Stored energy

The kinetic energy of a rotating wheel is
$$E = \tfrac{1}{2} I \omega^2$$
with angular velocity $\omega$ in radians per second.

### Example using CAD dimensions

The stock CAD model in [`cad/flywheel.scad`](../cad/flywheel.scad) defines a
thick disk with outer radius $r_o=50\,\text{mm}$, inner radius $r_i=5\,\text{mm}$ for
the shaft, and height $h=20\,\text{mm}$.  For material density $\rho$, the mass is

$$m = \rho\pi (r_o^2 - r_i^2) h$$

Converting the CAD dimensions to SI units gives $r = 0.05\,\text{m}$ and
$h = 0.02\,\text{m}$.  PLA has density
$\rho \approx 1.25\,\text{g/cm}^3 = 1.25\times10^3\,\text{kg/m}^3$.
The volume is $V = \pi r^2 h \approx 1.6\times10^{-4}\,\text{m}^3$, so the mass is
$m = \rho V \approx 0.20\,\text{kg}$.

$$I = \tfrac{1}{2} m r^2 \approx 2.5\times10^{-4}\,\text{kg·m}^2.$$ At
3000\,rpm the angular speed is $\omega = \tfrac{2\pi n}{60} \approx 314\,\text{rad/s}$,
so the wheel stores roughly $$E \approx 12\,\text{J}.$$

If the wheel were a thin rim of the same mass, the inertia would double:
$$I_{rim} = m r^2.$$

GitHub automatically displays these formulas when LaTeX expressions are wrapped
in dollar signs.

## Rim speed and material limits

The rim's tangential velocity is
$$v = \omega r$$
where $r$ is the wheel radius.  Using the CAD value $r=50\,\text{mm}$ and
3000\,rpm ($\omega \approx 314\,\text{rad/s}$) gives $v \approx 16\,\text{m/s}$.  Plastic
parts have a maximum safe speed set by hoop stress.  Approximating the wheel as
a thin rim,
$$\sigma \approx \rho r^2 \omega^2$$
with material density $\rho$ and yield strength $\sigma_y$.  Solving for the
upper speed limit,
$$\omega_{max} \approx \sqrt{\frac{\sigma_y}{\rho r^2}}$$
For PLA ($\rho \approx 1.25\,\text{g/cm}^3$, $\sigma_y \approx 60\,\text{MPa}$) and the
same radius, $\omega_{max} \approx 4.4\times10^3\,\text{rad/s}$ or about
42\,000\,rpm.  Designers typically apply a safety factor of at least two and
operate well below this bound.

```mermaid
graph TD
    R[Radius r = 50 mm] --> V[v = \omega r]
    R --> S[\sigma \approx \rho r^2 \omega^2]
    S --> W[\omega_{max} = \sqrt{\sigma_y/(\rho r^2)}]
```

## Spin-up time

A constant torque $T$ causes angular acceleration $\alpha$ according to

$$\alpha = \frac{T}{I}$$

Starting from rest, the time to reach speed $\omega$ is therefore

$$t = \frac{\omega}{\alpha} = \frac{I\omega}{T}$$

Using the same CAD dimensions as above ($I \approx 2.5\times10^{-4}\,\text{kg·m}^2$),
a modest $0.5\,\text{N·m}$ motor torque spins the wheel to
3000\,rpm ($\omega \approx 314\,\text{rad/s}$) in about $t \approx 0.16\,\text{s}$.

## Angular momentum and gyroscopic effects

The flywheel's angular momentum is

$$L = I\omega$$

which resists changes in orientation. Using the CAD values above
($I \approx 2.5\times10^{-4}\,\text{kg·m}^2$, $\omega \approx 314\,\text{rad/s}$)
gives $L \approx 7.8\times10^{-2}\,\text{kg·m}^2/\text{s}$.

Applying a torque $\tau$ perpendicular to the spin axis causes the wheel to
undergo precession at rate

$$\Omega = \frac{\tau}{L}.$$

```mermaid
graph TD
    L[Angular momentum L] --> O[Precession \Omega = \tau/L]
```

Even small hobbyist wheels can exhibit noticeable gyroscopic behavior when spun
at high speed.

## Spin-down from friction

Even unloaded, bearing and air drag slowly bleed energy from the wheel. Approximating a
constant friction torque $T_f$ gives the angular deceleration

$$\alpha = -\frac{T_f}{I}$$

so the coasting time from speed $\omega_0$ to rest is

$$t = \frac{I\omega_0}{T_f}$$

The stand in [`cad/stand.scad`](../cad/stand.scad) holds standard 608 bearings (22\,mm outer
diameter, 7\,mm thick) around the 8\,mm shaft from
[`cad/shaft.scad`](../cad/shaft.scad).  A typical 608 bearing produces
$T_f \approx 10^{-3}\,\text{N·m}$, so the example wheel ($I \approx
2.5\times10^{-4}\,\text{kg·m}^2$) coasts from 3000\,rpm ($\omega_0 \approx
314\,\text{rad/s}$) for roughly $t \approx 80\,\text{s}$.

## Angular momentum and precession

The spinning wheel also carries angular momentum
$$L = I \omega$$
which resists changes in orientation.  With the CAD inertia above and
$\omega \approx 314\,\text{rad/s}$, the wheel has
$L \approx 0.078\,\text{kg·m}^2/\text{s}$.  A torque $\tau$ applied
perpendicular to $L$ induces precession at
$$\Omega = \frac{\tau}{L}$$
on the stand in [`cad/stand.scad`](../cad/stand.scad).

```mermaid
graph TD
    T[Torque \tau] --> P[Precession \Omega = \tau / L]
```

## Forces on the adapter

When you spin the wheel, torque $T$ from the motor or handle acts on the
adapter. If the adapter slips, the wheel will not accelerate. Approximate the
shear stress on the clamp as
$$\tau \approx \frac{T}{r A}$$
where $r$ is the shaft radius and $A$ is the contact area.

Choose an adapter material with yield strength safely above $\tau$.
Nylon or metal inserts work for higher torques, while PETG suffices for lighter loads.

Tightening the bolts increases normal force $F_n$ on the shaft.
Friction then resists the twisting force:
$$T_{max} = \mu F_n r$$
with friction coefficient $\mu$ around 0.2--0.3 for plastic on steel.
Use stronger bolts or more clamp area if you need higher torque capacity.

For the adapter in [`cad/adapter.scad`](../cad/adapter.scad) the shaft diameter
is $8\,\text{mm}$ and the clamping length is $20\,\text{mm}$.  The contact area
is therefore $A \approx \pi d h \approx 5\times10^{-4}\,\text{m}^2$.  Under a
$5\,\text{N·m}$ torque the shear stress is about
$$\tau \approx \frac{5}{0.004\times 5\times10^{-4}} \approx 2.5\,\text{MPa},$$
well below the $40\,\text{MPa}$ yield strength of many nylon inserts.

## Multi-flywheel systems

Multiple wheels can be coupled together when a single flywheel does not
provide enough energy storage.  Belts, chains, or gears transfer torque
from one shaft to the next.  Assuming negligible losses, the ratio of
angular velocities in a belt drive is given by

$$\omega_2 = \frac{r_1}{r_2} \omega_1$$

where $r_1$ and $r_2$ are the radii of the driving and driven pulleys.
Gears follow the same relation using tooth counts instead of radii.

The total stored energy is simply the sum of each wheel's kinetic
energy:

$$E_{total} = \tfrac{1}{2} I_1 \omega_1^2 + \tfrac{1}{2} I_2 \omega_2^2 + \cdots$$

Connecting flywheels lets you trade off space, weight, and speed.  A
small high-speed wheel might feed power into a larger, slower wheel to
smooth out fluctuations.  Keep belt tension high enough to avoid slip
and align pulleys carefully so side loads do not wear the bearings.

Belt drives obey the tension ratio
$$\frac{T_1}{T_2} = e^{\mu \theta}$$
where $T_1$ is the tight-side tension, $T_2$ the slack side tension,
$\mu$ the coefficient of friction, and $\theta$ the wrap angle in radians.
This sets the maximum torque each belt can transmit.

```mermaid
graph LR
    A[Flywheel r\_1] -- belt --> B[Pulley r\_2]
    B -- belt --> C[Flywheel r\_3]
```

As an example, a 200\,mm wheel driving a 50\,mm pulley quadruples the speed.
Linking that smaller pulley to a third wheel can multiply storage while
keeping the overall setup compact.
Gears or chains work similarly but eliminate belt slip at the cost of more
noise and alignment care.

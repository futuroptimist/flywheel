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

### Example using CAD dimensions

The stock CAD model in [`cad/flywheel.scad`](../cad/flywheel.scad) defines a
solid cylinder with radius $r=50\,\text{mm}$ and height $h=20\,\text{mm}$.
For material density $\rho$, the mass is

$$m = \rho\,\pi r^2 h$$

Printing in PLA ($\rho \approx 1.25\,\text{g/cm}^3$) yields $m \approx 0.20\,\text{kg}$ and
$$I = \tfrac{1}{2} m r^2 \approx 2.5\times10^{-4}\,\text{kg·m}^2.$$ At
3000\,rpm the angular speed is $\omega = \tfrac{2\pi n}{60} \approx 314\,\text{rad/s}$,
so the wheel stores roughly $$E \approx 12\,\text{J}.$$

GitHub automatically displays these formulas when LaTeX expressions are wrapped
in dollar signs.

## Angular momentum

Angular momentum measures how strongly a spinning wheel resists changes in
orientation:
$$L = I \omega$$
Using the inertia from [`cad/flywheel.scad`](../cad/flywheel.scad)
($I \approx 2.5\times10^{-4}\,\text{kg·m}^2$) and the 3000\,rpm example
($\omega \approx 314\,\text{rad/s}$) gives
$$L \approx 0.08\,\text{kg·m}^2/\text{s}.$$
Heavier or faster wheels therefore exhibit stronger gyroscopic stability.

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

## Rim acceleration

The rim experiences centripetal acceleration as it spins:
$$a = r \omega^2$$
With the CAD radius $r = 50\,\text{mm}$ and $\omega \approx 314\,\text{rad/s}$,
$$a \approx 5\times10^3\,\text{m/s}^2$$
which is roughly 500\,$g$.  Spokes and hubs must withstand this load to keep
the wheel intact.

## Spin-up time

A constant torque $T$ causes angular acceleration $\alpha$ according to

$$\alpha = \frac{T}{I}$$

Starting from rest, the time to reach speed $\omega$ is therefore

$$t = \frac{\omega}{\alpha} = \frac{I\omega}{T}$$

Using the same CAD dimensions as above ($I \approx 2.5\times10^{-4}\,\text{kg·m}^2$),
a modest $0.5\,\text{N·m}$ motor torque spins the wheel to
3000\,rpm ($\omega \approx 314\,\text{rad/s}$) in about $t \approx 0.16\,\text{s}$.

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

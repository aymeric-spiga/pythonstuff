#! /usr/bin/env python

import sys

T = float(sys.argv[1])
P = float(sys.argv[2])

### For dust
radius = 2.e-6 ## m
rho = 2500. ## kg / m3

### For Mars
R = 192.  ## m2/s2/K
rhoair = P / R / T
grav = 3.72 ## m / s2
visc = 1.e-5 ## Gas molecular viscosity (N s / m2)
molrad = 2.2e-10 ## Effective gas molecular radius (m)

## Constant to compute stokes speed simple formulae
## Vstokes = b * rho * r**2 avec b = (2/9) * rho * g / visc
b = (2./9.) * grav / visc

## Constant to compute gas mean free path
## l= (T/P)*a, avec a = (  0.707*8.31/(4*pi*molrad**2 * avogadro))
a = 0.707 * 8.31 / ( 4 * 3.1416 * molrad * molrad * 6.023e23 )

## Sedimentation velocity (m/s)
## (stokes law corrected for low pressure by the Cunningham
## slip-flow correction  according to Rossow (Icarus 36, 1-50, 1978)
vstokes = b * rho * radius * radius * (1 + 1.333* ( a / 192. / rhoair ) / radius)

print "--- for T = %.0f K and P = %.0f Pa" % (T,P)
print "rho = %4.2e kg/m3 and vsedim = %4.2e m/s" % (rhoair,vstokes)

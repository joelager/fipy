#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "rotation.py"
 #
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 # ###################################################################
 ##

r"""

This example demonstraties the Roe solver for a single equation. The
exaample is from the Clawpack code and the reslults are comapred with
data generated by Clawpack. The example solver solid body rotation for
a circle and square region using the advection equation given by, 

.. math::
   
   \frac{\partial \phi}{\partial t} + \nabla \left( \vec{u} \phi \right) = 0

with

.. math::

   \vec{u} = \left(2 y, -2 x \right)

The intial conditions are shown in Figure.


>>> from fipy import *

>>> N = 80
>>> L = 2.
>>> dx = L / N 
>>> origin =[[-1], [-1]]

>>> mesh = Grid2D(nx=N, ny=N, dx=dx, dy=dx) + origin
>>> x, y = mesh.cellCenters

>>> var = CellVariable(mesh=mesh, hasOld=True)

>>> def initialize(v):
...     v[:] = 0.
...     v[(0.1 < x) & (x < 0.6) & (-0.25 < y) & (y < 0.25)] = 1.
...     r = numerix.sqrt((x + 0.45)**2 + y**2)
...     v.setValue(1 - r / 0.35, where=r < 0.35)
>>> initialize(var)

>>> vel = FaceVariable(mesh=mesh, rank=1)
>>> def psi(x, y):
...     return x**2 + y**2

>>> X, Y = mesh.faceCenters
>>> ## This is how CLAWPACK calculates the velocity. Go figure.
>>> vel[0] = (psi(X, Y + mesh.dy / 2) - psi(X, Y - mesh.dy / 2)) / mesh.dy
>>> vel[1] = -(psi(X + mesh.dx / 2, Y) - psi(X - mesh.dx / 2., Y)) / mesh.dx


>>> eqn = TransientTerm() + FirstOrderRoeConvectionTerm(vel)

>>> viewer = Viewer(var)
>>> elapsed = 0.0
>>> dt = 0.0009
>>> ##def run():
>>> numerix.savetxt('data0.txt', var.value)


>>> for i in range(50):
...     var.updateOld()
...     eqn.solve(var, dt=dt)
...     elapsed += dt
...     if i % 10 == 0 and __name__ == '__main__':
...          viewer.plot()

>>> import os 
>>> filepath = os.path.splitext(__file__)[0] + 'FirstOrder.gz'
>>> print var.allclose(numerix.loadtxt(filepath, skiprows=9))
True

>>> initialize(var)
>>> eqn = TransientTerm() + SecondOrderRoeConvectionTerm(vel)

>>> for i in range(50):
...     var.updateOld()
...     eqn.solve(var, dt=dt)
...     elapsed += dt
...     if i % 10 == 0 and __name__ == '__main__':
...          viewer.plot()

>>> import os 
>>> filepath = os.path.splitext(__file__)[0] + 'SecondOrder.gz'
>>> print var.allclose(numerix.loadtxt(filepath, skiprows=9))
True

"""

__docformat__ = 'restructuredtext'

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())

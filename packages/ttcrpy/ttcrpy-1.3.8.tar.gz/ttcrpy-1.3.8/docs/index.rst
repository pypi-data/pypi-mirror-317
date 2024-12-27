.. ttcrpy documentation master file, created by
   sphinx-quickstart on Mon Mar 23 21:27:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##################################
Welcome to ttcrpy's documentation!
##################################

`ttcrpy` is a package for computing traveltimes and raytracing that was
developed with geophysical applications in mind, e.g. ray-based seismic/GPR
tomography and microseismic event location (joint hypocenter-velocity inversion).
The package contains code to perform computation on 2D and 3D rectilinear grids,
as well as 2D triangular and 3D tetrahedral meshes. Three different algorithms
have been implemented: the Fast-Sweeping Method, the Shortest-Path Method, and
the Dynamic Shortest-Path Method. Calculations can be run in parallel on a
multi-core machine.  The core computing code is written in C++, and has been
wrapped with cython.

The source code of this project is hosted on `GitHub <https://github.com/groupeLIAMG/ttcr>`_.

If you use `ttcrpy`, please cite

Giroux B. 2021. ttcrpy: A Python package for traveltime computation and raytracing.
SoftwareX, vol. 16, 100834. doi: 10.1016/j.softx.2021.100834
https://www.sciencedirect.com/science/article/pii/S2352711021001217


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started.rst
   model_discretization.rst
   algorithms.rst
   performance.rst
   code.rst
   references.rst

##################
Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

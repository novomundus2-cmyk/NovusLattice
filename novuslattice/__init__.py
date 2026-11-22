"""
NovusLattice: Sutton-Chen Empirical Potential in Sobolev H¹(Ω) Spaces
Industrial Multiscale Continuum Mechanics Framework

Author: Mikel Irastorza
Organization: Novo Mundus (Spain)
License: PolyForm Noncommercial 1.0.0 / CC BY-NC-ND 4.0
"""

__version__ = "1.0.0"
__author__ = "Mikel Irastorza"
__organization__ = "Novo Mundus"
__country__ = "Spain"

from .potential import SuttonChenPotential, FCC_METALS, SuttonChenParams
from .springback import SpringbackSolver, BendingConfig, SpringbackResult
from .industrial_cases import (
    CuttingCase,
    BendingCase,
    RoboticGrippingCase,
    ThermalDriftCase,
    run_all_industrial_cases,
)

__all__ = [
    "SuttonChenPotential",
    "FCC_METALS",
    "SuttonChenParams",
    "SpringbackSolver",
    "BendingConfig",
    "SpringbackResult",
    "CuttingCase",
    "BendingCase",
    "RoboticGrippingCase",
    "ThermalDriftCase",
    "run_all_industrial_cases",
]

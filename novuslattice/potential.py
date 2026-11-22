"""
Sutton-Chen Empirical Potential Module
Calculates interatomic potentials, cohesive energies, and forces for FCC metals.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
import math

@dataclass(frozen=True)
class SuttonChenParams:
    name: str
    symbol: str
    epsilon_eV: float
    c: float
    a_angstrom: float
    n: int
    m: int
    thermal_alpha: float  # K^-1 linear expansion coefficient
    young_modulus_GPa: float
    yield_strength_MPa: float
    poisson_ratio: float

# Standard empirical parameters for FCC metals (Sutton & Chen 1990)
FCC_METALS: Dict[str, SuttonChenParams] = {
    "Au": SuttonChenParams(
        name="Gold",
        symbol="Au",
        epsilon_eV=1.2793e-2,
        c=34.408,
        a_angstrom=4.078,
        n=10,
        m=8,
        thermal_alpha=14.2e-6,
        young_modulus_GPa=78.0,
        yield_strength_MPa=205.0,
        poisson_ratio=0.44,
    ),
    "Ag": SuttonChenParams(
        name="Silver",
        symbol="Ag",
        epsilon_eV=2.541e-3,
        c=144.41,
        a_angstrom=4.086,
        n=12,
        m=6,
        thermal_alpha=18.9e-6,
        young_modulus_GPa=83.0,
        yield_strength_MPa=170.0,
        poisson_ratio=0.37,
    ),
    "Cu": SuttonChenParams(
        name="Copper",
        symbol="Cu",
        epsilon_eV=1.2382e-2,
        c=39.432,
        a_angstrom=3.615,
        n=9,
        m=6,
        thermal_alpha=16.5e-6,
        young_modulus_GPa=117.0,
        yield_strength_MPa=260.0,
        poisson_ratio=0.34,
    ),
    "Ni": SuttonChenParams(
        name="Nickel",
        symbol="Ni",
        epsilon_eV=1.5707e-2,
        c=39.755,
        a_angstrom=3.520,
        n=9,
        m=6,
        thermal_alpha=13.4e-6,
        young_modulus_GPa=200.0,
        yield_strength_MPa=350.0,
        poisson_ratio=0.31,
    ),
    "Al": SuttonChenParams(
        name="Aluminum",
        symbol="Al",
        epsilon_eV=5.033e-3,
        c=16.399,
        a_angstrom=4.050,
        n=7,
        m=6,
        thermal_alpha=23.1e-6,
        young_modulus_GPa=69.0,
        yield_strength_MPa=240.0,
        poisson_ratio=0.33,
    ),
}

class SuttonChenPotential:
    """Evaluates Sutton-Chen energy and forces with thermal lattice expansion."""

    def __init__(self, metal_symbol: str = "Au", reference_temp_K: float = 293.15):
        if metal_symbol not in FCC_METALS:
            raise ValueError(f"Unknown metal symbol '{metal_symbol}'. Available: {list(FCC_METALS.keys())}")
        self.params = FCC_METALS[metal_symbol]
        self.ref_temp_K = reference_temp_K

    def lattice_parameter(self, temp_K: float = 293.15) -> float:
        """Returns temperature-dependent FCC lattice constant a(T) in Angstroms."""
        delta_T = temp_K - self.ref_temp_K
        return self.params.a_angstrom * (1.0 + self.params.thermal_alpha * delta_T)

    def atomic_energy(self, distances_angstrom: List[float], temp_K: float = 293.15) -> float:
        """
        Calculates Sutton-Chen energy U_i for atom i given neighbor distances:
        U_i = epsilon * [ 0.5 * sum_j (a / r_ij)^n - c * sqrt( sum_j (a / r_ij)^m ) ]
        """
        if not distances_angstrom:
            return 0.0

        a = self.lattice_parameter(temp_K)
        eps = self.params.epsilon_eV
        c = self.params.c
        n = self.params.n
        m = self.params.m

        repulsive_sum = 0.0
        density_sum = 0.0

        for r in distances_angstrom:
            if r <= 1e-4:
                continue
            ratio = a / r
            repulsive_sum += math.pow(ratio, n)
            density_sum += math.pow(ratio, m)

        embedding = c * math.sqrt(density_sum) if density_sum > 0 else 0.0
        return eps * (0.5 * repulsive_sum - embedding)

    def pair_radial_force(self, r_angstrom: float, temp_K: float = 293.15, rho_avg: float = 12.0) -> float:
        """
        Approximate radial force magnitude dU/dr between two atoms:
        F(r) = - dU/dr (eV / Angstrom). Positive means attractive, negative repulsive.
        """
        if r_angstrom <= 1e-4:
            return 0.0
        a = self.lattice_parameter(temp_K)
        eps = self.params.epsilon_eV
        c = self.params.c
        n = self.params.n
        m = self.params.m

        ratio = a / r_angstrom
        d_repulsive = - (n / a) * math.pow(ratio, n + 1)
        # embedding gradient approximation
        d_embedding = - (m / (2.0 * a * math.sqrt(max(1.0, rho_avg)))) * math.pow(ratio, m + 1)

        d_U_dr = eps * (0.5 * d_repulsive - c * d_embedding)
        return - d_U_dr

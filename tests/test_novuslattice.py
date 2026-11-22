"""
Unit Tests for NovusLattice Framework
"""

import unittest
from novuslattice.potential import SuttonChenPotential, FCC_METALS
from novuslattice.springback import SpringbackSolver, BendingConfig
from novuslattice.industrial_cases import (
    CuttingCase,
    BendingCase,
    RoboticGrippingCase,
    ThermalDriftCase,
    run_all_industrial_cases,
)

class TestNovusLattice(unittest.TestCase):

    def test_potential_lattice_constant(self):
        pot_au = SuttonChenPotential("Au")
        self.assertAlmostEqual(pot_au.lattice_parameter(293.15), 4.078, places=3)
        # Thermal expansion test (warmer should expand lattice)
        self.assertGreater(pot_au.lattice_parameter(350.0), pot_au.lattice_parameter(293.15))

    def test_cohesive_energy_sign(self):
        pot_cu = SuttonChenPotential("Cu")
        a = pot_cu.lattice_parameter()
        r_nn = a / 1.41421356
        # 12 nearest neighbors in FCC
        energy = pot_cu.atomic_energy([r_nn] * 12)
        # Cohesive energy must be negative (bound state)
        self.assertLess(energy, 0.0)

    def test_springback_solver_overbend(self):
        cfg = BendingConfig(material_symbol="Al", thickness_mm=1.5, target_angle_deg=90.0)
        solver = SpringbackSolver(cfg)
        res = solver.solve(tolerance_mm=0.20)
        self.assertGreater(res.springback_angle_deg, 0.0)
        self.assertGreater(res.overbend_angle_deg, 90.0)
        # Uncompensated error exceeds 0.2 mm
        self.assertFalse(res.within_tolerance_without_comp)
        # Compensated error complies with tolerance
        self.assertLessEqual(res.compensated_flange_error_mm, 0.20)

    def test_industrial_cases_execution(self):
        cases = run_all_industrial_cases()
        self.assertEqual(len(cases), 4)
        for c in cases:
            self.assertIn("use_case", c)

if __name__ == "__main__":
    unittest.main()

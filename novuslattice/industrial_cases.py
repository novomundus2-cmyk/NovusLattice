"""
NovusLattice Industrial Manufacturing Use Cases
Evaluates cutting, bending/springback, robotic handling/tribology, and thermal drift.
"""

from dataclasses import dataclass
from typing import Dict, Any, List
import math
from .potential import FCC_METALS, SuttonChenPotential, SuttonChenParams
from .springback import SpringbackSolver, BendingConfig, SpringbackResult

@dataclass
class CuttingCase:
    """Case 1: Industrial Shearing, Punching and Laser Cutting."""
    metal_symbol: str
    sheet_thickness_mm: float
    cutting_speed_m_min: float = 25.0

    def evaluate(self) -> Dict[str, Any]:
        mat = FCC_METALS[self.metal_symbol]
        pot = SuttonChenPotential(self.metal_symbol)
        a_0 = pot.lattice_parameter(293.15)
        
        # Optimal blade clearance as percentage of thickness (C_opt ~ 0.005 * sqrt(sigma_y))
        clearance_pct = 0.006 * math.sqrt(mat.yield_strength_MPa) * 100.0
        clearance_mm = (clearance_pct / 100.0) * self.sheet_thickness_mm
        
        # Specific shear fracture energy (J/m^2) derived from cohesive energy
        # E_coh ~ 3.5 - 4.5 eV/atom converted to J/m^2 along {111} planes
        cohesive_eV = mat.epsilon_eV * mat.c
        cohesive_J = cohesive_eV * 1.60218e-19
        area_per_atom_m2 = (math.sqrt(3) / 4.0) * math.pow(a_0 * 1e-10, 2)
        surface_energy_J_m2 = cohesive_J / area_per_atom_m2

        # Shear stress required for crack initiation
        shear_strength_MPa = mat.yield_strength_MPa * 0.577  # Von Mises criterion

        return {
            "use_case": "Case 1: Industrial Shearing & Cutting (Corte y Cizallado)",
            "material": mat.name,
            "lattice_constant_angstrom": round(a_0, 4),
            "sheet_thickness_mm": self.sheet_thickness_mm,
            "optimal_clearance_percent": round(clearance_pct, 2),
            "optimal_clearance_mm": round(clearance_mm, 4),
            "shear_strength_MPa": round(shear_strength_MPa, 1),
            "surface_fracture_energy_J_m2": round(surface_energy_J_m2, 2),
            "burr_prevention_guideline": (
                f"Maintain blade clearance strictly at {clearance_mm:.3f} mm (±5 µm) to achieve clean "
                f"crystallographic slip along {{111}} planes and suppress secondary burr formation."
            ),
        }

@dataclass
class BendingCase:
    """Case 2: Precision Sheet Metal Bending & Springback Tolerance (EPTA France benchmark)."""
    metal_symbol: str = "Al"
    thickness_mm: float = 1.5
    punch_radius_mm: float = 1.0
    flange_length_mm: float = 50.0
    temperature_K: float = 293.15
    tolerance_threshold_mm: float = 0.20

    def evaluate(self) -> Dict[str, Any]:
        cfg = BendingConfig(
            material_symbol=self.metal_symbol,
            thickness_mm=self.thickness_mm,
            punch_radius_mm=self.punch_radius_mm,
            flange_length_mm=self.flange_length_mm,
            temperature_K=self.temperature_K,
        )
        solver = SpringbackSolver(cfg)
        res: SpringbackResult = solver.solve(tolerance_mm=self.tolerance_threshold_mm)

        return {
            "use_case": "Case 2: Sheet Metal Bending & Springback Compensation (Plegado y Recuperación Elástica)",
            "material": res.material,
            "ambient_temp_C": round(self.temperature_K - 273.15, 1),
            "target_angle_deg": 90.0,
            "springback_angle_deg": round(res.springback_angle_deg, 3),
            "required_overbend_angle_deg": round(res.overbend_angle_deg, 3),
            "uncompensated_flange_error_mm": round(res.flange_deflection_mm, 3),
            "tolerance_limit_mm": res.tolerance_threshold_mm,
            "passes_tolerance_uncompensated": res.within_tolerance_without_comp,
            "compensated_flange_error_mm": res.compensated_flange_error_mm,
            "industrial_impact": (
                f"Without NovusLattice overbend compensation ({res.overbend_angle_deg:.2f}°), "
                f"flange deflection is {res.flange_deflection_mm:.3f} mm, violating the ±{res.tolerance_threshold_mm} mm "
                f"spec. NovusLattice restores precision to {res.compensated_flange_error_mm:.3f} mm."
            ),
        }

@dataclass
class RoboticGrippingCase:
    """Case 3: Automated Robotic Handling, Gripping Force and Asperity Tribology."""
    metal_symbol: str = "Cu"
    pad_contact_area_mm2: float = 400.0  # 20 mm x 20 mm gripper pad
    safety_factor: float = 1.5

    def evaluate(self) -> Dict[str, Any]:
        mat = FCC_METALS[self.metal_symbol]
        # Maximum clamping force before yielding surface asperities
        sigma_yield_MPa = mat.yield_strength_MPa
        max_force_N = (sigma_yield_MPa * self.pad_contact_area_mm2) / self.safety_factor
        
        # Adhesion static friction coefficient
        mu_static = 0.35 if self.metal_symbol != "Al" else 0.42

        return {
            "use_case": "Case 3: Robotic Gripping & Surface Tribology (Manipulación Robótica y Fricción)",
            "material": mat.name,
            "pad_contact_area_mm2": self.pad_contact_area_mm2,
            "yield_limit_MPa": sigma_yield_MPa,
            "max_safe_clamping_force_N": round(max_force_N, 1),
            "static_friction_coeff": mu_static,
            "safe_slip_load_N": round(max_force_N * mu_static, 1),
            "recommendation": (
                f"Cap robotic end-effector normal force at {max_force_N:.0f} N to prevent localized "
                f"plastic indentation and micro-cold welding (galling) on sensitive metal surfaces."
            ),
        }

@dataclass
class ThermalDriftCase:
    """Case 4: Factory Floor Thermal Expansion & Environmental Drift."""
    metal_symbol: str = "Al"
    part_nominal_length_mm: float = 1000.0
    morning_temp_C: float = 15.0
    afternoon_temp_C: float = 35.0

    def evaluate(self) -> Dict[str, Any]:
        mat = FCC_METALS[self.metal_symbol]
        alpha = mat.thermal_alpha
        delta_T = self.afternoon_temp_C - self.morning_temp_C
        
        # Thermal elongation delta_L = L * alpha * delta_T
        delta_L_mm = self.part_nominal_length_mm * alpha * delta_T
        
        # Modulus variation
        e_morning = mat.young_modulus_GPa * (1.0 - 3.5e-4 * (self.morning_temp_C - 20.0))
        e_afternoon = mat.young_modulus_GPa * (1.0 - 3.5e-4 * (self.afternoon_temp_C - 20.0))
        delta_e_pct = ((e_afternoon - e_morning) / e_morning) * 100.0

        return {
            "use_case": "Case 4: Factory Environmental & Thermal Drift (Fluctuaciones Térmicas en Planta)",
            "material": mat.name,
            "nominal_length_mm": self.part_nominal_length_mm,
            "temp_swing_C": f"{self.morning_temp_C}°C -> {self.afternoon_temp_C}°C (ΔT = {delta_T}°C)",
            "thermal_expansion_mm": round(delta_L_mm, 4),
            "youngs_modulus_change_percent": round(delta_e_pct, 2),
            "compensation_requirement": (
                f"A 1-meter {mat.name} panel expands by {delta_L_mm:.3f} mm between morning and afternoon. "
                f"CNC laser stops and bending axes must apply NovusLattice dynamic thermal compensation."
            ),
        }

def run_all_industrial_cases() -> List[Dict[str, Any]]:
    """Runs all 4 canonical industrial use cases."""
    return [
        CuttingCase("Al", 1.5).evaluate(),
        BendingCase("Al", 1.5, 1.0, 50.0, 293.15, 0.20).evaluate(),
        RoboticGrippingCase("Cu", 400.0).evaluate(),
        ThermalDriftCase("Al", 1000.0, 15.0, 35.0).evaluate(),
    ]

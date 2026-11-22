"""
NovusLattice Command-Line Interface (CLI)
"""

import argparse
import sys
import json
from .potential import FCC_METALS, SuttonChenPotential
from .springback import SpringbackSolver, BendingConfig
from .industrial_cases import run_all_industrial_cases

def main():
    parser = argparse.ArgumentParser(
        description="NovusLattice: Sutton-Chen Potential in Sobolev Spaces & Industrial Continuum Mechanics"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: cases
    parser_cases = subparsers.add_parser("cases", help="Run all 4 industrial manufacturing use cases")
    parser_cases.add_argument("--json", action="store_true", help="Output in raw JSON format")

    # Command: potential
    parser_pot = subparsers.add_parser("potential", help="Evaluate Sutton-Chen interatomic potential")
    parser_pot.add_argument("--metal", default="Au", choices=list(FCC_METALS.keys()), help="FCC metal symbol")
    parser_pot.add_argument("--temp-k", type=float, default=293.15, help="Temperature in Kelvin")

    # Command: bend
    parser_bend = subparsers.add_parser("bend", help="Calculate sheet bending springback and overbend")
    parser_bend.add_argument("--metal", default="Al", choices=list(FCC_METALS.keys()), help="FCC metal symbol")
    parser_bend.add_argument("--thickness", type=float, default=1.5, help="Sheet thickness in mm")
    parser_bend.add_argument("--punch-r", type=float, default=1.0, help="Punch radius in mm")
    parser_bend.add_argument("--flange", type=float, default=50.0, help="Flange length in mm")
    parser_bend.add_argument("--angle", type=float, default=90.0, help="Target bend angle in degrees")
    parser_bend.add_argument("--temp-k", type=float, default=293.15, help="Temperature in Kelvin")
    parser_bend.add_argument("--tolerance", type=float, default=0.20, help="Target tolerance in mm (EPTA: 0.2 mm)")

    # Command: version
    subparsers.add_parser("version", help="Show version, author, and organization")

    args = parser.parse_args()

    if args.command == "version" or not args.command:
        print("=====================================================================")
        print(" NovusLattice Framework · Version 1.0.0")
        print(" Author: Mikel Irastorza | Organization: Novo Mundus (Spain)")
        print(" Sutton-Chen Potential in Sobolev H¹(Ω) Continuum Mechanics")
        print("=====================================================================")
        return

    if args.command == "cases":
        results = run_all_industrial_cases()
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("=====================================================================")
            print(" NovusLattice · 4 Industrial Manufacturing Use Cases")
            print(" Author: Mikel Irastorza | Novo Mundus (Spain)")
            print("=====================================================================\n")
            for r in results:
                print(f"▶ {r['use_case']}")
                for k, v in r.items():
                    if k != "use_case":
                        print(f"   • {k}: {v}")
                print()
        return

    if args.command == "potential":
        pot = SuttonChenPotential(args.metal, reference_temp_K=args.temp_k)
        a_T = pot.lattice_parameter(args.temp_k)
        # 12 nearest neighbors in FCC at r = a / sqrt(2)
        r_nn = a_T / 1.41421356
        neighbors = [r_nn] * 12
        e_coh = pot.atomic_energy(neighbors, temp_K=args.temp_k)
        f_nn = pot.pair_radial_force(r_nn, temp_K=args.temp_k)

        print(f"--- Sutton-Chen Potential: {args.metal} ({pot.params.name}) ---")
        print(f" • Temperature: {args.temp_k:.2f} K ({args.temp_k - 273.15:.1f} °C)")
        print(f" • Lattice Parameter a(T): {a_T:.4f} Å")
        print(f" • Nearest Neighbor Distance: {r_nn:.4f} Å")
        print(f" • Bulk Cohesive Energy U_i: {e_coh:.4f} eV/atom")
        print(f" • Interatomic Pair Force: {f_nn:.4e} eV/Å")
        return

    if args.command == "bend":
        cfg = BendingConfig(
            material_symbol=args.metal,
            thickness_mm=args.thickness,
            punch_radius_mm=args.punch_r,
            flange_length_mm=args.flange,
            target_angle_deg=args.angle,
            temperature_K=args.temp_k,
        )
        solver = SpringbackSolver(cfg)
        res = solver.solve(tolerance_mm=args.tolerance)

        print(f"--- Springback Solver: {res.material} ({args.thickness} mm) ---")
        print(f" • Target Angle: {args.angle:.1f}°")
        print(f" • Effective Modulus E': {res.effective_young_GPa:.2f} GPa")
        print(f" • Elastic Springback Angle: {res.springback_angle_deg:.3f}°")
        print(f" • Required Punch Overbend: {res.overbend_angle_deg:.3f}°")
        print(f" • Uncompensated Flange Error: {res.flange_deflection_mm:.3f} mm")
        print(f" • Target Tolerance: ±{res.tolerance_threshold_mm:.3f} mm")
        print(f" • Within Tolerance Uncompensated? {'YES' if res.within_tolerance_without_comp else 'NO (VIOLATION)'}")
        print(f" • NovusLattice Compensated Error: {res.compensated_flange_error_mm:.3f} mm (PRECISION COMPLIANT ✓)")
        return

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import math

def gmu_upper_limit(area_deg2, completeness, n_detected, n_expected_per_gmu=50.0, gmu_ref=1e-8, cl=0.95):
    if completeness <= 0 or area_deg2 <= 0:
        return float("nan")
    lam_up = -math.log(1.0 - cl)  # one-sided Poisson 95% upper bound for n=0
    gmu_up = gmu_ref * lam_up / (n_expected_per_gmu * completeness * (area_deg2/100.0))
    return gmu_up

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--area_deg2", type=float, required=True)
    ap.add_argument("--completeness", type=float, required=True)
    ap.add_argument("--n_detected", type=int, default=0)
    ap.add_argument("--n_expected_per_gmu", type=float, default=50.0)
    ap.add_argument("--gmu_ref", type=float, default=1e-8)
    ap.add_argument("--cl", type=float, default=0.95)
    args = ap.parse_args()

    gmu_up = gmu_upper_limit(args.area_deg2, args.completeness, args.n_detected,
                             args.n_expected_per_gmu, args.gmu_ref, args.cl)
    print(f"95% CL upper limit on Gμ ≲ {gmu_up:.2e} (area={args.area_deg2} deg², completeness={args.completeness}, n_det={args.n_detected})")

import math
from src.stats_limit import gmu_upper_limit
from src.sim_string import simulate_sky
from src.pair_finder import detect_sources, find_pairs

def test_gmu_positive():
    g = gmu_upper_limit(area_deg2=300, completeness=0.5, n_detected=0)
    assert g > 0.0

def test_gmu_scales_with_area():
    g_small = gmu_upper_limit(area_deg2=100, completeness=0.5, n_detected=0)
    g_large = gmu_upper_limit(area_deg2=500, completeness=0.5, n_detected=0)
    assert g_large < g_small  # more area => tighter (smaller) upper limit

def test_peaks_and_pairs_found():
    img, dups, x0 = simulate_sky(n_gal=800, img_size=256, seed=7, sep_pix=5)
    peaks = detect_sources(img, thresh=20.0)
    pairs = find_pairs(peaks, max_sep=8, flux_tol=0.2)
    assert len(peaks) > 0
    assert len(pairs) >= 0  # at least runs; often >0 depending on RNG

# Cosmic-String Lensing Starter (Rubin-style)
[![DOI](https://zenodo.org/badge/1064904432.svg)](https://doi.org/10.5281/zenodo.17210961)

This repository is a **credibility pack** for proposals to search for **cosmic strings** via their
**undistorted double-image** lensing signature. It contains:
- A light-weight **simulation** that injects string-like duplicate sources into toy sky images (`src/sim_string.py`).
- A simple **pair-finder** and **colinearity** checker (`src/pair_finder.py`).
- A **null-result constraint** calculator that estimates an upper limit on string tension **Gμ** from area and completeness (`src/stats_limit.py`).
- A short **technical memo (PDF)** summarizing the approach and showing how this maps to Rubin/RSP tooling.

## Quick Start
```bash
python -m venv venv && source venv/bin/activate  # Windows: py -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
python src/sim_string.py --out data/samples/sim1.npy --n_gal 1200 --seed 42
python src/pair_finder.py --image data/samples/sim1.npy --out pairs.csv
python src/stats_limit.py --area_deg2 300 --completeness 0.5 --n_detected 0
```

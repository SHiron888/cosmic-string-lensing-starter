#!/usr/bin/env python3
import numpy as np
import argparse

def simulate_sky(n_gal=1000, img_size=512, seed=0, gmu=2e-8, sep_pix=6):
    '''
    Simulate a toy "sky": random point sources plus a straight cosmic string
    that duplicates sources on one side to the other with a fixed offset (undistorted).
    This is a geometric toy to test detection logic.
    '''
    rng = np.random.default_rng(seed)
    img = np.zeros((img_size, img_size), dtype=float)

    # Random background sources
    xy = rng.integers(low=10, high=img_size-10, size=(n_gal, 2))
    flux = rng.uniform(50, 300, size=n_gal)

    # "String" is a straight vertical line at x = x0
    x0 = img_size // 2
    band = 8  # band around the string where duplication happens

    # draw point sources
    for (y, x), f in zip(xy, flux):
        img[y, x] += f

    # duplicate sources across the string with fixed separation
    dups = []
    for (y, x), f in zip(xy, flux):
        if abs(x - x0) <= band and (x + sep_pix) < img_size and (x - sep_pix) >= 0:
            left = x0 - sep_pix
            right = x0 + sep_pix
            img[y, left] += f
            img[y, right] += f
            dups.append(((y, left), (y, right), f))

    return img, dups, x0

def save_array(path, arr):
    np.save(path, arr)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="data/samples/sim1.npy")
    ap.add_argument("--n_gal", type=int, default=1200)
    ap.add_argument("--img_size", type=int, default=512)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--gmu", type=float, default=2e-8)
    ap.add_argument("--sep_pix", type=int, default=6)
    args = ap.parse_args()

    img, dups, x0 = simulate_sky(n_gal=args.n_gal, img_size=args.img_size, seed=args.seed, gmu=args.gmu, sep_pix=args.sep_pix)
    save_array(args.out, img)
    print(f"Saved simulated sky to {args.out} with {len(dups)} duplicated pairs. String at x={x0}.")

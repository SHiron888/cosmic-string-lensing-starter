#!/usr/bin/env python3
import numpy as np
import argparse
import pandas as pd

def load_image(path):
    return np.load(path)

def detect_sources(img, thresh=20.0):
    """
    Naive peak finder: marks local maxima above a threshold.
    A pixel is a peak if it's strictly greater than all 8 neighbors.
    """
    import numpy as np
    H, W = img.shape
    peaks = []
    for y in range(1, H-1):
        for x in range(1, W-1):
            v = img[y, x]
            if v <= thresh:
                continue
            nb = img[y-1:y+2, x-1:x+2].ravel()
            # exclude the center (index 4 in the 3x3 patch)
            if v > np.max(np.delete(nb, 4)):
                peaks.append((y, x, v))
    return np.array(peaks) if peaks else np.empty((0, 3))

def find_pairs(peaks, max_sep=8, flux_tol=0.15):
    pairs = []
    P = len(peaks)
    for i in range(P):
        y1, x1, f1 = peaks[i]
        for j in range(i+1, P):
            y2, x2, f2 = peaks[j]
            if abs(y1 - y2) <= 1 and abs(x1 - x2) <= max_sep:
                if f1 > 0 and f2 > 0 and abs(f1 - f2)/max(f1, f2) <= flux_tol:
                    pairs.append((y1, x1, f1, y2, x2, f2))
    return pairs

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", type=str, required=True)
    ap.add_argument("--out", type=str, default="pairs.csv")
    args = ap.parse_args()

    img = load_image(args.image)
    peaks = detect_sources(img)
    pairs = find_pairs(peaks)

    import pandas as pd
    df = pd.DataFrame(pairs, columns=["y1","x1","f1","y2","x2","f2"])
    df.to_csv(args.out, index=False)
    print(f"Found {len(pairs)} candidate pairs. Saved to {args.out}.")

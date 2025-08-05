"""
Handles command-line argument parsing and config file loading.
"""
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="GPU‑aware Eulerian motion magnifier")
    parser.add_argument("--in", dest="infile", required=True, help="Input video file")
    parser.add_argument("--out", dest="outfile", default=None, help="Output video file (NOT used for auto-naming with time)")
    parser.add_argument("--low", type=float, default=0.5, help="Low cutoff freq (Hz)")
    parser.add_argument("--high", type=float, default=2.0, help="High cutoff freq (Hz)")
    parser.add_argument("--alpha", type=float, default=15, help="Amplification factor")
    parser.add_argument("--levels", type=int, default=4, help="Pyramid levels")
    parser.add_argument("--order", type=int, default=2, help="Filter order")
    parser.add_argument("--chunk_sec", type=float, default=2, help="Process chunk (seconds)")
    parser.add_argument("--color", choices=["auto", "gray", "color"], default="gray")
    parser.add_argument("--fps", type=float, default=None)
    parser.add_argument("--out_fps", type=float, default=None)
    parser.add_argument("--backend", choices=["auto", "cpu", "cuda", "opencl"], default="auto")
    parser.add_argument("--out_fmt", choices=["avi", "mp4"], default="mp4")
    return parser.parse_args()
"""
Handles amplification logic and the main pipeline.
Includes terminal progress bar with elapsed time in seconds and parameter overlay.
"""

import time
import cv2
import numpy as np
from scipy import signal
from core.pyramid import build_pyramid
from core.filters import apply_temporal_filter
import os

def progress_bar(progress, total, start_time, bar_length=40):
    """
    Prints a simple progress bar with live elapsed seconds.
    Args:
        progress (int): Current chunk number (1-based).
        total (int): Total number of chunks.
        start_time (float): Time the process started, from time.perf_counter().
        bar_length (int): Width of the progress bar display.
    """
    percent = float(progress) / total if total else 1.0
    arrow = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    elapsed = int(round(time.perf_counter() - start_time))
    print(f'\rProcessing: [{arrow + spaces}] {int(percent * 100)}% | Elapsed: {elapsed} sec', end='', flush=True)

def run_amplifier(args):
    """
    Main function coordinating the amplification pipeline.
    Returns: The temporary output video path created (to be renamed later by main.py).
    """
    print("[INFO] Starting motion amplification.")
    cap = cv2.VideoCapture(args.infile)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    out_fps = args.out_fps or fps
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    color_mode = args.color

    nyq = fps / 2.0
    # Ensure frequency band is valid for filter design
    if not (0 < args.low < args.high < nyq):
        raise ValueError(f"Filter frequencies must satisfy 0 < low < high < Nyquist ({nyq} Hz)")

    # Design bandpass filter
    sos = signal.butter(args.order, [args.low, args.high], btype='band', fs=fps, output='sos')
    # Output video setup
    codec = cv2.VideoWriter_fourcc(*('XVID' if args.out_fmt == 'avi' else 'mp4v'))
    temp_out = "amplified_output." + args.out_fmt
    writer = cv2.VideoWriter(temp_out, codec, out_fps, (width, height))

    chunk_frames = int(args.chunk_sec * fps)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    print(f"[INFO] Processing {total_frames} frames in chunks of {chunk_frames}...")

    from io_utils.video_reader import read_chunk
    from io_utils.video_writer import write_frames

    chunk_idx = 0
    total_chunks = (total_frames + chunk_frames - 1) // chunk_frames

    start_time = time.perf_counter()  # For the elapsed time in progress bar

    # Prepare info text base (before processing loop)
    info_text_base = (
        f"Alpha: {args.alpha} | Levels: {args.levels} | Order: {args.order} | "
        f"Freq: {args.low}-{args.high}Hz | Chunk: {args.chunk_sec}s | "
        f"Backend: {args.backend} | Color: {args.color} | "
    )

    while True:
        frames = read_chunk(cap, chunk_frames)
        if not frames:
            break

        luma_stack = build_pyramid(frames, color_mode)
        # For stability: skip too-small chunks (for short videos/last chunk)
        if luma_stack.shape[0] < 31:
            print("[WARN] Skipping small chunk (<31 frames)")
            chunk_idx += 1
            progress_bar(chunk_idx, total_chunks, start_time)
            continue

        luma_out = apply_temporal_filter(luma_stack, sos, args.alpha)
        
        # Update running process time for better reflection
        cur_time = int(round(time.perf_counter() - start_time))
        info_text = info_text_base + f"Time: {cur_time}s"
        
        write_frames(writer, luma_out, frames, color_mode, info_text)
        chunk_idx += 1
        progress_bar(chunk_idx, total_chunks, start_time)

    print()  # Newline after progress bar
    cap.release()
    writer.release()
    print(f"[INFO] Finished initial processing. (Temporary file: {temp_out})")
    return temp_out
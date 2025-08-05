"""
Entrypoint for the motion amplification video processing pipeline.
Handles output file renaming based on processing duration (in seconds).
"""
from io_utils import config_loader
import os
import time

def main():
    args = config_loader.parse_args()
    from core.amplify import run_amplifier

    start_time = time.perf_counter()
    temp_out = run_amplifier(args)  # Get temp output filename
    total_time_sec = int(round(time.perf_counter() - start_time))

    # Build output filename based on input and seconds
    input_name, ext = os.path.splitext(os.path.basename(args.infile))
    final_out = f"{input_name}_{total_time_sec}_sec{ext}"

    # Move/rename the temporary output file
    if os.path.exists(temp_out):
        os.replace(temp_out, final_out)
        print(f"\n[INFO] Processed output saved as: {final_out}")
    else:
        print(f"\n[ERROR] Temporary output {temp_out} not found!")

    print(f"[INFO] Total processing time: {total_time_sec} seconds")

if __name__ == "__main__":
    main()
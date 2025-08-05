"""
Reads frames from a video file.
"""
import cv2

def read_chunk(cap, chunk_frames):
    """
    Reads a fixed number of frames from the video capture.
    Returns a list of frames.
    """
    frames = []
    for _ in range(chunk_frames):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames
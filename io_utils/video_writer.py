"""
Writes luma or color frames to the output video with parameter overlay.
"""
import cv2
import numpy as np

def add_info_overlay(frame, info_text):
    """
    Adds info text as an overlay at the bottom of the frame.
    """
    overlay = frame.copy()
    height, width = overlay.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    y0 = height - 10  # 10 pixels from bottom
    x0 = 10
    # Draw a semi-transparent black rectangle for readability
    cv2.rectangle(overlay, (0, height - 30), (width, height), (0, 0, 0), -1)
    alpha = 0.5
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    # Draw the info text in white
    cv2.putText(frame, info_text, (x0, y0), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    return frame

def write_frames(writer, luma_out, ref_frames, color_mode, info_text):
    """
    Converts processed image data back to video frames,
    overlays info text, and writes them.
    """
    for i, lum in enumerate(luma_out):
        if color_mode == "gray":
            frame_out = (lum * 255).clip(0, 255).astype('uint8')
            frame_out = cv2.cvtColor(frame_out, cv2.COLOR_GRAY2BGR)
        else:
            ycrcb = cv2.cvtColor(ref_frames[i], cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = (lum * 255).clip(0,255).astype('uint8')
            frame_out = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
        frame_out = add_info_overlay(frame_out, info_text)
        writer.write(frame_out)
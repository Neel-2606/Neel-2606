#!/usr/bin/env python3
import os
import sys
import numpy as np
import cv2

def fallback():
    print("WARNING: source-photo.jpg or source-photo.png not found.")
    print("Skipping ASCII portrait generation. Existing neel-ascii.svg will be preserved.")
    sys.exit(0)

def main():
    if os.path.exists("source-photo.jpg"):
        input_path = "source-photo.jpg"
    elif os.path.exists("source-photo.png"):
        input_path = "source-photo.png"
    else:
        fallback()
        return

    print(f"Processing {input_path}...")
    bgr_img = cv2.imread(input_path)
    if bgr_img is None:
        print("Error: Could not read image.")
        sys.exit(1)

    print("Cropping to square...")
    h, w = bgr_img.shape[:2]
    size = min(h, w)
    y1 = (h - size) // 2
    y2 = y1 + size
    x1 = (w - size) // 2
    x2 = x1 + size
    cropped = bgr_img[y1:y2, x1:x2]

    print("Converting to grayscale and applying CLAHE...")
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(gray)

    print("Applying circular mask (profile pic style)...")
    mask = np.zeros((size, size), dtype=np.uint8)
    center = (size // 2, size // 2)
    # Slightly smaller radius to ensure smooth edge
    radius = int((size // 2) * 0.98)
    cv2.circle(mask, center, radius, 255, -1)

    # Composite onto white background
    white_bg = np.ones((size, size), dtype=np.uint8) * 255
    alpha_mask = mask / 255.0
    
    composite = (cl1 * alpha_mask) + (white_bg * (1 - alpha_mask))
    composite = composite.astype(np.uint8)

    out_path = "source-prepped.png"
    cv2.imwrite(out_path, composite)
    print(f"Saved prepped photo to {out_path}")

if __name__ == "__main__":
    main()

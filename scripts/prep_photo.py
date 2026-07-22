#!/usr/bin/env python3
import os
import sys

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

    try:
        from rembg import remove
        from PIL import Image
        import numpy as np
        import cv2
    except ImportError as e:
        print(f"Error importing required libraries: {e}")
        sys.exit(1)

    print(f"Processing {input_path}...")

    with open(input_path, "rb") as f:
        input_bytes = f.read()

    print("Removing background...")
    output_bytes = remove(input_bytes)
    
    import io
    img = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    cv_img = np.array(img)
    b, g, r, a = cv2.split(cv_img)
    bgr_img = cv2.merge([b, g, r])

    print("Converting to grayscale and applying CLAHE...")
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(gray)

    print("Compositing onto white background...")
    h, w = cl1.shape
    white_bg = np.ones((h, w), dtype=np.uint8) * 255
    
    alpha_mask = a / 255.0
    
    composite = (cl1 * alpha_mask) + (white_bg * (1 - alpha_mask))
    composite = composite.astype(np.uint8)

    out_path = "source-prepped.png"
    cv2.imwrite(out_path, composite)
    print(f"Saved prepped photo to {out_path}")

if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import cv2

st.set_page_config(page_title="Photo Editor", layout="centered")
st.title("PHOTO EDITOR APPLICATION")
img_path = r"C:\01_Projects\img_editor\wp14763358-ryusei-shido-wallpapers.png"

# Load image
img = cv2.imread(img_path)

if img is None:
    st.error("Image Not Found")
    st.stop()

# Display original
col1, col2 = st.columns(2)
with col1:
    st.subheader("Original")
    st.image(img, channels="BGR")

# Copy image
edited = img.copy()

# Sidebar
st.sidebar.header("Controls")

# Resize
width = st.sidebar.slider("Width", 100, 1000, edited.shape[1])
height = st.sidebar.slider("Height", 100, 1000, edited.shape[0])
edited = cv2.resize(edited, (width, height))

# Brightness & Contrast
brightness = st.sidebar.slider("Brightness", -100, 100, 0)
contrast = st.sidebar.slider("Contrast", 0.5, 3.0, 1.0)
edited = cv2.convertScaleAbs(edited, alpha=contrast, beta=brightness)

st.sidebar.subheader("Filters")

# Grayscale (safe)
if st.sidebar.checkbox("Grayscale"):
    edited = cv2.cvtColor(edited, cv2.COLOR_BGR2GRAY)
    edited = cv2.cvtColor(edited, cv2.COLOR_GRAY2BGR)

# Blur (fixed)
blur = st.sidebar.slider("Blur", 1, 25, 1, step=2)
if blur > 1:
    edited = cv2.GaussianBlur(edited, (blur, blur), 0)

# Sharpen
if st.sidebar.checkbox("Sharpen"):
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    edited = cv2.filter2D(edited, -1, kernel)

# Warm Filter
if st.sidebar.checkbox("Warm"):
    edited[:,:,2] = cv2.add(edited[:,:,2], 30)

# -------------------------
# Advanced Effects
# -------------------------
st.sidebar.subheader("Advanced Effects")

# Edge Detection
if st.sidebar.checkbox("Edge Detection"):
    gray = cv2.cvtColor(edited, cv2.COLOR_BGR2GRAY)
    edited = cv2.Canny(gray, 100, 200)

# Rotation
angle = st.sidebar.slider("Rotate", 0, 360, 0)
(h, w) = edited.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
edited = cv2.warpAffine(edited, M, (w, h))

# -------------------------
# Display Output
# -------------------------
with col2:
    st.subheader("Edited")
    if len(edited.shape) == 2:
        st.image(edited)
    else:
        st.image(edited, channels="BGR")

# -------------------------
# Download
# -------------------------
success, buffer = cv2.imencode(".png", edited)

st.download_button(
    label="Download Image",
    data=buffer.tobytes(),
    file_name="edited.png",
    mime="image/png"
)
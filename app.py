import streamlit as st
import cv2
import numpy as np
from PIL import Image
from color_detector import load_colors, get_color_name

st.title("🎨 Color Detection Tool")
colors_df = load_colors("colors.csv")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Click to detect color", use_column_width=True)
    image_np = np.array(image.convert('RGB'))

    click = st.image(image_np)
    
    if "click_x" not in st.session_state:
        st.session_state.click_x = st.session_state.click_y = 0

    def on_click(event):
        st.session_state.click_x = int(event.xdata)
        st.session_state.click_y = int(event.ydata)

    # Streamlit currently does not support click callbacks directly. 
    # To handle clicks, you may need to use OpenCV + local interface or use `streamlit-drawable-canvas`.

    st.write("Use OpenCV window for color detection (workaround):")

    if st.button("Open OpenCV Window"):
        img = cv2.imread(uploaded_file.name)
        img = cv2.resize(img, (600, 400))

        def show_color(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                b, g, r = img[y, x]
                color_name = get_color_name(r, g, b, colors_df)
                display = img.copy()
                cv2.rectangle(display, (20, 20), (300, 60), (int(b), int(g), int(r)), -1)
                cv2.putText(display, f"{color_name} ({r},{g},{b})", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow("Color Detection", display)

        cv2.namedWindow("Color Detection")
        cv2.setMouseCallback("Color Detection", show_color)
        cv2.imshow("Color Detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

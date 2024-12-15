import streamlit as st
from PIL import Image
import os
import io

# Folder untuk menyimpan gambar yang diupload dan dikompresi
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# Allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Fungsi untuk memeriksa format file yang diperbolehkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi untuk mengompres gambar
def compress_image(image, quality=50):
    img = Image.open(image)
    compressed_image = io.BytesIO()  # Buffer untuk gambar terkompresi
    img.save(compressed_image, format="JPEG", optimize=True, quality=quality)
    compressed_image.seek(0)  # Kembalikan ke posisi awal setelah menulis
    return compressed_image

# CSS untuk tampilan custom di Streamlit
def custom_css():
    st.markdown("""
    <style>
    body {
        font-family: 'Courier New', Courier, monospace;
        background-color: #1e1e2f;
        color: #fff;
        margin: 0;
        text-align: center;
        padding: 50px;
        image-rendering: pixelated;
    }
    .container {
        display: inline-block;
        background: #3a3a5a;
        border: 4px solid #0056b3;
        box-shadow: 4px 4px #003366;
        padding: 30px;
        border-radius: 8px;
        width: 300px;
    }
    h1 {
        color: #66a3ff;
        font-size: 32px;
        text-transform: uppercase;
    }
    p {
        color: #cce6ff;
    }
    .btn {
        font-size: 20px;
        background-color: #0056b3;
        color: #ffffff;
        padding: 10px 20px;
        border: 2px solid #003366;
        border-radius: 4px;
        text-decoration: none;
        cursor: pointer;
        box-shadow: 2px 2px #003366;
        display: block;
        margin: 10px auto;
    }
    .btn:hover {
        background-color: #66a3ff;
    }
    input[type="file"] {
        display: block;
        margin: 20px auto;
        padding: 5px;
        border: 2px dashed #66a3ff;
        background-color: #3a3a5a;
        color: #cce6ff;
        width: 80%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Streamlit App
def main():
    st.title("Pixel Compress")
    st.write("Compress your photos in a pixelated style!")
    
    # Mengupload gambar
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "gif"])

    # Jika file diupload dan formatnya diperbolehkan
    if uploaded_file is not None and allowed_file(uploaded_file.name):
        # Tampilkan gambar yang diupload
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Kompres gambar
        if st.button("Compress Image"):
            compressed_img = compress_image(uploaded_file)

            # Tampilkan gambar hasil kompresi
            st.image(compressed_img, caption="Compressed Image", use_column_width=True)

            # Tombol untuk mendownload gambar terkompresi
            st.download_button(
                label="Download Compressed Image",
                data=compressed_img,
                file_name=f"compressed_{uploaded_file.name}",
                mime="image/jpeg"
            )

    # Tampilan report
    st.sidebar.title("Report")
    st.sidebar.write("Here you can display your report data or statistics.")

if __name__ == '__main__':
    custom_css()
    main()

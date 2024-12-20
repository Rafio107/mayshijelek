import streamlit as st
from PIL import Image
import io

# Fungsi untuk memeriksa format file yang diperbolehkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Fungsi untuk mengompres gambar dengan tambahan efek resizing (pixelated effect)
def compress_image(image, quality=30, resize_factor=0.5):
    img = Image.open(image)
    
    # Convert image to JPEG format if it is not already JPEG
    if img.mode in ("RGBA", "P"):  # Convert png with transparency to RGB
        img = img.convert("RGB")
    
    # Resize image to create pixelation effect
    width, height = img.size
    new_width = int(width * resize_factor)
    new_height = int(height * resize_factor)
    img_resized = img.resize((new_width, new_height), Image.NEAREST)  # Shrink image
    img_pixelated = img_resized.resize((width, height), Image.NEAREST)  # Scale back to original size
    
    # Compress image with reduced quality
    compressed_image = io.BytesIO()  # Buffer untuk gambar terkompresi
    img_pixelated.save(compressed_image, format="JPEG", optimize=True, quality=quality)
    compressed_image.seek(0)  # Kembali ke posisi awal setelah menulis
    return compressed_image

# CSS untuk tampilan custom di Streamlit
def custom_css():
    st.markdown("""
    <style>
    body {
        font-family: 'Courier New', Courier, monospace;
        background-color: #ADD8E6; /* Latar belakang biru muda */
        color: #000000; /* Warna teks hitam */
        margin: 0;
    }
    h1, h2, h3 {
        text-align: center;
        color: #003366;
    }
    .content {
        text-align: left;
        margin: 0 auto;
        max-width: 800px;
    }
    </style>
    """, unsafe_allow_html=True)

# Halaman 1: Linear Group 5 dan Instruksi
def page1():
    st.title("Welcome to Linear Group 5!")
    st.header("Image Compression Project")

    # Gunakan div khusus agar teks rata kiri
    st.markdown("""
    <div class="content">
        <p>
            This project is developed by <b>Linear Group 5</b> to demonstrate image compression techniques.
            You can navigate through the following pages:
        </p>
        <ul>
            <li><b>Page 1</b>: Introduction and Instructions</li>
            <li><b>Page 2</b>: Team Members</li>
            <li><b>Page 3</b>: Image Compression Tool</li>
        </ul>
        <h3>Instructions:</h3>
        <ol>
            <li>Navigate to <b>Page 3</b>.</li>
            <li>Upload an image (PNG, JPEG, JPG, or GIF).</li>
            <li>Adjust the compression quality and pixelation factor using the sliders.</li>
            <li>Download the compressed image.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.info("Use the sidebar to navigate to other pages.")

# Halaman 2: Anggota Grup
def page2():
    st.title("Our Team Members")
    st.header("Linear Group 5")
    st.write("""
    - **Member 1**: NOVITA AIROTORIA SINAGA (004202300062) 
    - **Member 2**: MAYSHI PERMATASARI EDDYPUTRI (004202300048)
    - **Member 3**: CORAIMA DELANEIRA MEZIA GUSMÃO (004202300085)
    """)
    st.write("We worked together to deliver this awesome image compression app!")

# Halaman 3: Proses Kompresi Gambar
def page3():
    st.title("Pixel Compress")
    st.write("Compress your photos with a pixelated style!")

    # Mengupload gambar
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "gif"])

    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):  # Periksa format file
            # Tampilkan gambar yang diupload
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            # Slider untuk mengatur kualitas dan efek resize
            quality = st.slider("Select Compression Quality (lower = more compression)", 10, 100, 30)
            resize_factor = st.slider("Select Resize Factor (lower = more pixelation)", 0.1, 1.0, 0.5)

            # Kompres gambar
            if st.button("Compress Image"):
                with st.spinner("Compressing..."):
                    try:
                        compressed_img = compress_image(uploaded_file, quality=quality, resize_factor=resize_factor)

                        # Tampilkan gambar hasil kompresi
                        st.image(compressed_img, caption="Compressed Image", use_column_width=True)

                        # Tombol untuk mendownload gambar terkompresi
                        st.download_button(
                            label="Download Compressed Image",
                            data=compressed_img,
                            file_name="compressed_image.jpg",
                            mime="image/jpeg"
                        )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        else:
            st.error("The uploaded file format is not supported. Please upload a valid image.")
    else:
        st.info("Please upload an image file.")

# Main App: Navigasi antar halaman
def main():
    # Sidebar untuk navigasi antar halaman
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Page 1: Introduction", "Page 2: Team Members", "Page 3: Image Compression"])

    custom_css()  # Terapkan CSS

    if page == "Page 1: Introduction":
        page1()
    elif page == "Page 2: Team Members":
        page2()
    elif page == "Page 3: Image Compression":
        page3()

if __name__ == "__main__":
    main()

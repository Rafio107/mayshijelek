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
        background-color: #ADD8E6; /* Ubah latar belakang ke biru muda */
        color: #000000; /* Warna teks hitam */
        margin: 0;
        text-align: center;
        padding: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Streamlit App
def main():
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

if __name__ == "__main__":
    custom_css()
    main()

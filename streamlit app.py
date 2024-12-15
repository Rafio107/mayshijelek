from flask import Flask, render_template_string, request, send_file
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

# CSS Styles for the entire application
css_styles = '''
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
'''

# Homepage
@app.route('/')
def homepage():
    homepage_html = f'''
    {css_styles}
    <div class="container">
        <h1>Pixel Compress</h1>
        <p>Compress your photos in a pixelated style!</p>
        <a href="/compress" class="btn">Start Compressing</a>
        <a href="/report" class="btn">View Report</a>
    </div>
    '''
    return render_template_string(homepage_html)

# Compress Page
@app.route('/compress', methods=['GET', 'POST'])
def compress():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file uploaded", 400

        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        compressed_path = os.path.join(COMPRESSED_FOLDER, f"compressed_{file.filename}")

        file.save(filepath)
        with Image.open(filepath) as img:
            img.save(compressed_path, optimize=True, quality=50)

        return render_template_string(f'''
        {css_styles}
        <div class="container">
            <h1>Image Compressed!</h1>
            <a href="{{{{ url_for('download_file', filename='compressed_{file.filename}') }}}}" class="btn">Download Image</a>
        </div>
        ''')

    compress_html = f'''
    {css_styles}
    <div class="container">
        <h1>Compress Your Image</h1>
        <form id="cropForm" action="/compress" method="POST" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*" required>
            <button class="btn" type="submit">Compress</button>
        </form>
    </div>
    '''
    return render_template_string(compress_html)

# Report Page
@app.route('/report')
def report():
    report_html = f'''
    {css_styles}
    <div class="container">
        <h1>Report</h1>
        <p>Here you can display your report data or statistics.</p>
        <a href="/" class="btn">Back to Home</a>
    </div>
    '''
    return render_template_string(report_html)

# Download compressed file
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(COMPRESSED_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

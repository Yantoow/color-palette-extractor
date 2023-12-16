"""
Author:         Yanto Christoffel
Project Title:  Color Palette Generator
"""

from colorpalette import get_palette, sort_palette_by_hue
from PIL import Image
from flask import Flask, render_template, request, redirect
import base64
from io import BytesIO
import os


class PaletteSettings:
    def __init__(self, k, tol):
        self.k = k
        self.tol = tol

    def set_k(self, value):
        self.k = value

    def set_tol(self, value):
        self.tol = value


app = Flask(__name__)
allowed_exts = {'jpg', 'jpeg','png','JPG','JPEG','PNG'}
settings = PaletteSettings(k=10, tol=100)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Use the previous image
        if request.form.get("generate_again"):
            try:
                img = Image.open("static/images/last_file.png")
            except FileNotFoundError:
                return redirect(request.url)
        # Use a new image
        else:
            if 'file' not in request.files:
                print('No file attached in request')
                return redirect(request.url)

            # Grab the uploaded file
            file = request.files['file']

            if file.filename == '':
                print('No file selected')
                return redirect(request.url)

            if file and is_allowed_file(file.filename):
                img = Image.open(file.stream)
                img.save("static/images/last_file.png")
            else:
                return redirect(request.url)

        # Create a palette
        return show_palette(img)
    else:
        try:
            os.remove("static/images/last_file.png")
        except FileNotFoundError:
            pass
        return render_template('homepage.html', img_data="", current_k=settings.k, current_tol=settings.tol, was_successful=True), 200


def show_palette(img):
    """Uses colorpalette.py to generate a color palette from an image."""
    print(f"Creating palette with k={settings.k}, tol={settings.tol}...")
    palette, was_successful = get_palette(img, settings.k, settings.tol)
    palette = sort_palette_by_hue(palette)
    hex_codes = ['#%02x%02x%02x' % tuple(col) for col in palette]

    img = img.convert('RGB')

    # Pass the encoded image and the palette to the html
    return render_template(
        'homepage.html',
        img_data=encode_img(img),
        palette=hex_codes,
        current_k=settings.k,
        current_tol=settings.tol,
        was_successful=was_successful
    ), 200


@app.route('/k_slider_update', methods=['POST', 'GET'])
def slider_k():
    """Updates the palette length according to the range slider."""
    received_data = request.data
    settings.set_k(int(received_data))
    return received_data

@app.route('/tol_slider_update', methods=['POST', 'GET'])
def slider_tol():
    """Updates the color contrast according to the range slider."""
    received_data = request.data
    settings.set_tol(int(received_data))
    return received_data


def encode_img(img):
    """Encodes the uploaded image in base64."""
    with BytesIO() as buf:
        img.save(buf, 'jpeg')
        image_bytes = buf.getvalue()
    return base64.b64encode(image_bytes).decode()


def is_allowed_file(filename):
    """Checks if a file is a proper image."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


if __name__ == "__main__":
    app.run(debug=True)

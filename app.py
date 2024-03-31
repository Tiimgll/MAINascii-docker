from flask import Flask, render_template, request, redirect, send_file
from PIL import Image
import io
import base64
from ascii_image import image_resize, image_to_ascii_greyscale
from ascii_image import adjust_brightness, adjust_contrast

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    
    img = Image.open(file.stream)
    img = image_resize(img, width=100)
    ascii_list = image_to_ascii_greyscale(img, 100, ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@'])
    ascii_image = '\n'.join(ascii_list)
    
    # Convert ASCII image to base64
    ascii_bytes = ascii_image.encode('utf-8')
    base64_bytes = base64.b64encode(ascii_bytes)
    base64_ascii_image = base64_bytes.decode('utf-8')
    
    return render_template('result.html', ascii_image=ascii_image, base64_ascii_image=base64_ascii_image)

@app.route('/save', methods=['POST'])
def save_ascii_image():
    ascii_image = request.form['ascii_image']
    with open('ascii_image.txt', 'w') as f:
        f.write(ascii_image)
    return send_file('ascii_image.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

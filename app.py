from flask import Flask, render_template, request, redirect, send_file
from PIL import Image
import io
import base64
import requests
from io import BytesIO
from ascii_image import image_resize, image_to_ascii_greyscale

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
    resolution = int(request.form['resolution'])
    img = image_resize(img, width=resolution)
    ascii_list = image_to_ascii_greyscale(img, resolution, ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@'])
    ascii_image = '\n'.join(ascii_list)
    
    # Convert ASCII image to base64
    ascii_bytes = ascii_image.encode('utf-8')
    base64_bytes = base64.b64encode(ascii_bytes)
    base64_ascii_image = base64_bytes.decode('utf-8')
    
    return render_template('result.html', ascii_image=ascii_image, base64_ascii_image=base64_ascii_image)

@app.route('/convert_url', methods=['POST'])
def convert_url():
    image_url = request.form['image_url']
    resolution = int(request.form['resolution'])
    img = get_image_from_url(image_url)
    img = image_resize(img, width=resolution)
    ascii_list = image_to_ascii_greyscale(img, resolution, ['.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@'])
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

def get_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

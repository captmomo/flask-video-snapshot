from flask import Flask, render_template, request
from app import app
import re
from pixel_image import pixelate_image, generate_pixel_image
import binascii

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input = request.json
    image_data = re.sub('^data:image/.+;base64,', '', input['img'])
    image_ascii = generate_pixel_image(image_data)
    return image_ascii
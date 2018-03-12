from flask import Flask, render_template, request
from app import app
import re
from pixel_image import pixelate_image, generate_pixel_image, classify_face



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face_classify')
def face_classify():
    return render_template('face_classify.html')


@app.route('/test')
def test():
    return render_template('testpage.html')


@app.route('/test2')
def test2():
    return render_template('testpage_2.html')


@app.route('/process', methods=['POST'])
def process():
    input = request.json
    image_data = re.sub('^data:image/.+;base64,', '', input['img'])
    image_ascii = generate_pixel_image(image_data)
    return image_ascii

@app.route('/classify', methods=['POST'])
def classify():
    input = request.json
    image_data = re.sub('^data:image/.+;base64,', '', input['img'])
    image_ascii = classify_face(image_data)
    return image_ascii

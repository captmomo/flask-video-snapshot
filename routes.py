from flask import Flask, render_template, request
from app import app
import re
from pixel_image import pixelate_image, generate_pixel_image, classify_face, atkinson_dither

hex_list = []
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face_streaming')
def face_streaming():
    return render_template('face_classify_stream.html')

@app.route('/face_classify')
def face_classify():
    return render_template('face_classify.html')


@app.route('/test')
def test():
    return render_template('testpage.html')


@app.route('/test2')
def test2():
    return render_template('testpage_2.html')

@app.route('/focus', methods=['POST','GET'])
def focus():
    if request.method == 'POST':
        hex_list.append('#')
    else:
        if len(hex_list) != 0:
            hex_list.pop()

    hex_string = ' '.join(hex_list)
    if len(hex_list) == 0:
        hex_string = 'dead'
    return hex_string



@app.route('/process', methods=['POST'])
def process():
    input = request.json
    image_data = re.sub('^data:image/.+;base64,', '', input['img'])
    image_ascii = atkinson_dither(image_data)
    return image_ascii


@app.route('/classify', methods=['POST'])
def classify():
    input = request.json
    image_data = re.sub('^data:image/.+;base64,', '', input['img'])
    image_ascii = classify_face(image_data)
    return image_ascii

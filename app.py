from flask import Flask, session, g,\
                  render_template, request,\
                  redirect, url_for, make_response,\
                  jsonify, flash, json
import numpy as np
from PIL import Image
import base64
import io


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ujewhfijqehfjqhfehihdhwebc22e2imagesForDimasicAndVanyokiu3hye8u23ugrf3fjwhefdiqbfhjqhiyhqeojfbqe'
UPLOAD_FOLDER = 'static/data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    '''
    Дана функція завантажує датасет
    та видає результат аналізу
    '''
    if (request.method == 'POST') and ('image' in request.files):

        photo = request.files['image']

        if photo.filename == '':
            flash("File is not choosen! \
                  Choose file before pressing that button.")
            return redirect(url_for('index'))

        if allowed_file(photo.filename) is False:
            flash("File extension is not allowed! \
                   Our service can handle only jpeg files.")
            return redirect(url_for('index'))

        im = Image.open(photo)
        data = io.BytesIO()
        im.save(data, "jpeg")
        encoded_img_data = base64.b64encode(data.getvalue())

        description = "There should go prediction"

        return render_template("predictions.html",
                               img_data=encoded_img_data.decode('utf-8'),
                               description=description)

    return render_template('error404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
        Роут, що переводить на
        головну сторінку програми
    '''
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    '''
    Ця функція відловлює невідомі роути
    та перенаправляє на сторінку 404.
    '''
    return render_template('error404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)

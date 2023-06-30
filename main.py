from flask import *

from detect_and_measure import *

app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/detect-and-measure', methods=['POST'])
def success():
    if request.method == 'POST':
        multiplier = request.args.get('multiplier')
        f = request.files['file']
        f.save(f.filename)
        width, length, height, volume = detect_and_measure(f.filename, multiplier)

        data = {
            'name': 'from truck AH 0000 AE',
            'width': width,
            'length': length,
            'height': height,
            'volume': volume
        }

        return jsonify(data)
        # return render_template("success.html", name=f.filename,
        #                        width=width, length=length, height=height,
        #                        volume=volume, path='detected_cargo.jpg')

@app.route('/detected_cargo.jpg')
def get_detected_cargo():
    return send_file('static/detected_cargo.jpg', mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

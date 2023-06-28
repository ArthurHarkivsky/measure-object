from flask import *

from detect_and_measure import *

app = Flask(__name__)


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/detect-and-measure', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        width, length, height, volume = detect_and_measure(f.filename)

        data = {
            'width': width + ' meters',
            'length': length + ' meters',
            'height': height + ' meters',
            'volume': volume + ' cubic meters',
        }

        return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

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

        return render_template("success.html", name=f.filename,
                               width=width, length=length, height=height,
                               volume=volume)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

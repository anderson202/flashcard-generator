from flask import Flask, request, Response
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route("/api/upload", methods=["POST"])
@cross_origin()
def upload():
    print(request.files)
    if "files" not in request.files:
        print("no file");
        return "No file found", 400

    file = request.files["files"]

    if file.filename == "":
        return "No file selected", 400

    file.save(file.filename)

    # response = flask.jsonify({'some': 'data'})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return ""

if __name__ == "__main__":
    app.run(debug=True)

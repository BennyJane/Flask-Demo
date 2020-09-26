from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "<h5>app.py内完成Flask的实例化  .flaskenv:</h5><h1>FLASK_APP=demo.app</h1>"


if __name__ == '__main__':
    app.run(debug=True)

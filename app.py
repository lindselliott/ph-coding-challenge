from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/test')
def testing():
    return "Hello, Flask! testing route"

if __name__ == '__main__':
    app.run(debug=True)
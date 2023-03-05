from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Watching Youtube'

if __name__ == '__main__':
    app.run(host='  ', port=80)
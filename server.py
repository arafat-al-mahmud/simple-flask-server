import atexit
from flask import Flask, request, render_template, redirect, url_for
from utils import read_configuration
from storages import DatabaseBackend

app = Flask(__name__)

@app.route('/')
def index():
    quotes = backend.list_quotes()
    return render_template('index.html', quotes=quotes)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        data = {'quote' : request.form['quote'], 'author' : request.form['author']}
        backend.add_quote(data)
        return redirect('/')

if __name__ == '__main__':

    backend = DatabaseBackend()
    backend.on_start()
    atexit.register(backend.on_exit)

    config = read_configuration()
    hostname = config['hostname']
    port = int(config['port'])

    app.run(host=hostname, port=port)
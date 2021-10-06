from threading import current_thread
from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy
import string
import random



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Good_urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    orig_url = db.Column("orig_url", db.String())
    short_url = db.Column("short_url", db.String(10))

    def __init__(self, orig_url, short_url):
        self.orig_url = orig_url
        self.short_url = short_url

def make_it_shorter():
    letters = string.ascii_letters
    while True:
        url_letters = random.choices(letters, k=3)
        url_letters = ''.join(url_letters)
        print(url_letters)
        short = Good_urls.query.filter(Good_urls.short_url == url_letters).all()
        if not short:
            return url_letters

db.create_all()


@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == "POST":
        #get the input url
        long_url = request.form['long_url']
        print(long_url)
        #see if it is in the database already
        current_url = Good_urls.query.filter(Good_urls.orig_url == long_url).all()

        if current_url:
            #return the already shortended one if it is
            return render_template('newurl.html', new_url = current_url[0].short_url)
        else: 
            #create short url
            url_extension = make_it_shorter()
            #add long and short url into one object
            new_obj = Good_urls(long_url, url_extension)
            #add them into thedata base
            db.session.add(new_obj)
            db.session.commit()
            #return the shorter URL
            return render_template('newurl.html', new_url=long_url)
    else:
        return render_template('home.html')

@app.route('/<short_url>')
def check_url(short_url):
    og_url = Good_urls.query.filter_by(short_url = short_url).all()
    if og_url:
        return redirect(og_url.orig_url)
    else: 
        return f"<h1>No such URL pal - maybe you need to try again?</h1>"

@app.errorhandler(exceptions.NotFound)
def not_found_404(request, exception):
    data = { 'err': exception }
    return render_template('errors/404.html', data), 404

@app.errorhandler(exceptions.MethodNotAllowed)
def handle_405(err):
    return render_template('errors/405.html'), 405

@app.errorhandler(exceptions.InternalServerError)
def server_error_500(request):
    return render_template('errors/500.html'), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
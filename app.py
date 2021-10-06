from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy



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

    # def shorten_url():
    #     letters = string.ascii_lowercase + string.ascii_uppercase
    #     while True:
    #         rand_letters = random.choices(letters, k=3)
    #         rand_letters = "".join(rand_letters)
    #         short_url = Urls.query.filter_by(short=rand_letters).first()
    #         if not short_url:
    #             return rand_letters

db.create_all()


@app.route('/', methods = ['POST', 'GET'])
def home():
    if request.method == "POST":
        long_url = request.form['long_url']
        return long_url
    else:
        return render_template('home.html')

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
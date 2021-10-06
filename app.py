from flask import Flask, jsonify, redirect, render_template, request
from flask_cors import CORS
from werkzeug import exceptions

app = Flask(__name__,  template_folder='templates')
CORS(app)

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
    app.run(debug=True)
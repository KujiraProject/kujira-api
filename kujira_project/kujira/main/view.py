from flask import render_template
from kujira.main import INDEX_PAGE


@INDEX_PAGE.route('/')
def index():
    return render_template('index.html')

from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def showCategory():
    return ('categories here!!!')


@app.route('/<int:category_id>/')
def showCategoryItems():
    return ('show items here!!!')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=8000)

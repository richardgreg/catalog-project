from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def showCategory():
    return ('All categories here!!!')


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item')
def showCategoryItems(category_id):
    return ('show items here!!!')


@app.route('/category/<int:category_id>/item/new',
           methods=['GET', 'POST'])
def newCategoryItem(category_id):
    return('new item here!!!')


@app.route('/category/<int:category_id>/item/<int:category_item_id>')
def categoryItemDescription(category_id, category_item_id):
    return('Description of item here!!!')


@app.route('/category/<int:category_id>/item/<int:category_item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, category_item_id):
    return('Delete item here!!!')


@app.route('/category/<int:category_id>/item/<int:category_item_id>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_id, category_item_id):
    return('Delete item here!!!')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='localhost', port=8000)

from flask import Flask, render_template, url_for

app = Flask(__name__)

# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'},
                {'name':'Blue Burgers', 'id':'2'},
                {'name':'Taco Hut', 'id':'3'}]


# Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese',
        'price':'$5.99','course' :'Entree', 'id':'1'},
        {'name':'Chocolate Cake','description':'made with Dutch Chocolate',
        'price':'$3.99', 'course':'Dessert','id':'2'},
        {'name':'Caesar Salad',
        'description':'with fresh organic vegetables','price':'$5.99',
        'course':'Entree','id':'3'},
        {'name':'Iced Tea',
        'description':'with lemon','price':'$.99', 'course':'Beverage',
        'id':'4'},
        {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach',
        'price':'$1.99', 'course':'Appetizer','id':'5'} ]

item =  {'name':'Cheese Pizza','description':'made with fresh cheese',
        'price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/categories')
def showCategories():
    return render_template ('categories.html', res=restaurants)


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item')
def showCategoryItems(category_id):
    return render_template ('categoryitem.html', items=items, category_id=category_id)


@app.route('/category/<int:category_id>/item/new',
           methods=['GET', 'POST'])
def newCategoryItem(category_id):
    return render_template ('newcategoryitem.html', category_id=category_id)


@app.route('/category/<int:category_id>/item/<int:category_item_id>')
def categoryItemDescription(category_id, category_item_id):
    return render_template ('categoryiteminfo.html', category_id=category_id,
                            category_item_id=category_item_id)


@app.route('/category/<int:category_id>/item/<int:category_item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, category_item_id):
    return render_template ('editcategoryitem.html', category_id=category_id,
                            category_item_id=category_item_id)


@app.route('/category/<int:category_id>/item/<int:category_item_id>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_id, category_item_id):
    return render_template ('deletecategoryitem.html', category_id=category_id,
                            category_item_id=category_item_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

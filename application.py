#!/usr/bin/env python3
from flask import Flask, render_template, url_for, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Category, CategoryItem, Base
app = Flask(__name__)
engine = create_engine('sqlite:///bookcatalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


@app.route('/')
@app.route('/categories')
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', cat=categories)


@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item')
def showCategoryItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    i = session.query(CategoryItem).filter_by(category_id=category_id)
    category_items = i
    return render_template('categoryitem.html', items=category_items,
                           category_id=category_id, category=category)


@app.route('/category/<int:category_id>/item/new',
           methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if request.method == 'POST':
        new_item = CategoryItem(title=request.form['title'],
                                description=request.form['description'],
                                author=request.form['author'],
                                category_id=category_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('showCategories', category_id=category_id))
    else:
        return render_template('newcategoryitem.html',
                               category_id=category_id)


@app.route('/category/<int:category_id>/item/<int:category_item_id>')
def categoryItemDescription(category_id, category_item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    i = session.query(CategoryItem).filter_by(category_id=category_id)
    category_item = i.filter_by(id=category_item_id)

    return render_template('categoryiteminfo.html', category_id=category_id,
                           category_item_id=category_item_id,
                           cat_item=category_item,
                           category=category)


@app.route('/category/<int:category_id>/item/<int:category_item_id>/edit',
           methods=['GET', 'POST'])
def editCategoryItem(category_id, category_item_id):
    i = session.query(CategoryItem).filter_by(id=category_item_id).one()
    item_to_edit = i
    if request.method == 'POST':
        if request.form['title']:
            item_to_edit.title = request.form['title']
        if request.form['description']:
            item_to_edit.description = request.form['description']
        if request.form['author']:
            item_to_edit.author = request.form['author']
        session.add(item_to_edit)
        session.commit()
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('editcategoryitem.html',
                               category_id=category_id,
                               category_item_id=category_item_id,
                               item=item_to_edit)


@app.route('/category/<int:category_id>/item/<int:category_item_id>/delete',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_id, category_item_id):
    return render_template('deletecategoryitem.html', category_id=category_id,
                           category_item_id=category_item_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

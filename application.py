#!/usr/bin/env python3
# Bare app functionality imports
from flask import (Flask, render_template, url_for,
                   redirect, request, jsonify, flash)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, CategoryItem, Base, User

# Import for login session and anti-forgery state token
from flask import session as login_session
import random
import string

# Imports for handling google-signin callback method in template
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from functools import wraps


app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///bookcatalog.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Declare google auth client ID by referencing the client secrets file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Book-ish"


# Create a state token to prevent request forgery
# Store it in the session for later validation.
# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('''Current user
                                             is already logged-in.'''),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if user exists, if it doesn't make one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Brief welcom message before redirecting to homepage
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = "width: 300px; height: 300px;border-radius: 150px; '
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("Welcome %s!" % login_session['username'])
    print("done!")
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except ImportError:
        return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        reply = 'Current user not connected.'
        response = make_response(json.dumps(reply), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    revoke_url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
    url = revoke_url % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print(response)
        flash("You have successfully been logged out!!")
        return redirect(url_for('showCategories'))
    else:
        reply = 'Failed to revoke token for given user.'
        response = make_response(json.dumps(reply), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Book Information
@app.route('/category/<int:category_id>/item/JSON')
def categoryItemJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    x = session.query(CategoryItem).filter_by(category_id=category_id)
    items = x
    return jsonify(CategoryItems=[i.serialize for i in items])


# Display available categories
@app.route('/')
@app.route('/categories/')
def showCategories():
    categories = session.query(Category).all()
    return render_template('categories.html', cat=categories)


# Show all items related to category
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/item/')
def showCategoryItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    i = session.query(CategoryItem).filter_by(category_id=category_id)
    # x = session.query(CategoryItem).filter_by(category_id=category_id).one()
    category_items = i
    # category_item = x
    # creator = session.query(User).filter_by(id=category_item.id)
    if 'username' not in login_session:

        return render_template('publiccategoryitem.html', category=category,
                               items=category_items, category_id=category_id)
    else:
        # creator = session.query(User).filter_by(id=category_item.id)
        return render_template('categoryitem.html', items=category_items,
                               category_id=category_id, category=category,
                               email=login_session['email'])


# Create a new category item
@app.route('/category/<int:category_id>/item/new/',
           methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if "username" not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        new_item = CategoryItem(title=request.form['title'],
                                description=request.form['description'],
                                author=request.form['author'],
                                category_id=category_id,
                                user_id=login_session['user_id'],
                                user_email=login_session['email'])
        session.add(new_item)
        session.commit()
        flash("New catalog item successfully addded!!!")
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('newcategoryitem.html',
                               category_id=category_id, category=category)


# Display more Information about a specific item
@app.route('/category/<int:category_id>/item/<int:category_item_id>/')
def categoryItemDescription(category_id, category_item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    i = session.query(CategoryItem).filter_by(category_id=category_id)
    category_item = i.filter_by(id=category_item_id)
    # creator = session.query(User).filter_by(id=category_item.user_id)
    return render_template('categoryiteminfo.html', category_id=category_id,
                           category_item_id=category_item_id,
                           cat_item=category_item,
                           category=category)


# Edit a specific BOOK item
@app.route('/category/<int:category_id>/item/<int:category_item_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editCategoryItem(category_id, category_item_id):
    i = session.query(CategoryItem).filter_by(id=category_item_id).one_or_none()
    item_to_edit = i
    # Java script Authorization code
    if item_to_edit.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
         "to delete this restaurant. Please create your own restaurant" \
         "in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['title']:
            item_to_edit.title = request.form['title']
        if request.form['description']:
            item_to_edit.description = request.form['description']
        if request.form['author']:
            item_to_edit.author = request.form['author']
        session.add(item_to_edit)
        session.commit()
        flash("Catalog item successfully edited!!!")
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('editcategoryitem.html',
                               category_id=category_id,
                               category_item_id=category_item_id,
                               item=item_to_edit)


# Delete a book item
@app.route('/category/<int:category_id>/item/<int:category_item_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteCategoryItem(category_id, category_item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    i = session.query(CategoryItem).filter_by(id=category_item_id).one()
    item_to_be_deleted = i
    # Java script Authorization code
    if item_to_be_deleted.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized "\
         "to delete this restaurant. Please create your own restaurant" \
         "in order to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(item_to_be_deleted)
        session.commit()
        flash("Catalog item successfully deleted!!!")
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('deletecategoryitem.html',
                               category_id=category_id,
                               category_item_id=category_item_id,
                               item=item_to_be_deleted, category=category)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)

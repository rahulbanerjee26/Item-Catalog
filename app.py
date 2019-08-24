#!/usr/bin/env python

from flask import Flask,render_template,redirect,request,url_for,flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from databaseSetup import User,Category,Item,Base
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2 
import json
import requests
from flask import make_response 


CLIENT_ID = json.loads(open('client_secrets.json','r').read()) ['web'] ['client_id']


#Configuration
engine = create_engine('sqlite:///itemCatalog.db',
connect_args={'check_same_thread': False})
Base.metadata.create_all(engine) 
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

login_session = {}
login_session['LoggedIn']= False


# ----------
# Home Route
# ----------

@app.route('/')
def home():
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    items = session.query(Item).all()
    sizeItems = len(items)
    return render_template('home.html', categories = categories, sizeCategories = sizeCategories, items = items, sizeItems = sizeItems, login_session = login_session ),200

# -------------------
# CRUD for Categories
# -------------------

# Create
@app.route('/createCategory', methods= ['GET','POST'])
def createCategory():
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    if login_session['LoggedIn'] == False:
        return render_template('pleaseLogin.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    if(request.method == 'GET'):
        return render_template('createCategory.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    name = request.form['name']
    user_id = session.query(User).filter_by(email = login_session['email']).one().id
    category = Category(name = name,user_id = user_id)
    session.add(category)
    session.commit()
    flash('Created Category')
    return redirect(url_for('home')),303

#Read
@app.route('/viewCategories')
def viewCategories():
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    return render_template('viewCategories.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session ),200 

#Update
@app.route('/<int:id>/updateCategory',methods = ['GET','POST'])
def updateCategory(id):
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    category = session.query(Category).get(id)
    if login_session['LoggedIn'] == False:
        return render_template('pleaseLogin.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    if(category.user.email != login_session['email']):
        return render_template('unauthorized.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session,user = category.user)
    if(request.method == 'GET'):
        return render_template('updateCategory.html',selectedCategory = category,categories = categories,sizeCategories = sizeCategories, login_session = login_session ),200
    name = request.form['name']
    category.name = name
    session.add(category)
    session.commit()
    flash('Updated Category')
    return redirect(url_for('home')),303

#Delete
@app.route('/<int:id>/deleteCategory',methods = ['GET','POST'])
def deleteCategory(id):
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    category = session.query(Category).get(id)
    if login_session['LoggedIn'] == False:
        return render_template('pleaseLogin.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    items = session.query(Item).filter_by(category_id = id).all()
    if(category.user.email != login_session['email']):
        return render_template('unauthorized.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session,user = category.user)
    if(request.method == 'GET'):
        return render_template('deleteCategory.html',selectedCategory = category,categories = categories,sizeCategories = sizeCategories,items = items, login_session = login_session ),200

    for item in items:
        session.delete(item) 
    session.delete(category)
    session.commit()
    flash('Deleted Category')
    return redirect(url_for('home')),303

# ---------------------
# CRUD for Category end
# ---------------------   

# --------------
# CRUD for Items 
# --------------

# Create
@app.route('/createItem',methods = ['GET','POST'])
def createItem():
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    if login_session['LoggedIn'] == False:
        return render_template('pleaseLogin.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    if(request.method == 'GET'):
        return render_template('createItem.html', categories = categories, sizeCategories = sizeCategories, login_session = login_session )

    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    id = session.query(Category).filter_by(name = category).one().id 
    user_id = session.query(User).filter_by(email = login_session['email']).one().id
    item = Item(name = name, description = description, category_id = id,user_id = user_id)
    session.add(item)
    session.commit()
    flash('Created Item')
    return redirect(url_for('home')),303



# Read all Items
@app.route('/<int:id>/viewItems')
def viewItems(id):
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    category = session.query(Category).get(id)
    items = session.query(Item).filter_by(category_id = id).all()
    sizeItems = len(items)
    return render_template('viewItems.html',categories = categories, sizeCategories = sizeCategories,items = items,sizeItems = sizeItems,category = category, login_session = login_session )



# Read a specific item
@app.route('/<int:id>/viewItem')
def viewItem(id):
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    item = session.query(Item).get(id)
    return render_template('viewItem.html',categories = categories, sizeCategories = sizeCategories,item = item, login_session = login_session )
    

# Update
@app.route('/<int:id>/updateItem',methods=['GET','POST'])
def updateItem(id):
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    item = session.query(Item).get(id)
    if login_session['LoggedIn'] == False:
        return render_template('pleaseLogin.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    if(item.user.email != login_session['email']):
        return render_template('unauthorized.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session,user = item.user)
    if request.method == 'GET':
        return render_template('updateItem.html',categories = categories, sizeCategories = sizeCategories,item = item, login_session = login_session )
    name = request.form['name']
    description = request.form['description']
    category = request.form['category']
    id = session.query(Category).filter_by(name = category).one().id 
    item.name = name
    item.description = description
    item.category_id = id
    session.add(item)
    session.commit()
    flash('Updated Item')
    return redirect(url_for('home')),303




# Delete
@app.route('/<int:id>/deleteItem',methods = ['GET','POST'])
def deleteItem(id):
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    item = session.query(Item).get(id)
    if login_session['LoggedIn'] == False:
        return render_template('pleaseLogin.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session)
    if(item.user.email != login_session['email']):
        return render_template('unauthorized.html',categories = categories,sizeCategories = sizeCategories, login_session = login_session,user = item.user)
    if(request.method == 'GET'):
        return render_template('deleteItem.html', categories = categories, sizeCategories = sizeCategories,item = item, login_session = login_session )
    session.delete(item)
    session.commit()
    flash('Deleted Item')
    return redirect(url_for('home')),303

# ------------------
# CRUD for Items End
# ------------------ 

#  ----------------
#  Helper Functions
#  ----------------

def createUser(login_session):
    newUser = User( name = login_session['name'],
                    email = login_session['email'],
                    picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUser(user_id):
    result = session.query(User).get(user_id)
    return result    

def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None 
#  --------------------
#  Helper Functions End
#  --------------------  

# ------------
# Log in Route
# ------------
@app.route('/login')
def login():
    #generating anti-forgery state token
    categories = session.query(Category).all()
    sizeCategories = len(categories)
    state = "".join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))    
    login_session['state'] = state
    return render_template('login.html',STATE=state,categories = categories, sizeCategories = sizeCategories, login_session = login_session )

# -------------
# Log Out Route
# -------------
@app.route('/logout')
def logout():
    if(login_session['provider'] == 'facebook'):
        return redirect(url_for('fbdisconnect')),303
    else:
        return redirect(url_for('gdisconnect')),303


# --------------
# Google Account
# --------------

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print('Inavlid state token')
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object which contains
        # access token
        #creating oauth flow object by passing credentials 
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # specify with postmessage that the server is sending off the one time 
        # authorization code
        oauth_flow.redirect_uri = 'postmessage'
        # finally exchange the one time authorization code for credentials object
        credentials = oauth_flow.step2_exchange(code)
    #if there was an error, an a FlowExchangeError exception will be thrown    
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print('FlowExchangeError')
        return response

    # Get access token from the credentials object
    access_token = credentials.access_token
    # google api validates the acces token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # get request to store the result       
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error dueing GET, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        print('GET Error')
        return response

    # Verify that the result object with validated access token 
    # has the same user id as the user id
    # in the credentials object
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        print('Valid acces token but not same user')
        return response

    # Verify that the result object with 
    # validated access token has same client id as original client id.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        print('mismatch in client id')
        return response

    # Check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        print('user is already logged in')
        return response

    # if none of the if statements are triggered, we have a valid access token
    # and user is signed in. They can now make API calls and we have the info
    print('No coditions triggered')    

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    # data is json with all the user's info
    data = answer.json()

    #storing info in login session
    login_session['gplus_id'] = gplus_id
    login_session['name'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    login_session['LoggedIn']= True

    #storing user info in database
    user_id = getUserId(login_session['email'])
    if not user_id:
        createUser(login_session)
    login_session['user_id'] = user_id


    #display redirect message
    output = ''
    output += '<h1>Welcome, '
    output += login_session['name']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['name'])
    return output

@app.route('/gdisconnect')
def gdisconnect():
    #get the current session's acces token
    access_token = login_session.get('access_token')

    #user is no logged in so no need to log out
    if access_token is None:
        print ('No user logged in')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['name'])
    # revoke the token to log out
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    # result stores the returned json object
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)

    # if successful delete all info from the login session
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['name']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        del login_session['user_id']
        login_session['LoggedIn']= False
        flash('Successfuly Logged Out')
        return redirect(url_for('home')),303

# --------------------
# Google Account Close
# --------------------


# ----------
# FB Account
# ----------

@app.route('/fbconnect',methods=['POST'])
def fbconnect():
    #check state
    if login_session['state'] != request.args.get('state'):
        response = make_response(json.dumps('Wrong state token',400))
        response.headers['content-type'] = 'application/json'
        return response
    access_token = request.data

    #upgrade access token to credentials object
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    #get info in json format
    data = json.loads(result)
    login_session['name'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['provider'] = 'facebook'
    login_session['access_token'] = token
    login_session['LoggedIn']= True

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['name']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['name'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    #revoking access
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['access_token']
    del login_session['facebook_id'] 
    del login_session['name']
    del login_session['email']
    del login_session['picture']
    del login_session['provider']
    login_session['LoggedIn']= False
    flash('Successfuly Logged Out')
    return redirect(url_for('home')),303

# ----------------
# FB Account Close
# ----------------

# ---------
# JSON DATA
# ---------
@app.route('/items/JSON')
def itemsJSON():
    items = session.query(Item).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/item/<int:id>/JSON')
def itemJSON(id):
    item = session.query(Item).get(id)
    return jsonify(Item= item.serialize)

@app.route('/categories/JSON')
def categoriesJSON():
    items = session.query(Category).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/category/<int:id>/JSON')
def categoryJSON(id):
    category = session.query(Category).get(id)
    return jsonify(Category= category.serialize)

@app.route('/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(Users=[i.serialize for i in users])

@app.route('/user/<int:id>/JSON')
def userJSON(id):
    user = session.query(User).get(id)
    return jsonify(User=user.serialize)

# -------------
# JSON Data End
# -------------

if __name__ == '__main__':
    app.secret_key = "my_secret_key"
    app.run(host='0.0.0.0', port=5000)
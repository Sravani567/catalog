from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, CompanyName, ItemName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime
engine = create_engine('sqlite:///cosmetics.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Cosmetics"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
ars_rat = session.query(CompanyName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    ars_rat = session.query(CompanyName).all()
    ares = session.query(ItemName).all()
    return render_template(
        'login.html', STATE=state, ars_cat=ars_rat, ares=ares)
    # return render_template('myhome.html', STATE=state
    # ars_rat= ars_rat,ares=ares)


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
    result = json.loads(h.request(url, 'GET')[1])
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
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the for session later use.
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

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
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
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
# Home


@app.route('/')
@app.route('/home')
def home():
    ars_rat = session.query(CompanyName).all()
    return render_template('myhome.html',  ars_rat=ars_rat)
#####
# Cosmetic Hub for admins


@app.route('/CosmeticHub')
def CosmeticHub():
    try:
        if login_session['username']:
            name = login_session['username']
            ars_rat = session.query(CompanyName).all()
            ars = session.query(CompanyName).all()
            ares = session.query(ItemName).all()
            return render_template('myhome.html', ars_rat=ars_rat,
                                   ars=ars, ares=ares, uname=name)
    except:
        return redirect(url_for('showLogin'))

######
# Showing cosmeticss based on  company


@app.route('/CosmeticHub/<int:arid>/AllCosmetics')
def showCosmetics(arid):
    ars_rat = session.query(CompanyName).all()
    ars = session.query(CompanyName).filter_by(id=arid).one()
    ares = session.query(ItemName).filter_by(companynameid=arid).all()
    try:
        if login_session['username']:
            return render_template('showCosmetics.html', ars_rat=ars_rat,
                                   ars=ars, ares=ares,
                                   uname=login_session['username'])
    except:
        return render_template('showCosmetics.html',
                               ars_rat=ars_rat, ars=ars, ares=ares)

#####
# Add New CosmeticCompanyName


@app.route('/CosmeticHub/addCompanyName', methods=['POST', 'GET'])
def addCompanyName():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        companyname = CompanyName(name=request.form['name'],
                                  user_id=login_session['user_id'])
        session.add(companyname)
        session.commit()
        return redirect(url_for('CosmeticHub'))
    else:
        return render_template('addCompanyName.html', ars_rat=ars_rat)

########
# Edit CosmeticCompanName


@app.route('/CosmeticHub/<int:arid>/edit', methods=['POST', 'GET'])
def editCompanyName(arid):
    editCompanyName = session.query(CompanyName).filter_by(id=arid).one()
    creator = getUserInfo(editCompanyName.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Restaurent Name."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CosmeticHub'))
    if request.method == "POST":
        if request.form['name']:
            editCompanyName.name = request.form['name']
        session.add(editCompanyName)
        session.commit()
        flash("Company Name Edited Successfully")
        return redirect(url_for('CosmeticHub'))
    else:
        # ars_rat is global variable we can them in entire application
        return render_template('editCompanyName.html',
                               ar=editCompanyName, ars_rat=ars_rat)

#####
# Delete  CosmeticCompanyName


@app.route('/CosmeticHub/<int:arid>/delete', methods=['POST', 'GET'])
def deleteCompanyName(arid):
    ar = session.query(CompanyName).filter_by(id=arid).one()
    creator = getUserInfo(ar.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this CompanyName."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('CosmeticHub'))
    if request.method == "POST":
        session.delete(ar)
        session.commit()
        flash("Company Name Deleted Successfully")
        return redirect(url_for('CosmeticHub'))
    else:
        return render_template(
            'deleteCompanyName.html', ar=ar, ars_rat=ars_rat)

######
# Add New Cosmetic ItemName Details


@app.route(
    '/CosmeticHub/addCompanyName/addCompanyItemDetails/<string:arname>/add',
    methods=['GET', 'POST'])
def addCompanyDetails(arname):
    ars = session.query(CompanyName).filter_by(name=arname).one()
    # See if the logged in user is not the owner of item
    creator = getUserInfo(ars.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new Company item"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showCosmetics', arid=ars.id))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        feedback = request.form['feedback']
        itemdetails = ItemName(name=name,
                               description=description,
                               price=price,
                               feedback=feedback,
                               date=datetime.datetime.now(),
                               companynameid=ars.id,
                               user_id=login_session['user_id'])
        session.add(itemdetails)
        session.commit()
        return redirect(url_for('showCosmetics', arid=ars.id))
    else:
        return render_template('addCompanyItemDetails.html',
                               arname=ars.name, ars_rat=ars_rat)

#####
# Edit Item details


@app.route('/CosmeticHub/<int:arid>/<string:arename>/edit',
           methods=['GET', 'POST'])
def editCompanyItem(arid, arename):
    ar = session.query(CompanyName).filter_by(id=arid).one()
    itemdetails = session.query(ItemName).filter_by(name=arename).one()
    # See if the logged in user is not the owner of item
    creator = getUserInfo(ar.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this company item"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showCosmetics', arid=ar.id))
    # POST methods
    if request.method == 'POST':
        itemdetails.name = request.form['name']
        itemdetails.description = request.form['description']
        itemdetails.price = request.form['price']
        itemdetails.feedback = request.form['feedback']
        itemdetails.date = datetime.datetime.now()
        session.add(itemdetails)
        session.commit()
        flash("Item Edited Successfully")
        return redirect(url_for('showCosmetics', arid=arid))
    else:
        return render_template(
            'editCompanyItem.html',
            arid=arid, itemdetails=itemdetails, ars_rat=ars_rat)

#####
# Delete items in cosmetic companies


@app.route('/CosmeticHub/<int:arid>/<string:arename>/delete',
           methods=['GET', 'POST'])
def deleteCompanyItem(arid, arename):
    ar = session.query(CompanyName).filter_by(id=arid).one()
    itemdetails = session.query(ItemName).filter_by(name=arename).one()
    # See if the logged in user is not the owner of item
    creator = getUserInfo(ar.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this item"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showCosmetics', arid=ar.id))
    if request.method == "POST":
        session.delete(itemdetails)
        session.commit()
        flash("Deleted item Successfully")
        return redirect(url_for('showCosmetics', arid=arid))
    else:
        return render_template('deleteCompanyItem.html',
                               arid=arid, itemdetails=itemdetails,
                               ars_rat=ars_rat
                               )

#####
# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={
                      'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
#####
# Json
# Displays the whole CosmeticHub. Companies and all items.


@app.route('/CosmeticHub/JSON')
def allCompaniesJSON():
    companyname = session.query(CompanyName).all()
    category_dict = [c.serialize for c in companyname]
    for c in range(len(category_dict)):
        cosmetics = [i.serialize for i in session.query(
                 ItemName).filter_by(
                     companynameid=category_dict[c]["id"]).all()]
        if cosmetics:
            category_dict[c]["cosmetics"] = cosmetics
    return jsonify(CompanyName=category_dict)

#####
# Displays all companies


@app.route('/CosmeticHub/CompanyName/JSON')
def categoriesJSON():
    cosmetics = session.query(CompanyName).all()
    return jsonify(companyName=[c.serialize for c in cosmetics])

#####
# Displays  all cosmetic company items


@app.route('/CosmeticHub/cosmetics/JSON')
def itemsJSON():
    items = session.query(ItemName).all()
    return jsonify(cosmetics=[i.serialize for i in items])

#####
# Displays items for specific company


@app.route('/CosmeticHub/<path:company_name>/cosmetics/JSON')
def categoryItemsJSON(company_name):
    companyName = session.query(CompanyName).filter_by(name=company_name).one()
    cosmetics = session.query(ItemName).filter_by(
        companyname=companyName).all()
    return jsonify(companyName=[i.serialize for i in cosmetics])

#####
# Displays a specific company item.


@app.route('/CosmeticHub/<path:company_name>/<path:companyitem_name>/JSON')
def ItemJSON(company_name, companyitem_name):
    companyName = session.query(CompanyName).filter_by(name=company_name).one()
    companyItemName = session.query(ItemName).filter_by(
        name=companyitem_name, companyname=companyName).one()
    return jsonify(companyItemName=[companyItemName.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)

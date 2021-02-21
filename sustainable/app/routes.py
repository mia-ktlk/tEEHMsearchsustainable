from flask import render_template, redirect, session, url_for, request
from sustainable.app import app, db, auth
from sustainable.app.forms import LoginForm, ForgetPasswordForm, SearchBar, ReportForm, ConfirmForm, SuggestForm
from sustainable.app.search import getResults, explicitSearch
from selenium import webdriver



@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = SearchBar()
    if form.validate_on_submit():
        term = form.search.data
        filter = form.filter.data
        results = getResults(term, 'items', filter)
        return render_template("results.html", results=results, term=term, form=form)

    return render_template("index.html", title="Home", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        print(session["usr"])
        return redirect(url_for("dashboard"))
    except KeyError:
        form = LoginForm()
        if form.validate_on_submit():
            try:
                user = auth.sign_in_with_email_and_password(
                    form.username.data, form.password.data
                )
                user_id = user["idToken"]
                session["usr"] = user_id
                return redirect(url_for("dashboard"))
            except:
                fail = True
                return render_template("login.html", fail=fail, form=form)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/dashboard")
def dashboard():
    # get reported items
    temp = db.child("reported").get()
    temp2 = db.child("suggested").get()
    rResults = []
    sResults = []
    if temp:
        for item in temp.each():
            rResults.append(item.val())
            full = True
    else:
        full = False
        rResults.append("There are no open reports.")

    if temp2:
        for item in temp2.each():
            sResults.append(item.val())
            full2 = True
    else:
        full2 = False
        sResults.append("There are no current suggestions.")
    return render_template("dash.html", title="Admin Dashboard", reports = rResults, suggestions = sResults, full=full, full2=full2)


@app.route("/forgotPass", methods=["GET", "POST"])
def forgotPass():
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        try:
            auth.send_password_reset_email(form.email.data)
            return redirect(url_for("login"))
        except:
            fail = True
            return render_template("forgotPass.html", fail=fail, form=form)

    return render_template("forgotPass.html", title="Forgot Password", form=form)


@app.route('/report', methods=["GET", "POST"])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        try:
            print("plese not this one")

            itemName = request.args.get('name')

            print("checkpoint 0")

            item = explicitSearch(itemName)
            print("checkpoint 0.5")

            myDict = {}
            myDict['origKey'] = item.key()
            myDict['itemName'] = item.val()['name']
            myDict['message'] = form.reason.data
            myDict['reportKey'] = ""
            print("checkpoint 1")
            temp = db.child("reported").push(myDict)
            print("checkpoint 2")
            jankId = temp['name']
            db.child("reported").child(jankId).update({"reportKey": jankId})
            return redirect(url_for("index"))
        except:
            fail = True
            print('mission failed')
            return render_template("report.html", fail=fail, form=form)
    return render_template("report.html", title="Report a Issue", form=form)


@app.route('/suggest', methods=["GET", "POST"])
def suggest():
    form = SuggestForm()

    if form.validate_on_submit():
        try:
            myDict = {}
            myDict['compName'] = form.name.data
            myDict['message'] = form.reason.data
            myDict['url'] = form.url.data
            myDict['sKey'] = ""
            temp = db.child("suggested").push(myDict)
            print("checkpoint 2")
            jankId = temp['name']
            db.child("suggested").child(jankId).update({"sKey": jankId})
            return redirect(url_for("index"))
        except:
            fail = True
            return render_template("suggest.html", title="Make a Suggestion", fail=fail, form=form)
    return render_template("suggest.html", title="Make a Suggestion", form=form)



@app.route('/adminReports', methods=["GET", "POST"])
def adminReports():   
    temp = db.child("reported").get()
    results = []
    for item in temp.each():
        results.append(item.val())
   
    
    return render_template("adminReports.html", results=results)

@app.route('/deleteConfirm', methods=["GET", "POST"])
def deleteConfirm():
    form = ConfirmForm()
    dataB = request.args.get('delet')
    key =  request.args.get('key')
    otherKey = request.args.get('otherKey') #only used if dataB is items

    try:
        print(session["usr"])
        if form.validate_on_submit():
            if(form.keyword.data.upper() == "GREEN EARTH"):
                db.child(dataB).child(key).remove()
                if dataB == "items":
                    db.child('reported').child(otherKey).remove()
                return redirect(url_for('dashboard'))
            else:
                render_template('deleteConfirm.html', fail=True, dataB = dataB, key = key, otherKey=otherKey, form=form)
    except:
        redirect(url_for(index))
    return render_template('deleteConfirm.html', dataB = dataB, key = key, otherKey=otherKey, form=form)


# @app.route("/results", methods=['GET', 'POST'])

# # def results():
# #     results = [{'approved': 'True', 'brand': "Aunt Fannie's", 'date_stored': '02/20/2021', 'img_src': 'https://res.cloudinary.com/epantry/image/upload/f_auto,fl_progressive,h_368,w_auto,q_auto,dpr_auto,ar_1:1,c_pad,b_white/v1551375738/lkxogluw79du0t6yibe1.jpg', 'name': 'Mosquito Repellent Spray', 'price': 9.99, 'rating': 4, 'search_terms': 'repellent', 'url': 'https://www.grove.co/catalog/product/mosquito-repellent-spray/?v=3933&attrsrc=18&attrpg=catalog&attrpos=1', 'vendor': 'Grove Collaborative'}, {'approved': 'True', 'brand': 'Babyganics', 'date_stored': '02/20/2021', 'img_src': 'https://res.cloudinary.com/epantry/image/upload/f_auto,fl_progressive,h_600,q_auto/v1531517815/wdusmep23sjqgnxdej2c.jpg', 'name': 'Insect Repellent', 'price': 9.99, 'rating': 4.4, 'search_terms': 'repellent', 'url': 'https://www.grove.co/catalog/product/insect-repellent/?v=1518&attrsrc=18&attrpg=catalog&attrpos=0', 'vendor': 'Grove Collaborative'}]
# #     return render_template('results.html', title="results", results=results)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico')

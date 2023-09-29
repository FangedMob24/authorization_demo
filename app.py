from flask import Flask, request, render_template, redirect
from flask import flash, session
from models import db, User, Feedback
from forms import AddUserForm, LoginUser, NewFeedback


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "secret"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    else:
        # load the test config if passed in
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True

    db.init_app(app)

    return app

app = create_app()

# 
# UI ROUTES
# 

@app.route('/')
def redirect_register():
    return redirect('/register')

@app.route('/register',methods=['GET','POST'])
def register_form():
    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password,
                        email, first_name,
                        last_name)
        
        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect(f'/users/{new_user.username}')
    else:
        return render_template('register_form.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_form():
    form = LoginUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if(user == False):
            flash("Username or Password is incorrect")
            return redirect('/login')
        else:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
    else:
        return render_template('login_form.html', form=form)
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# 
# USER ROUTES
# 

@app.route('/users/<username>')
def user(username):
    """   """
    if "username" in session and session["username"] == username:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username).all()
        return render_template('user.html', user=user, feedback=feedback)
    else:

        return redirect("/register")
    
@app.route('/users/<username>/delete',methods=["POST"])
def delete_user(username):
    """  """
    if "username" in session and session["username"] == username:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=username).all()

        db.session.delete(user)
        for feed in feedback:
            db.session.delete(feed)

        db.session.commit()
        return redirect('/')
    else:
        return redirect('/login')

@app.route('/users/<username>/feedback/add',methods=["GET","POST"])
def new_feedback(username):
    """  """
    if "username" in session and session["username"] == username:
        form = NewFeedback()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            feed = Feedback(title=title, content=content, username=username)
            db.session.add(feed)
            db.session.commit()

            return redirect(f'/users/{username}')
        else:
            return render_template('feedback_form.html',form=form)
    else:
        return redirect('/login')



@app.route('/feedback/<feedback_id>/update', methods=["GET","POST"])
def update_feedback(feedback_id):
    """  """
    feed = Feedback.query.get_or_404(feedback_id)

    if "username" in session and session["username"] == feed.username:
        form = NewFeedback(obj=feed)

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            feed.title = title
            feed.content = content

            db.session.commit()

            return redirect(f'/users/{feed.username}')
        else:
            return render_template('feedback_form.html',form=form)
    else:
        return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """  """
    feed = Feedback.query.get_or_404(feedback_id)
    username = feed.username

    if "username" in session and session["username"] == username:
        db.session.delete(feed)
        db.session.commit()
        return redirect(f'/users/{username}')
    else:
        return redirect('/login')
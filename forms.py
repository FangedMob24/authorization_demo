from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField
from wtforms.validators import InputRequired, Length

class AddUserForm(FlaskForm):
    """Form for adding users"""

    username = StringField("Username",
                           validators=[InputRequired(),Length(max=20)])

    password = PasswordField("Password",
                           validators=[InputRequired()])

    email = EmailField("Email",
                       validators=[InputRequired(),Length(max=50)])

    first_name = StringField("First Name",
                             validators=[InputRequired(),Length(max=30)])

    last_name = StringField("Last Name",
                            validators=[InputRequired(),Length(max=30)])
    
class LoginUser(FlaskForm):
    """Form for loging in an alrendy created user"""

    username = StringField("Username",
                           validators=[InputRequired(),Length(max=20)])

    password = PasswordField("Password",
                           validators=[InputRequired()])
    
class NewFeedback(FlaskForm):
    """ To add new feedback """

    title = StringField("Title",
                        validators=[InputRequired(),Length(max=100)])
    
    content = StringField("Content",
                          validators=[InputRequired()])
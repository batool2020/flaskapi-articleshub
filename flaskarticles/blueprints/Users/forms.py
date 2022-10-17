from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from flaskarticles.Models.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    # Validate the field, if  it's already exist, raise error

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first() # if this username exist, through validation error
        if user:
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()  # if this email exist, through validation error
            if user:
                raise ValidationError('That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


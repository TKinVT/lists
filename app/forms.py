from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from app.models import List


class NewListForm(FlaskForm):
    name = StringField('List name', validators=[DataRequired()])
    checklist = BooleanField('Checklist?')
    private = BooleanField('Private?')
    submit = SubmitField('Add List')

    def validate_name(self, name):
        # print(name.data)
        # names = [list.name for list in List.objects()]
        # print(names)
        # if name.data in names:
        list = List.objects(name=name.data)
        if list.count() > 0:
            raise ValidationError('Name already taken. Choose a new one.')


class EditListForm(FlaskForm):
    name = StringField('List name', validators=[DataRequired()])
    checklist = BooleanField('Checklist?')
    private = BooleanField('Private?')
    submit = SubmitField('Save')

    # fixing the duplicate list name bug
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
    def __init__(self, original_name, *args, **kwargs):
        super(EditListForm, self).__init__(*args, **kwargs)
        self.original_name = original_name

    def validate_name(self, name):
        if name.data != self.original_name:
            list = List.objects(name=name.data)
            if list.count() > 0:
                raise ValidationError('Name already taken. Choose a new one.')


class NewItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add Item')


class EditItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Save')


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

from wtforms import Form, StringField, DateField, SelectField, validators


class UserForm(Form):
    first_name = StringField('First name', [validators.DataRequired(), validators.Length(min=3, max=25)])
    last_name = StringField('Last name', [validators.DataRequired(), validators.Length(min=3, max=25)])
    department_id = SelectField('Department', [validators.Optional()], coerce=int)
    position_id = SelectField('Position', [validators.Optional()], coerce=int)
    email = StringField('Email', [validators.Optional(), validators.Email()])
    phone = StringField('Phone', [validators.Optional(), validators.Regexp(r'\+[0-9]{12}$')])  # +380505005050
    date_of_birth = DateField('Date of birth (dd-mm-yyyy)', [validators.DataRequired()], format='%d-%m-%Y')

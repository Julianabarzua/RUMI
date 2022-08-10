from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.firstname = data['fname']
        self.lastname = data['lname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at ) VALUES (%(firstname)s,%(lastname)s,%(email)s,%(password)s, NOW() , NOW() );"
        return connectToMySQL('rumi_schema').query_db( query, data )

    @classmethod
    def get_all_emails(cls):
        query = "SELECT email FROM users;"
        results = connectToMySQL('rumi_schema').query_db(query)
        emails = []
        for email in results:
            emails.append(email)
        return emails

    @classmethod
    def logedUser(cls, data):
        query = """
        SELECT * FROM users WHERE id = %(id)s;
        """
        result = connectToMySQL('rumi_schema').query_db(query, data)
        return result

    @staticmethod
    def validate_user(user):

        is_valid = True
        all_emails = User.get_all_emails()

        if len(user['fname']) < 2:
            flash("First name must be at least 2 characters.")
            is_valid = False

        if not user['fname'].isalpha():
            flash("First name must be just letters.")
            is_valid = False

        if len(user['lname']) < 2:
            flash("Last name must be at least 2 characters.")
            is_valid = False

        if not user['lname'].isalpha():
            flash("Last name must be just letters.")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!")
            is_valid = False

        for correo in all_emails:
            if user['email'] == correo['email']:
                flash('Mail already registered, please add a new one')
                is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False

        if user['password'] != user['password2']:
            flash("Password doesnt match, try again")
            is_valid = False


        return is_valid

    @classmethod
    def getEmail(cls, data):
        query = """
        SELECT * FROM users JOIN users_groups ON id = user_id WHERE email = %(email)s;
        """
        resultado = connectToMySQL('rumi_schema').query_db(query, data)
        return resultado
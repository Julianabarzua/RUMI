from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Group:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.pin = data['pin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO rumi_schema.groups (name, pin) VALUES (%(name)s,%(pin)s);"
        return connectToMySQL('rumi_schema').query_db( query, data )

    @classmethod
    def get_all_groups(cls):
        query = "SELECT * FROM rumi_schema.groups;"
        results = connectToMySQL('rumi_schema').query_db(query)
        groups = []
        for group in results:
            groups.append(group)
        return groups

    @classmethod
    def save_user_to_group(cls, data ):
        query = "INSERT INTO rumi_schema.users_groups (group_id, user_id) VALUES (%(group_id)s,%(user_id)s);"
        return connectToMySQL('rumi_schema').query_db( query, data )

    @classmethod
    def get_group_by_id(cls,data):
        query = """
        SELECT * FROM rumi_schema.groups WHERE id = %(group_id)s;
        """
        resultado = connectToMySQL('rumi_schema').query_db(query, data)
        return resultado

    @classmethod
    def get_group_by_user_id(cls,data):
        query = """
        SELECT * FROM rumi_schema.groups
        JOIN users_groups ON rumi_schema.groups.id = rumi_schema.users_groups.group_id
        WHERE user_id = %(id)s;
        """
        resultado = connectToMySQL('rumi_schema').query_db(query, data)
        return resultado

    @staticmethod
    def validate_group(user):

        is_valid = True

        if len(user['pin']) != 4:
            flash("PIN must be 4 digits")
            is_valid = False

        if user['pin'] != user['pin2']:
            flash("PIN doesnt match, try again")
            is_valid = False

        return is_valid



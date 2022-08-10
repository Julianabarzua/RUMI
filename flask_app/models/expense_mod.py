from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash


class Expense:
    def __init__(self,data):
        self.id = data['id']
        self.amount = data['amount']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = data['posted_by']
        self.posted_by_name = data['posted_by_name']
        self.date = data['date']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO expenses (amount, description, posted_by, created_at, updated_at, date ) VALUES (%(amount)s,%(description)s,%(posted_by)s, NOW() , NOW(), %(date)s );"
        return connectToMySQL('rumi_schema').query_db( query, data )

    @classmethod
    def get_all_from_group(cls, data):
        query = """SELECT expenses.id, amount, description, posted_by, expenses.created_at, expenses.updated_at, users.first_name as posted_by_name, date
        from expenses
        join users on posted_by = users.id
        JOIN users_groups ON posted_by = user_id
		WHERE group_id=%(group_id)s AND month(date) = %(month)s AND year(date) = %(year)s
        ORDER BY expenses.date ;
                """
        results = connectToMySQL('rumi_schema').query_db(query, data)
        print(results)
        expenses = []
        for expense in results:
            expenses.append(cls(expense))
        return expenses

    @classmethod
    def get_totals_for_users(cls,data):
        query = """
                    SELECT rumi_schema.users.id,CONCAT(rumi_schema.users.first_name,' ', rumi_schema.users.last_name) as name, group_id, SUM(amount) as total_amount FROM rumi_schema.users
                    LEFT JOIN users_groups ON rumi_schema.users.id = user_id
                    LEFT JOIN expenses ON posted_by =rumi_schema.users.id
                    WHERE group_id = %(group_id)s AND month(date) = %(month)s AND year(date) = %(year)s
                    GROUP BY rumi_schema.users.id;
                """

        results = connectToMySQL('rumi_schema').query_db(query, data)
        return results

    @classmethod
    def delete(cls,id):
        query = "DELETE FROM expenses WHERE id ="+id+";"
        return connectToMySQL('rumi_schema').query_db( query)

    @classmethod
    def getonebyid(cls, id ):
        query = "SELECT * from expenses WHERE expenses.id ="+id+";"
        
        expense = connectToMySQL('rumi_schema').query_db( query)
        print(expense)
        return expense

    @classmethod
    def update_expense(cls,data, id):
        query = "UPDATE expenses SET date=%(date)s, amount=%(amount)s, description=%(description)s, expenses.updated_at = NOW() WHERE expenses.id ="+id+";"
        return connectToMySQL('rumi_schema').query_db( query, data)
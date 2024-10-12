from flask_pymongo import PyMongo
from bson import ObjectId

mongo = PyMongo()

class User:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.role = role

    def save(self):
        mongo.db.users.insert_one({
            'username': self.username,
            'password': self.password,
            'role': self.role
        })

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({'username': username})

class Loan:
    def __init__(self, user_id, amount, reason, status='pending'):
        self.user_id = user_id
        self.amount = amount
        self.reason = reason
        self.status = status

    def save(self):
        mongo.db.loans.insert_one({
            'user_id': self.user_id,
            'amount': self.amount,
            'reason': self.reason,
            'status': self.status
        })

    @staticmethod
    def find_by_user_id(user_id):
        return mongo.db.loans.find({'user_id': user_id})

    @staticmethod
    def update_loan(loan_id, update_data):
        mongo.db.loans.update_one({'_id': ObjectId(loan_id)}, {'$set': update_data})

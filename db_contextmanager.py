from terminal import User
from create_db import connect
from exceptions import UserCreationFail


class CreateUserContextManager:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.local_connection = None
        self.result = None
        self.err = None
        self.user = None
        self.exc_type = None
        self.exc_val = None

    def __enter__(self):
        return self

    def create_user(self, first_name, last_name, password, phone, email, role, con=None, cur=None):
        if all([first_name, last_name, password, phone, email, role]):
            self.user = User.register_new_user(first_name, last_name, password, phone, email, role)
        else:
            raise UserCreationFail('ساخت کاربر با خطا مواجه شد')

        if self.user:
            self.user.user_id = None
            self.conn, self.cur, self.local_connection = connect(con, cur)
            query = """INSERT INTO travel_user(first_name, last_name, password, phone, email, role_id, 
            is_authenticated, have_bank_account) values (%s,%s,%s,%s,%s,%s,%s,%s)"""

            self.user.insert_to_database(self.cur, query=query)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and self.local_connection:
            self.user = None
            self.err = f'create user fail\nHINT {exc_val}'
            self.cur.execute('ROLLBACK')
            self.cur.close()
            self.conn.close()
        elif exc_val and not self.local_connection:
            self.err = f'create user fail\nHINT {exc_val}'
        elif not exc_val and self.user is not None and self.user.have_bank_account and self.local_connection:
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            self.result = 'create user and back account success '
        elif not self.user.have_bank_account:
            self.cur.execute('ROLLBACK')
            self.cur.close()
            self.conn.close()
            self.err = 'user not have back account'
        elif not exc_val and self.user.have_bank_account and not self.local_connection:
            self.result = f'user {self.user.full_name} created'

        return True
